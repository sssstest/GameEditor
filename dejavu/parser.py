#!/usr/bin/env python

from tokens import *
from lexer import *
from driver import *
from node import *
from error_stream import *

def isassignment(t):#token_type
	if t in [equals,plus_equals,minus_equals,times_equals,div_equals,and_equals,or_equals,xor_equals]:
		return True

	else:
		return False

class symbol():
	def __init__(self):
		self.precedence=1
		self.std=None
		self.nud=None
		self.led=None

	def __str__(self):
		return "symbol("+str(self.precedence)+" "+str(self.std)+" "+str(self.nud)+" "+str(self.led)+")"

class parser():
	def __init__(self, l, e):#token_stream error_stream
		self.lexer=l
		self.current=self.lexer.gettoken()
		self.errors=e
		e.parser=self

	def getprogram(self):
		if self.current.type == l_brace:
			stmt = self.getstatement()
		else:
			stmts=[]
			while self.current.type != eof:
				stmts.append(self.getstatement())

			stmt = block(stmts)

		self.advance2(eof)
		return stmt

	def getexpression(self, prec=1):
		t = self.advance()

		n = symbols[t.type].nud#nud_parser
		if not n:
			# skip to the next token that could start an expression
			self.advance()
			while not symbols[self.current.type].nud:
				self.advance()

			return self.error_expr(unexpected_token_error(t, "expression"))

		left = n(self,t)

		while prec < symbols[self.current.type].precedence:
			# fixme: is there a better way for led_parsers to reject ts and lefts?
			#if self.current.type == l_paren and not (left.type == value_node and left.t.type == name):
				#print "break paren"
			#	break
			#if self.current.type == l_square and not (left.type == value_node and left.t.type == name) and not (left.type == binary_node and left.op == dot):
				#print "break square"
				#break
			# fixme: is there a better way to tell if the previous expr was in parens?
			if self.current.type == l_square and t.type == l_paren:
				#print "break square paren"
				break

			t = self.advance()

			l = symbols[t.type].led#led_parser
			if not l:
				# skip to (I hope) the start of the next statement
				while not symbols[self.current.type].std:
					self.advance()

				return self.error_expr(unexpected_token_error(t, "operator"))
			left = l(self, t, left)

		return left

	def id_nud(self, t):#token
		return value(t)

	def prefix_nud(self, t):
		return unary(t.type, self.getexpression(70))

	def paren_nud(self, t):
		expr = self.getexpression(0)
		self.advance2(r_paren)
		return expr

	def null_nud(self, t):
		return error_expr(unexpected_token_error(t, "expression"))

	def infix_led(self, t, left):#expression
		if t.type == equals:
			type = is_equals#token_type
		else:
			type = t.type
		return binary(
			type, left, self.getexpression(symbols[t.type].precedence)
		)

	def dot_led(self, t, left):
		n = self.advance2(name)
		if n.type != name:
			return expression_error()

		return binary(t.type, left, symbols[n.type].nud(self, n))

	def square_led(self, t, left):
		indices=[]
		while self.current.type != r_square and self.current.type != eof:
			indices.append(self.getexpression())

			if self.current.type == comma:
				self.advance()
			else:
				break

		#self.advance(r_square) # or expected comma
		if self.current.type != r_square:
			e = self.current
			while not symbols[self.current.type].std:
				self.advance()

			return self.error_expr(unexpected_token_error(e, "[ or ,"))

		self.advance()

		return subscript(left, indices)

	def paren_led(self, t, left):
		args=[]
		while self.current.type != r_paren and self.current.type != eof:
			args.append(self.getexpression(0))

			if self.current.type == comma:
				self.advance()
			else:
				break
		self.advance2(r_paren) # or expected comma

		return call(left, args)

	def ternary_led(self, t, left):
		cond = left

		branch_true = self.getexpression(1)

		if self.current.type == colon:
			self.advance()
			branch_false = self.getexpression(1)
		else:
			self.error_stmt(unexpected_token_error(e, "colon"))

		return ifstatement(cond, branch_true, branch_false)

	def getstatement(self):
		if self.current.type == comma:
			self.advance()
		s = symbols[self.current.type].std
		if not s:
			# skip to the next token that could start a statement
			e = self.current
			while not symbols[self.current.type].std:
				self.advance()

			return self.error_stmt(unexpected_token_error(e, "statement"))
		stmt = s(self)

		while self.current.type == semicolon:
			self.advance()

		return stmt

	def global_local_std(self):
		t = self.advance()
		if self.current.type == dot:
			self.backup(t)
			return self.expr_std()
		else:
			self.backup(t)
			return self.var_std()

	def expr_std(self):
		lvalue = self.getexpression(symbols[equals].precedence)

		if lvalue.type == call_node:
			return invocation(lvalue)

		if not isassignment(self.current.type):
			e = self.current
			while not symbols[self.current.type].std:
				self.advance()
			return self.error_stmt(unexpected_token_error(e, "assignment operator"))

		op = self.advance().type#token_type

		rvalue = self.getexpression()

		return assignment(op, lvalue, rvalue)

	def var_std(self):
		t = self.advance()

		names=[]
		assignments=[]
		types=[t]
		while self.current.type != semicolon and self.current.type != eof:
			if self.current.type == kw_var:
				t=self.advance()
				types.append(t)
				continue
			n = self.advance2(name)
			if n.type != name:
				if len(assignments)>0:
					stmts = [declaration(types, names)]
					stmts.extend(assignments)
					return block(stmts, False)
				return declaration(types, names)

			names.append(symbols[n.type].nud(self, n))

			if self.current.type == comma:
				self.advance()
			if isassignment(self.current.type):
				op = self.advance().type#token_type
				rvalue = self.getexpression()
				assignments.append(assignment(op, names[-1], rvalue))
				if self.current.type == comma:
					self.advance()

		self.advance2(semicolon)

		if len(assignments)>0:
			stmts = [declaration(types, names)]
			stmts.extend(assignments)
			return block(stmts, False)
		return declaration(types, names)

	def brace_std(self):
		self.advance()

		stmts=[]
		while self.current.type != r_brace and self.current.type != eof:
			stmts.append(self.getstatement())

		self.advance2(r_brace)

		return block(stmts)

	def if_std(self):
		self.advance()
		cond = self.getexpression()

		if self.current.type == kw_then:
			self.advance()
		branch_true = self.getstatement()

		branch_false = 0
		if self.current.type == kw_else:
			self.advance()
			branch_false = self.getstatement()

		return ifstatement(cond, branch_true, branch_false)

	def while_std(self):
		self.advance()
		cond = self.getexpression()

		if self.current.type == kw_do:
			self.advance()
		stmt = self.getstatement()

		return whilestatement(cond, stmt)

	def do_std(self):
		self.advance()
		stmt = self.getstatement()

		self.advance(kw_until)

		cond = self.getexpression()

		return dostatement(cond, stmt)

	def repeat_std(self):
		self.advance()
		count = self.getexpression()
		stmt = self.getstatement()
		return repeatstatement(count, stmt)

	def for_std(self):
		self.advance()

		self.advance2(l_paren)

		init = self.getstatement()

		cond = self.getexpression()
		if self.current.type == semicolon:
			self.advance()

		inc = self.getstatement()

		self.advance2(r_paren)

		stmt = self.getstatement()

		return forstatement(init, cond, inc, stmt)

	def switch_std(self):
		self.advance()

		expr = self.getexpression()

		if self.current.type != l_brace:
			return error_stmt(unexpected_token_error(self.current, l_brace))
		stmts = self.brace_std()

		return switchstatement(expr, stmts)

	def with_std(self):
		self.advance()
		expr = self.getexpression()

		if self.current.type == kw_do:
			self.advance()
		stmt = self.getstatement()

		return withstatement(expr, stmt)

	def jump_std(self):
		return jump(self.advance().type)

	def return_std(self):
		self.advance()

		expr = self.getexpression()

		return returnstatement(expr)

	def case_std(self):
		t = self.advance()

		expr = 0
		if t.type == kw_case:
			expr = self.getexpression()

		self.advance2(colon)

		return casestatement(expr)

	def unsigned_std(self):
		unsigned = self.advance()
		return attrnode("unsigned")

	def null_std(self):
		return self.error_stmt(unexpected_token_error(self.current, "statement"))

	def backup(self, r):
		self.current = r
		self.lexer.backup()

	def advance(self):
		r = self.current
		self.current = self.lexer.gettoken()
		return r

	def advance2(self, t):#token_type
		n = self.advance()
		if n.type != t:
			# skip to (I hope) the beginning of the next statement
			while not symbols[self.current.type].std:
				self.advance()
				if self.current.type not in symbols:
					print("not in symbols")
			self.errors.error(unexpected_token_error(n, t))
		return n

	def error_stmt(self, e):#unexpected_token_error
		self.errors.error(e)
		return statement_error()

	def error_expr(self, e):#unexpected_token_error
		self.errors.error(e)
		return expression_error()

