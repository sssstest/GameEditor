#!/usr/bin/env python

from tokens import *

class linker():
	def __init__(self, g, triple, e) :
		self.source=g#game
		self.errors=e#error_stream
		td=get_target(triple)#str
		self.compiler=td

	def build(self, target):#str
		self.errors.progress(20, "compiling libraries")
		self.build_libraries()

		self.errors.progress(30, "compiling scripts")
		self.build_scripts()

		self.errors.progress(40, "compiling objects")
		self.build_objects()

		if self.errors.count() > 0:
			return False

		self.errors.progress(60, "linking runtime")
		game = compiler.get_module()

		linker = Linker("", "", game.getContext())
		linker.LinkInModule(game)
		linker.LinkInFile("runtime.bc")
		module = linker.getModule()

		errors.progress(80, "optimizing game")
		pm = PassManager()
		pm.add(new TargetData(*td))

		pmb = PassManagerBuilder()
		pmb.OptLevel = 3
		pmb.Inliner = createFunctionInliningPass(275)
		pmb.populateModulePassManager(pm)
		pmb.populateLTOPassManager(pm, true, true)

		pm.add(createVerifierPass())

		std::string error_info
		std::unique_ptr<tool_output_file> out(
			new tool_output_file(target, error_info, raw_fd_ostream::F_Binary)
		)
		if not error_info.empty():
			errors.error(error_info)
			return false

		pm.add(createBitcodeWriterPass(out->os()))
		pm.run(module)
		out.keep()

		return errors.count() == 0

	def build_libraries(self):
		for i in range(0,self.source.nactions):
			if (self.source.actions[i].exec != action_type::exec_code)
				continue

			name = "action_lib"
			if self.source.actions[i].parent > -1:
				name += self.source.actions[i].parent
			name += "_" + self.source.actions[i].id

			self.add_function(
				len(self.source.actions[i].code), self.source.actions[i].code,
				name, 16 + self.source.actions[i].relative
			)

	def build_scripts(self):
		for i in range(0,self.source.nscripts):
			add_function(
				len(self.source.scripts[i].code), self.source.scripts[i].code, self.source.scripts[i].name, 16
			)

	def build_objects(self):
		for i in range(0,self.source.nobjects):
			object &obj = source.objects[i]
			# todo: output object properties

			for e in range(0,obj.nevents):
				event &evt = obj.events[e]
				# todo: output event data

				# todo: move this into compiler
				code=""
				for a in range(0,evt.nactions):
					act = evt.actions[a]

					# todo: don't do this by unparsing and reparsing
					if act.type->kind==action_type::act_begin:
						code += "{\n"
					elif act.type->kind==action_type::act_end:
						code += "}\n"
					elif act.type->kind==action_type::act_else:
						code += "else\n"
					elif act.type->kind==action_type::act_exit:
						code += "exit\n"

					elif act.type->kind==action_type::act_repeat:
						code += "repeat (" << act.args[0].val << ")\n"
					elif act.type->kind==action_type::act_variable:
						code
							+= act.args[0].val
							+ (act.relative ? " += " : " = ")
							+ act.args[1].val + "\n"

					elif act.type->kind==action_type::act_code:
						s = obj.name + "_" + evt.main_id + "_" + evt.sub_id + "_" + a
						self.add_function(len(act.args[0].val), act.args[0].val, s, 0)

						code += s.str() + "()\n"

					elif act.type->kind==action_type::act_normal:
						if act.type->exec == action_type::exec_none:
							continue

						if act.target != action::self:
							code += "with (" + act.target + ")"
						if act.type->question:
							code += "if ("
							if act.inv:
								code += "!"

						if act.type->exec == action_type::exec_code:
							code += "action_lib"
							if act.type->parent > -1:
								code += act.type->parent
							code += "_" + act.type->id
						else:
							code += act.type->code

						code += '('
						n = 0
						for n in range(0,act.nargs):
							if (i != 0) code += ", "
							code += act.args[n]
						for n in range(n,16):
							if (n != 0) code += ", "
							code += 0
						if act.type->relative:
							code += ", " + act.relative
						code += ")"

						if act.type.question:
							code += ")"

						code += '\n'

					#else: # do nothing

				s = obj.name + "_" + evt.main_id + "_" + evt.sub_id
				self.add_function(len(code), code, s, 0)

#std::ostream &operator <<(std::ostream &out, const argument &arg) {
#	switch (arg.kind) {
#	case argument::arg_expr:
#		return out << arg.val
#
#	case argument::arg_both:
#		if (arg.val[0] == '"' || arg.val[0] == '\'') return out << arg.val
#
#	// fall through
#	case argument::arg_string: {
#		std::string val(arg.val)
#		while (val.find('"') != std::string::npos) {
#			val.replace(val.find('"'), 1, "\"+'\"'+\"")
#		}
#		return out << '"' << val << '"'
#	}
#
#	case argument::arg_bool:
#		return out << (arg.val[0] == '0')
#
#	case argument::arg_menu:
#		return out << arg.val
#
#	case argument::arg_color:
#		return out << '$' << arg.val
#
#	default:
#		return out << arg.resource
#	}
#}

	def add_function(self, size_t length, const char *data, const std::string &name, int args):
		code=""
		tokens = token_stream(code)
		parser = parser(tokens, self.errors)
		self.errors.set_context(name)

		std::unique_ptr<node> program(parser.getprogram())
		if self.errors.count() > 0:
			return

		compiler.add_function(program.get(), name.c_str(), args)
