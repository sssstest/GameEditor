#!/usr/bin/env python

from __future__ import print_function
from .lexer import *
from .node import *
from .tokens import *
from .parser import *
import io

class printer(object):
	@staticmethod
	def toGML(p):
		global printf
		printf=io.StringIO()
		n=node_printer()
		n.visit(p.stmts[0])
		printf.seek(0)
		return printf.read()+"\n"

	@staticmethod
	def toGMLMinifier(p):
		global printf
		printf=io.StringIO()
		n=node_printer()
		n.minified=True
		n.visit(p.stmts[0])
		printf.seek(0)
		return printf.read()

def print_token(t):
	if t.type==unexpected:
		print(t.stringdata, end="", file=printf)

	elif t.type==name:
		print(t.namekey, end="", file=printf)

	elif t.type==real:
		print(t.real, end="", file=printf)

	elif t.type==string:
		print("\""+t.stringdata+"\"", end="", file=printf)

	elif t.type in OPERATORS:
		print(OPERATORS[t.type], end="", file=printf)

	else:
		if t.type.startswith("kw_"):
			print(t.type[3:], end="", file=printf)
		else:
			print(repr(t.type))
			raise 4

class node_printer(object):
	def __init__(self):
		self.scope=0
		self.precedence=0
		self.minified=False

	def visit(self, n):
		if type(n)==expression_error:
			self.visit_expression_error(n)
		elif type(n)==value:
			self.visit_value(n)
		elif type(n)==unary:
			self.visit_unary(n)
		elif type(n)==binary:
			self.visit_binary(n)
		elif type(n)==subscript:
			self.visit_subscript(n)
		elif type(n)==call:
			self.visit_call(n)
		elif type(n)==statement_error:
			self.visit_statement_errort(n)
		elif type(n)==assignment:
			self.visit_assignment(n)
		elif type(n)==invocation:
			self.visit_invocation(n)
		elif type(n)==declaration:
			self.visit_declaration(n)
		elif type(n)==block:
			self.visit_block(n)
		elif type(n)==ifstatement:
			self.visit_ifstatement(n)
		elif type(n)==whilestatement:
			self.visit_whilestatement(n)
		elif type(n)==dostatement:
			self.visit_dostatement(n)
		elif type(n)==repeatstatement:
			self.visit_repeatstatement(n)
		elif type(n)==forstatement:
			self.visit_forstatement(n)
		elif type(n)==switchstatement:
			self.visit_switchstatement(n)
		elif type(n)==withstatement:
			self.visit_withstatement(n)
		elif type(n)==jump:
			self.visit_jump(n)
		elif type(n)==returnstatement:
			self.visit_returnstatement(n)
		elif type(n)==casestatement:
			self.visit_casestatement(n)
		else:
			print(type(n))
			raise 4

	def visit_expression_error(self, e):
		print("<expression error>", end="", file=printf)

	def visit_value(self, v):
		if self.precedence >= 80 and v.t.type == real:
			print("(", end="", file=printf)
		print_token(v.t)
		if self.precedence >= 80 and v.t.type == real:
			print(")", end="", file=printf)

	def visit_unary(self, u):
		print_token(token(u.op, 0, 0))

		p = precedence
		self.precedence = 70

		self.visit(u.right)

		self.precedence = p

	def visit_binary(self, b):
		if symbols[b.op].precedence < self.precedence:
			print("(", end="", file=printf)
		p = self.precedence
		self.precedence = symbols[b.op].precedence

		self.visit(b.left);
		if b.op != dot:
			if not self.minified:
				print(" ", end="", file=printf)
		print_token(token(b.op, 0, 0))
		if b.op != dot:
			if not self.minified:
				print(" ", end="", file=printf)
		self.visit(b.right);

		self.precedence = p;
		if symbols[b.op].precedence < self.precedence:
			print(")", end="", file=printf)

	def visit_subscript(self, s):
		self.visit(s.array)
		print("[", end="", file=printf)

		p = precedence
		self.precedence = 0

		self.print_list(s.indices)

		self.precedence = p

		print("]", end="", file=printf)

	def visit_call(self, c):
		self.visit(c.function)
		print("(", end="", file=printf)
		self.print_list(c.args)
		print(")", end="", file=printf)

	def visit_statement_error(self, e):
		print("<statement error>", end="", file=printf)

	def visit_assignment(self, a):
		self.visit(a.lvalue)
		if not self.minified:
			print(" ", end="", file=printf)
		print_token(token(a.op, 0, 0))
		if not self.minified:
			print(" ", end="", file=printf)
		self.visit(a.rvalue)
		print(";", end="", file=printf)

	def visit_invocation(self, i):
		self.visit(i.c)
		print(";", end="", file=printf)

	def visit_declaration(self, d):
		print("var ", end="", file=printf)
		self.print_list(d.names)
		print(";", end="", file=printf)

	def visit_block(self, b):
		if not self.minified:
			print("{\n", end="", file=printf)
		else:
			print("{", end="", file=printf)
		self.scope+=1
		for it in b.stmts:
			if it.type == casestatement_node:
				self.scope-=1
			self.indent()
			self.visit(it)
			if not self.minified:
				print("\n", end="", file=printf)
			if it.type == casestatement_node:
				self.scope+=1
		self.scope-=1
		self.indent()
		print("}", end="", file=printf)

	def visit_ifstatement(self, i):
		if not self.minified:
			print("if (", end="", file=printf)
		else:
			print("if(", end="", file=printf)
		self.visit(i.cond)
		print(")", end="", file=printf)
		self.print_branch(i.branch_true)
		if i.branch_false:
			if not self.minified:
				print("\n", end="", file=printf)
			self.indent()
			print("else", end="", file=printf)

			if i.branch_false.type != ifstatement_node:
				if not self.minified:
					print("\n", end="", file=printf)
				self.print_branch(i.branch_false)
			else:
				print(" ", end="", file=printf)
				self.visit(i.branch_false)

	def visit_whilestatement(self, w):
		print("while (", end="", file=printf)
		self.visit(w.cond)
		print(")", end="", file=printf)
		self.print_branch(w.stmt)

	def visit_dostatement(self, d):
		print("do", end="", file=printf)
		self.print_branch(d.stmt);
		print(" until (", end="", file=printf)
		self.visit(d.cond)
		print(");", end="", file=printf)

	def visit_repeatstatement(self, r):
		if not self.minified:
			print("repeat (", end="", file=printf)
		else:
			print("repeat(", end="", file=printf)
		self.visit(r.expr)
		print(")", end="", file=printf)
		self.print_branch(r.stmt)

	def visit_forstatement(self, f):
		if not self.minified:
			print("for (", end="", file=printf)
		else:
			print("for(", end="", file=printf)
		self.visit(f.init)
		if not self.minified:
			print(" ", end="", file=printf)
		self.visit(f.cond)
		if not self.minified:
			print("; ", end="", file=printf)
		else:
			print(";", end="", file=printf)
		self.visit(f.inc)
		#print("\b", end="", file=printf)
		print(")", end="", file=printf)
		self.print_branch(f.stmt)

	def visit_switchstatement(self, s):
		print("switch (", end="", file=printf)
		self.visit(s.expr)
		print(")", end="", file=printf)
		self.print_branch(s.stmts)

	def visit_withstatement(self, w):
		print("with (", end="", file=printf)
		self.visit(w.expr)
		print(")", end="", file=printf)
		self.print_branch(w.stmt)

	def visit_jump(self, j):
		print_token(token(j.type, 0, 0))
		print(";", end="", file=printf)

	def visit_returnstatement(self, r):
		print("return ", end="", file=printf)
		self.visit(r.expr)
		print(";", end="", file=printf)

	def visit_casestatement(self, c):
		if c.expr:
			print("case ", end="", file=printf)
			self.visit(c.expr)
		else:
			print("default", end="", file=printf)

		print(":", end="", file=printf)

	def indent(self):
		if self.minified:
			return
		for i in range(0, self.scope):
			print("    ", end="", file=printf)

	def print_branch(self, s):
		if s.type == block_node:
			print(" ", end="", file=printf)
			self.visit(s)
		else:
			if not self.minified:
				print("\n", end="", file=printf)
			self.scope+=1
			self.indent()
			self.visit(s)
			self.scope-=1

	def print_list(self, l):
		a=0
		for it in l:
			if a != 0:
				print(", ", end="", file=printf)
			self.visit(it)
			a+=1
