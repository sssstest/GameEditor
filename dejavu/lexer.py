#!/usr/bin/env python

import re
from tokens import *

class token():
	def __init__(self, t, r, c):
		self.type=t
		self.row=r
		self.col=c

	def __str__(self):
		if self.type==real:
			return "real("+str(self.real)+")"
		if self.type==name:
			return "name("+str(self.namekey)+")"
		if self.type==string:
			return "string("+str(self.stringkey)+")"
		return "token("+str(self.type)+")"
		#return "token("+str(self.type)+" "+str(self.row)+" "+str(self.col)+")"

	#token_type type
	#size_t row, col

	#union {
	#	double real
	#	struct {
	#		size_t length
	#		const char *data
	#	} string
	#}

def isspace(c):
	return c == ' ' or c == '\t' or c == '\n' or c == '\r'

def isnewline(c):
	return c == '\n' or c == '\r'

def isnamestart(c):
	return c == '_' or ('a' <= c and c <= 'z') or ('A' <= c and c <= 'Z')
	#return ('a' <= c and c <= 'z') or ('A' <= c and c <= 'Z')

def isname(c):
	return c == '_' or isnamestart(c) or isdigit(c)

def isoperator(c):
	if c in '{}()[].,:;+-*/|&^~=<>?!':
		return True

	return False

def isdigit(c):
	return '0' <= c and c <= '9'

keywords={}

keywords["begin"] = l_brace
keywords["end"] = r_brace
keywords["not"] = exclaim
keywords["and"] = ampamp
keywords["or"] = pipepipe
keywords["xor"] = caretcaret

def KEYWORD(X):
	keywords[X] = "kw_"+X

KEYWORD("div")
KEYWORD("mod")

KEYWORD("true")
KEYWORD("false")

KEYWORD("self")
KEYWORD("other")
KEYWORD("all")
KEYWORD("noone")
KEYWORD("global")
KEYWORD("local")

KEYWORD("globalvar")
KEYWORD("var")

KEYWORD("unsigned")

KEYWORD("if")
KEYWORD("then")
KEYWORD("else")
KEYWORD("repeat")
KEYWORD("while")
KEYWORD("do")
KEYWORD("until")
KEYWORD("for")
KEYWORD("switch")
KEYWORD("with")
KEYWORD("case")
KEYWORD("default")
KEYWORD("break")
KEYWORD("continue")
KEYWORD("exit")
KEYWORD("return")