class symbol_table(dict):#token_type, symbol
	def prefix(self, t, nud=parser.prefix_nud):#nud_parser
		if t not in self:
			self[t]=symbol()
		self[t].nud = nud

	def infix(self, t, prec, led=parser.infix_led):#int led_parser
		if t not in self:
			self[t]=symbol()
		self[t].precedence = prec
		self[t].led = led

	def __init__(self):
		self[real]=symbol()
		self[real].nud = parser.id_nud
		self[string]=symbol()
		self[string].nud = parser.id_nud
		self[kw_self]=symbol()
		self[kw_self].nud = parser.id_nud
		self[kw_other]=symbol()
		self[kw_other].nud = parser.id_nud
		self[kw_all]=symbol()
		self[kw_all].nud = parser.id_nud
		self[kw_noone]=symbol()
		self[kw_noone].nud = parser.id_nud
		self[kw_global]=symbol()
		self[kw_global].nud = parser.id_nud
		self[kw_local]=symbol()
		self[kw_local].nud = parser.id_nud
		self[kw_true]=symbol()
		self[kw_true].nud = parser.id_nud
		self[kw_false]=symbol()
		self[kw_false].nud = parser.id_nud
		self[name]=symbol()
		self[name].nud = parser.id_nud

		self.infix(dot, 90, parser.dot_led)

		self.prefix(l_paren, parser.paren_nud)

		self.infix(l_paren, 80, parser.paren_led)
		self.infix(l_square, 80, parser.square_led)

		self.prefix(exclaim)
		self.prefix(tilde)
		self.prefix(minus)
		self.prefix(plus)

		self.infix(times, 60)
		self.infix(divide, 60)
		self.infix(kw_div, 60)
		self.infix(kw_mod, 60)

		self.infix(plus, 50)
		self.infix(minus, 50)

		self.infix(shift_left, 40)
		self.infix(shift_right, 40)

		self.infix(bit_and, 30)
		self.infix(bit_or, 30)
		self.infix(bit_xor, 30)

		self.infix(less, 20)
		self.infix(less_equals, 20)
		self.infix(is_equals, 20)
		self.infix(equals, 20)
		self.infix(not_equals, 20)
		self.infix(greater, 20)
		self.infix(greater_equals, 20)

		self.infix(ampamp, 10)
		self.infix(pipepipe, 10)
		self.infix(caretcaret, 10)
		
		self[question]=symbol()
		#self[question].std = parser.ternary_std
		self[question].led = parser.ternary_led
		self[question].precedence=9

		self.infix(minus_equals, 9)
		self.infix(plus_equals, 9)
		self.infix(times_equals, 9)

		self[kw_var]=symbol()
		self[kw_var].std = parser.var_std
		self[kw_globalvar]=symbol()
		self[kw_globalvar].std = parser.var_std

		self[name].std = parser.expr_std
		self[l_paren].std = parser.expr_std
		self[kw_self].std = parser.expr_std
		self[kw_other].std = parser.expr_std
		self[kw_all].std = parser.expr_std
		self[kw_noone].std = parser.expr_std
		self[kw_global].std = parser.global_local_std#expr_std
		self[kw_local].std = parser.global_local_std#expr_std

		self[l_brace]=symbol()
		self[l_brace].std = parser.brace_std

		self[kw_if]=symbol()
		self[kw_if].std = parser.if_std
		self[kw_while]=symbol()
		self[kw_while].std = parser.while_std
		self[kw_do]=symbol()
		self[kw_do].std = parser.do_std
		self[kw_repeat]=symbol()
		self[kw_repeat].std = parser.repeat_std
		self[kw_for]=symbol()
		self[kw_for].std = parser.for_std
		self[kw_switch]=symbol()
		self[kw_switch].std = parser.switch_std
		self[kw_with]=symbol()
		self[kw_with].std = parser.with_std

		self[kw_break]=symbol()
		self[kw_break].std = parser.jump_std
		self[kw_continue]=symbol()
		self[kw_continue].std = parser.jump_std
		self[kw_exit]=symbol()
		self[kw_exit].std = parser.jump_std
		self[kw_return]=symbol()
		self[kw_return].std = parser.return_std
		self[kw_case]=symbol()
		self[kw_case].std = parser.case_std
		self[kw_default]=symbol()
		self[kw_default].std = parser.case_std

		self[eof]=symbol()
		self[eof].std = parser.null_std
		self[eof].nud = parser.null_nud

		self[semicolon]=symbol()
		self[semicolon].std = parser.null_std
		self[semicolon].nud = parser.null_nud
		self[comma]=symbol()
		self[comma].std = parser.null_std
		self[comma].nud = parser.null_nud
		self[comma].precedence=0

		self[r_paren]=symbol()
		self[r_paren].std = parser.null_std
		self[r_paren].nud = parser.null_nud
		self[r_paren].precedence=0
		self[r_square]=symbol()
		self[r_square].std = parser.null_std
		self[r_square].nud = parser.null_nud
		self[r_square].precedence=0
		self[r_brace]=symbol()
		self[r_brace].std = parser.null_std
		self[r_brace].nud = parser.null_nud
		self[r_brace].precedence=0
		self[unexpected]=symbol()
		self[unexpected].std = parser.null_std
		self[unexpected].nud = parser.null_nud
		self[unexpected].precedence=0
		self[colon]=symbol()
		self[colon].std = parser.null_std
		self[colon].nud = parser.null_nud
		self[colon].precedence=0
		self[kw_unsigned]=symbol()
		self[kw_unsigned].std = parser.unsigned_std
		self[kw_unsigned].precedence=0
		self[kw_else]=symbol()
		self[kw_else].std = parser.unsigned_std
		self[kw_else].precedence=0

symbols = symbol_table()

if __name__=="__main__":
	code=open("test.gml").read()
	tokens = token_stream(code)
	parser = parser(tokens, error_printer(build_log()))
	print parser.getprogram()
