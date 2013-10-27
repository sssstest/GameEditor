#!/usr/bin/env python

from __future__ import print_function

class build_log():
	def append(self, c):
		print(c,end="")

	def message(self, c):
		print(c)

	def percent(self, i):
		print(i)

class error_printer():#error_stream
	def __init__(self, log):
		self.log=log
		self.errors = 0
		self.context = "<untitled>"

	def set_context(self, c):
		self.context = c

	def count(self):
		return self.errors

	def error(self, e):
		s	= self.context + ":" + str(e.unexpected.row) + ":" + str(e.unexpected.col) + ": " + "error: unexpected '" +str(e.unexpected) + "'; expected "
		if e.expected:
			s += e.expected
		else:
			s += e.expected_token
		s += "\n"

		self.log.append(s)
		self.log.append(self.parser.lexer.source.split("\n")[e.unexpected.row-1]+"\n")
		self.log.append(" "*(e.unexpected.col-1)+"^\n")
		self.errors+=1
		raise 1

	def error_string(self, e):
		self.log.append(e)
		self.errors+=1

	def progress(i, n = ""):
		self.log.percent(i)
		if not n.empty():
			self.log.message(n)

	def compile(self, target, source, log):
		errors = error_printer(log)

		return linker(source, getHostTriple(), errors).build(target)
