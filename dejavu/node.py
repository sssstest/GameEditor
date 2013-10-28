#!/usr/bin/env python

expression_error_node=1

value_node=2
unary_node=3
binary_node=4
subscript_node=5
call_node=6

statement_error_node=7

assignment_node=8
invocation_node=9
declaration_node=10
block_node=11

ifstatement_node=12
whilestatement_node=13
dostatement_node=14
repeatstatement_node=15
forstatement_node=16
switchstatement_node=17
withstatement_node=18

jump_node=19
returnstatement_node=20
casestatement_node=21

class node(object):
	def __init__(self, type=None):
		self.type=type

class expression(node):
	def __init__(self, type=None):
		super(expression, self).__init__()
		self.node=type

class expression_error(expression):
	def __init__(self):
		super(expression_error, self).__init__()
		self.expression=expression_error_node

class attrnode(node):
	def __init__(self, attr):
		super(attrnode, self).__init__()
		self.type=None
		self.attr=attr

	def __str__(self):
		return "attrnode("+str(self.attr)+")"

class value(expression):
	def __init__(self, t):
		super(value, self).__init__()
		self.expression=value_node
		self.t=t

	def __str__(self):
		return "value("+str(self.t)+")"

class unary(expression):
	def __init__(self, op, right):
		super(unary, self).__init__()
		self.expression=unary_node
		self.op=op
		self.right=right
	#token_type op
	#expression *right

	def __str__(self):
		return "unary("+str(self.op)+" "+str(self.right)+")"

# todo: so much special handling for . - should it be its own node type?
class binary(expression):
	def __init__(self, op, left, right):
		super(binary, self).__init__()
		self.expression=binary_node
		self.op=op
		self.left=left
		self.right=right

	def __str__(self):
		return "binary("+str(self.op)+" "+str(self.left)+" "+str(self.right)+")"
	#token_type op
	#expression *left, *right

class subscript(expression):
	def __init__(self, array, indices):
		super(subscript, self).__init__()
		self.expression=subscript_node
		self.array=array
		self.indices=indices

	def __str__(self):
		return "subscript("+str(self.array)+" "+str(list(map(str,self.indices)))+")"
	#expression *array
	#std::vector<expression*> indices

class call(expression):
	def __init__(self, function, args):
		super(call, self).__init__()
		self.type=call_node
		self.expression=call_node
		self.function=function
		self.args=args

	def __str__(self):
		return "call("+str(self.function)+" "+str(list(map(str,self.args)))+")"
	#value *function
	#std::vector<expression*> args

class statement(node):
	def __init__(self, type=None):
		super(statement, self).__init__()
		self.node=type

class statement_error(statement):
	def __init__(self):
		super(statement_error, self).__init__()
		self.statement=statement_error_node

class assignment(statement):
	def __init__(self, op, lvalue, rvalue):
		super(assignment, self).__init__()
		self.statement=assignment_node
		self.op=op
		self.lvalue=lvalue
		self.rvalue=rvalue

	def __str__(self):
		return "assign("+str(self.lvalue)+" "+str(self.op)+" "+str(self.rvalue)+")"
		#return "assignment("+str(self.lvalue)+" "+str(self.op)+" "+str(self.rvalue)+")"
	#token_type op
	#expression *lvalue, *rvalue

class invocation(statement):
	def __init__(self, c):
		super(invocation, self).__init__()
		self.statement=invocation_node
		self.c=c

	def __str__(self):
		return "invocation("+str(self.c)+")"
	#call *c

class declaration(statement):
	def __init__(self, types, names):
		super(declaration, self).__init__()
		self.statement=declaration_node
		self.types=types
		self.names=names

	def __str__(self):
		return "declaration("+str(list(map(lambda x:x.namekey,self.types)))+" "+str(list(map(str,self.names)))+")"
		#return "declaration("+str(self.type)+" "+str(list(map(str,self.names)))+")"
	#token type
	#std::vector<value*> names

class block(statement):
	def __init__(self, stmts, s=True):
		super(block, self).__init__()
		self.statement=block_node
		self.s=s
		self.stmts=stmts

	def __str__(self):
		if self.s:
			stri="block{\n"
		else:
			stri="nblock{\n"
		for x in self.stmts:
			for z  in str(x).split("\n"):
				stri+="  "+z+"\n"
		stri+="}"
		return stri
		#return "block("+str(list(map(str,self.stmts)))+")"
	#std::vector<statement*> stmts

class ifstatement(statement):
	def __init__(self, cond, branch_true, branch_false):
		super(ifstatement, self).__init__()
		self.statement=ifstatement_node
		self.cond=cond
		self.branch_true=branch_true
		self.branch_false=branch_false

	def __str__(self):
		return "if("+str(self.cond)+" "+str(self.branch_true)+" "+str(self.branch_false)+")"
	#expression *cond
	#statement *branch_true, *branch_false

class whilestatement(statement):
	def __init__(self, cond, stmt):
		super(whilestatement, self).__init__()
		self.statement=whilestatement_node
		self.cond=cond
		self.stmt=stmt

	def __str__(self):
		return "while("+str(self.cond)+" "+str(self.stmt)+")"
	#expression *cond
	#statement *stmt

class dostatement(statement):
	def __init__(self, cond, stmt):
		super(dostatement, self).__init__()
		self.statement=dostatement_node
		self.cond=cond
		self.stmt=stmt

	def __str__(self):
		return "do("+str(self.cond)+" "+str(self.stmt)+")"
	#expression *cond
	#statement *stmt

class repeatstatement(statement):
	def __init__(self, expr, stmt):
		super(repeatstatement, self).__init__()
		self.statement=repeatstatement_node
		self.expr=expr
		self.stmt=stmt

	def __str__(self):
		return "repeat("+str(self.expr)+" "+str(self.stmt)+")"
	#expression *expr
	#statement *stmt

class forstatement(statement):
	def __init__(self, init, cond, inc, stmt):
		super(forstatement, self).__init__()
		self.statement=forstatement_node
		self.init=init
		self.cond=cond
		self.inc=inc
		self.stmt=stmt

	def __str__(self):
		return "for("+str(self.init)+" "+str(self.cond)+" "+str(self.inc)+" "+str(self.stmt)+")"
	#statement *init
	#expression *cond
	#statement *inc
	#statement *stmt

class switchstatement(statement):
	def __init__(self, expr, stmts):
		super(switchstatement, self).__init__()
		self.statement=switchstatement_node
		self.expr=expr
		self.stmts=stmts

	def __str__(self):
		return "switch("+str(self.expr)+" "+str(self.stmts)+")"
	#expression *expr
	#block *stmts

class withstatement(statement):
	def __init__(self, expr, stmt):
		super(withstatement, self).__init__()
		self.statement=withstatement_node
		self.expr=expr
		self.stmt=stmt

	def __str__(self):
		return "with("+str(self.expr)+" "+str(self.stmt)+")"
	#expression *expr
	#statement *stmt

class jump(statement):
	def __init__(self, type):
		super(jump, self).__init__()
		self.statement=jump_node
		self.type=type

	def __str__(self):
		return "jump("+str(self.type)+")"
	#token_type type

class returnstatement(statement):
	def __init__(self, expr):
		super(returnstatement, self).__init__()
		self.statement=returnstatement_node
		self.expr=expr

	def __str__(self):
		return "return("+str(self.expr)+")"
	#expression *expr

class casestatement(statement):
	def __init__(self, expr):
		super(casestatement, self).__init__()
		self.statement=casestatement_node
		self.expr=expr

	def __str__(self):
		return "case("+str(self.expr)+")"
	#expression *expr
