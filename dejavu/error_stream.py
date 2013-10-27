#!/usr/bin/env python

class unexpected_token_error():
	def __init__(self, unexpected, expected):
		self.unexpected=unexpected
		self.expected=expected#str
		self.expected_token=expected#token_type

# todo: lexer errors
# todo: codegen errors
# todo: linker errors

class error_stream():
	def set_context(e):
		1
	def count():
		1
	def error(self, e):
		1
	def progress(self, i, e):
		1