class token_stream():
	def __init__(self, b):
		self.row=1
		self.col=1
		self.source=b
		self.current=0
		self.buffer_end=len(b)

	def backup(self):
		self.current=self.backup_current
		self.row=self.backup_row
		self.col=self.backup_col

	# todo: potential cleanup/optimization with a switch statement
	def gettoken(self):
		self.backup_current=self.current
		self.backup_row=self.row
		self.backup_col=self.col
		
		self.skipwhitespace()

		# eof
		if self.current == self.buffer_end:
			return token(eof, self.row, self.col)
		# skip comments
		# todo: can we pull this out into a helper function?
		# the control flow interacts weirdly with whitespace and division
		if self.source[self.current] == '/':
			# don't increment current yet, it might be a / token

			# single-line comment
			if self.source[self.current + 1] == '/':
				self.current+=1
				self.current+=1
				while self.current != self.buffer_end and not isnewline(self.source[self.current]):
					self.current+=1
					#continue

			# multi-line comment
			elif self.source[self.current + 1] == '*':
				self.current += 2
				self.col += 2

				while (
					(self.source[self.current] != '*' or self.source[self.current+1] != '/') and
					(self.current + 1 != self.buffer_end)
				):
					self.current+=1
					self.col+=1
					if isnewline(self.source[self.current]):
						self.skipnewline()

				self.current+=2
				self.col+=2
			# division token
			else:
				return self.getoperator()

			return self.gettoken()

		if isnamestart(self.source[self.current]):
			return self.getname()

		if (
			isoperator(self.source[self.current]) and

			# we need a special case for stupid numbers like .25
			(self.source[self.current] != '.' or not isdigit(self.source[self.current + 1]))
		):
			return self.getoperator()

		if isdigit(self.source[self.current]) or self.source[self.current] == '$' or self.source[self.current] == '.':
			return self.getnumber()

		if self.source[self.current] == '"' or self.source[self.current] == '\'':
			return self.getstring()

		# eof
		if self.current == self.buffer_end:
			return token(eof, self.row, self.col)

		# error
		self.col+=1
		u = token(unexpected, self.row, self.col)
		u.stringdata = self.current+1
		self.current+=1
		u.stringlength = 1
		return u

	# skips any whitespace at the current position
	def skipwhitespace(self):
		while self.current != self.buffer_end and isspace(self.source[self.current]):
			if self.source[self.current] == '\t':
				self.col += 4
			elif isnewline(self.source[self.current]):
				self.skipnewline()
			else:
				self.col += 1
			self.current+=1

	# skips a newline at the current position
	# does NOT update current for single-char newlines
	# if there's no newline, behavior is undefined
	def skipnewline(self):
		self.row += 1
		self.col = 1

		if self.source[self.current] == '\r' and self.source[self.current + 1] == '\n':
			self.current+=1

	# returns the name or keyword at the current position
	# if there is none, behavior is undefined
	def getname(self):
		t = token(name, self.row, self.col)
		t.stringdata = self.current

		while isname(self.source[self.current]):
			self.current+=1
		t.stringlength = self.current - t.stringdata

		self.col += t.stringlength

		# todo: figure out a better way than constructing an std::string?
		key = self.source[t.stringdata:t.stringdata+t.stringlength]
		t.namekey=key
		if key in ["char","short","int","bool","float","double","unsigned","signed","uint","const","variant"]:#"string"
			key="var"

		if keywords.has_key(key):
			t.type = keywords[key]

		return t

	# returns the operator token at the current position
	# if there is none, behavior is undefined
	def getoperator(self):
		t = token(unexpected, self.row, self.col)

		# todo: can we use tokens.tbl here for maintainability? it just
		# needs to be put in the right order for e.g. a regex parser
		self.col+=1
		c = self.source[self.current]
		self.current+=1
		if c=='{':
			t.type = l_brace
			return t
		elif c=='}':
			t.type = r_brace
			return t
		elif c=='(': 
			t.type = l_paren
			return t
		elif c==')': 
			t.type = r_paren
			return t
		elif c=='[': 
			t.type = l_square
			return t
		elif c==']': 
			t.type = r_square
			return t

		elif c==',': 
			t.type = comma
			return t
		elif c=='.': 
			t.type = dot
			return t
		elif c==';': 
			t.type = semicolon
			return t
		elif c==':':
			ch=self.source[self.current]
			if ch=='=':
				self.col+=1
				self.current+=1
				t.type = equals
				return t
			else:
				t.type = colon
				return t

		elif c=='~': 
			t.type = tilde
			return t

		elif c=='=':
			ch=self.source[self.current]
			if ch=='=': 
				self.col+=1
				self.current+=1
				t.type = is_equals
				return t
			else:
				t.type = equals
				return t
		elif c=='!':
			ch=self.source[self.current]
			if ch=='=': 
				self.col+=1
				self.current+=1
				t.type = not_equals
				return t
			else:
				t.type = exclaim
				return t
		elif c=='<':
			ch=self.source[self.current]
			if ch=='<': 
				self.col+=1
				self.current+=1
				t.type = shift_left
				return t
			elif ch=='=':
				self.col+=1
				self.current+=1
				t.type = less_equals
				return t
			elif ch=='>':
				self.col+=1
				self.current+=1
				t.type = not_equals
				return t
			else:
				t.type = less
				return t
		elif c=='>':
			ch=self.source[self.current]
			if ch=='>':
				self.col+=1
				self.current+=1
				t.type = shift_right
				return t
			elif ch=='=':
				self.col+=1
				self.current+=1
				t.type = greater_equals
				return t
			else:
				t.type = greater
				return t
		elif c=='?':
			t.type = question
			return t
		elif c=='+':
			ch=self.source[self.current]
			if ch=='=':
				self.col+=1
				self.current+=1
				t.type = plus_equals
				return t
			elif ch=='+':
				self.col+=1
				self.current+=1
				t.type = plusplus
				return t
			else:
				t.type = plus
				return t
		elif c=='-':
			ch=self.source[self.current]
			if ch=='=':
				self.col+=1
				self.current+=1
				t.type = minus_equals
				return t
			elif ch=='-':
				self.col+=1
				self.current+=1
				t.type = minusminus
				return t
			else:
				t.type = minus
				return t
		elif c=='*':
			ch=self.source[self.current]
			if ch=='=':
				self.col+=1
				self.current+=1
				t.type = times_equals
				return t
			else:
				t.type = times
				return t
		elif c=='/':
			ch=self.source[self.current]
			if ch=='=':
				col+=1
				current+=1
				t.type = div_equals
				return t
			else:
				t.type = divide
				return t

		elif c=='&':
			ch=self.source[self.current]
			if ch=='=':
				self.col+=1
				self.current+=1
				t.type = and_equals
				return t
			elif ch=='&':
				self.col+=1
				self.current+=1
				t.type = ampamp
				return t
			else:
				t.type = bit_and
				return t
		elif c=='|':
			ch=self.source[self.current]
			if ch=='=':
				self.col+=1
				self.current+=1
				t.type = or_equals
				return t
			elif ch=='|':
				self.col+=1
				self.current+=1
				t.type = pipepipe
				return t
			else:
				t.type = bit_or
				return t
		elif c=='^':
			ch=self.source[self.current]
			if ch=='=':
				self.col+=1
				self.current+=1
				t.type = xor_equals
				return t
			elif ch=='^':
				self.col+=1
				self.current+=1
				t.type = caretcaret
				return t
			else:
				t.type = bit_xor
				return t

		else: return t

	# returns the number at the current position
	# if there is none, behavior is undefined
	def getnumber(self):
		t = token(real, self.row, self.col)

		if self.source[self.current] == '$':
			key = re.findall(r"(\d*)\D",self.source[self.current+1:])[0]
			t.real = int(key,16)#strtoul(current + 1, &end, 16)
		else:
			key = re.findall(r"([\d.]*)\D",self.source[self.current:])[0]
			if "." in key:
				t.real = float(key)
			else:
				t.real = int(key,10)#strtod(current, &end)
		endlen=len(key)
		self.col += endlen - self.current
		self.current += endlen

		return t

	# returns the string literal at the current position
	# GML makes this easy without escape sequences but we'll want them later
	# todo: error on unterminated strings
	def getstring(self):
		t = token(string, self.row, self.col)

		delim = self.source[self.current]
		self.current+=1
		self.col += 1

		t.stringdata = self.current
		while self.current != self.buffer_end and self.source[self.current] != delim:
			if isnewline(self.source[self.current]):
				self.skipnewline()

			self.current+=1
			self.col += 1
		t.stringlength = self.current - t.stringdata
		t.stringkey=self.source[t.stringdata:t.stringdata+t.stringlength]

		self.current+=1
		self.col += 1

		return t
