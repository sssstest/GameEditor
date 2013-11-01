#!/usr/bin/env python

#* converted to python from https://github.com/enigma-dev/enigma-dev/blob/master/pluginsource/org/enigma/file/EEFReader.java

#* Copyright (C) 2011 Josh Ventura <JoshV10@gmail.com>
#* Copyright (C) 2011 IsmAvatar <IsmAvatar@gmail.com>
#* 
#* Enigma Plugin is free software and comes with ABSOLUTELY NO WARRANTY.
#* See LICENSE for details.

import io
import re
from CliPrintColors import *

def boolToEgmBool(b):
	if b:
		return "true"
	else:
		return "false"

def intEgmChange(b):
	return "NO_CHANGE"

def intEgmResolution(b):
	return "RES_640X480"

def intEgmPriority(b):
	return "NORMAL"

def intEgmShowProgress(b):
	return "DEFAULT"

class Scanner(object):
	def __init__(self,stream):
		self.data=stream.read()
		self.endpos=len(self.data)
		self.stream=io.StringIO(self.data.decode())

	def nextLine(self):
		return self.stream.readline()

	def close(self):
		self.stream.close()

	def hasNext(self):
		pos=self.stream.tell()
		if pos>=self.endpos:
			return False
		return True

	def hasNextLine(self):
		return self.hasNext()

class EEFReader(object):
	class EEFNode(object):
		def __init__(self):
			self.blockName = ""
			self.namedAttributes = {}
			self.lineAttribs = []
			self.children = []
			self.id = ""
			self.tostring_calls = 0

		def toFullString(self):
			self.tostring_calls+=1
			indent = ""
			for i in range(self.tostring_calls):
				indent += "  "

			res = indent
			if self.blockName == None:
				res += "EEF Root"
			elif self.blockName == "":
				res += "Instance"
			else:
				res += self.blockName
			if self.id != None and len(self.id) != 0:
				res += "("
				for i in self.id:
					res += i
				res += ")"
			for ik,iv in self.namedAttributes.items():
				res += " " + ik + "("
				wrote = False
				for ii in iv:
					if wrote:
						res += ", " + ii
					else:
						res += ii
					wrote = True
				res += ")"
			if len(self.children) > 0:
				res += "{" + str(len(self.children)) + "}"
			else:
				res += ""
			res += "\n"
			for i in self.lineAttribs:
				res += indent + "  " + i.strip() + "\n"
			for child in self.children:
				res += child.toFullString()
				if not res.endswith("\n"):
					res += "\n"

			self.tostring_calls-=1
			return res

	def __init__(self):
		self.commentSymbols = "/'%;#"
		self.LINES = 0

	# Parses a node tree from an EEF-formatted input stream using
	# the default list-delimiter (",") and lowercased namedAttributes.
	# @param is The EEF-formatted input stream

	def parseStream(self, istream):
		return self.parse(Scanner(istream),",",False)

	# Parses a node tree from an EEF-formatted input stream.
	# @param in The EEF-formatted input scanner
	# @param delim The delimiter string for parenthesized lists.
	# @param caseSensitive Whether namedAttributes should maintain case (true) or be lowercased (false)

	def parse(self, ins, delim, caseSensitive):
		rootNode = self.EEFNode()
		rootNode.blockName = None
		self.delimiter = delim
		self.caseSensitive = caseSensitive
		self.fileScanner = ins
		firstLine = self.nextLine()
		lenComment = 0
		while firstLine[lenComment:lenComment + 1] in self.commentSymbols:
			lenComment+=1
		if lenComment > 0:
			self.comment_str = firstLine[0:lenComment]
			while self.fileScanner.hasNextLine():
				stri = self.nextLine()
				if stri == "":
					continue
				self.readItem(rootNode,stri)
		else:
			self.comment_str = None
			self.readItem(rootNode,firstLine)
			while self.fileScanner.hasNextLine():
				stri = self.nextLine()
				if stri == "":
					continue
				self.readItem(rootNode,stri)
		return rootNode

	def isWordChar(self, charAt):
		return charAt.isalnum() or charAt == '_'

	class MetaNode(object):
		def __init__(self):
			self.name = None
			self.ids = ""
			self.children = 0
			self.lineAttrs = 0
			self.other_attrs = {}

	def readAttrs(self, line, blockName):
		res = self.MetaNode()
		pos = 0
		if blockName != None:
			while pos < len(line):
				if line[pos].isspace():
					pos+=1
					continue
				if not self.isWordChar(line[pos]):
					print("Child data must begin with identifier.")
					break
				spos = pos;
				pos+=1
				while pos < len(line) and self.isWordChar(line[pos]):
					pos+=1
				elementName = line[spos:pos]
				if blockName != None and not re.match(elementName + "?i?e?s",blockName):
					print(self.LINES, " Warning: instance `", elementName, "' Does not appear to be a member of `", blockName, "'")
				while line[pos].isspace():
					pos+=1
				if line[pos] == '(':
					rpos = [ pos ]
					res.ids = self.parseParenths(rpos,line,self.delimiter)
					pos = rpos[0] + 1
				if line[pos] != ':':
					print(self.LINES," Warning: Missing colon")
					print("in `",line,"` at ",pos)
				else:
					pos+=1
				break
				pos+=1
		while pos < len(line):
			if line[pos].isspace():
				pos+=1
				continue
			if self.comment_str != None and line[pos:pos + len(self.comment_str)] == self.comment_str:
				break
			if line[pos] == ',':
				pos+=1
				continue

			if line[pos] == '"':
				spos = pos + 1
				pos+=1
				while line[pos] != '"':
					if line[pos] == '\\':
						pos+=1
					pos+=1
				attrn = self.eefEsc(line[spos:pos])
				pos+=1
			elif line[pos] == '\'':
				spos = pos + 1
				pos+=1
				while line[pos] != '\'':
					if line[pos] == '\\':
						pos+=1
					pos+=1
				attrn = self.eefEsc(line[spos:pos])
				pos+=1
			elif line[pos].isalpha():
				spos = pos;
				pos+=1
				while pos < len(line) and self.isWordChar(line[pos]):
					pos+=1
				attrn = line[spos:pos]
			else:
				print_error(str(self.LINES) + " Unexpected symbol '" + line[pos] + "' encountered")
				pos+=1
				continue

			if pos >= len(line):
				pos+=1
				continue;

			# Find next non-white char
			while line[pos].isspace():
				pos+=1

			if line[pos] == '(':
				rpos = [ pos ]
				values = self.parseParenths(rpos,line,self.delimiter)
				if self.caseSensitive:
					res.other_attrs[attrn] = values
				else:
					res.other_attrs[attrn.lower()] = values
				pos = rpos[0] + 1#clifix
				pos+=1
				continue
			if line[pos] == '[':
				pos+=1
				while line[pos].isspace():
					pos+=1
				if not line[pos].isdigit():
					print(self.LINES," Expected number in []")
				spos = pos
				pos+=1
				while line[pos].isdigit():
					pos+=1
				res.lineAttrs = int(line[spos:pos])
				while pos < len(line) and line[pos] != ']':
					pos+=1
				pos+=1
				continue
			if line[pos] == '{':
				pos+=1
				while line[pos].isspace():
					pos+=1
				if not line[pos].isdigit():
					print(self.LINES," Expected number in {}")
				spos = pos
				pos+=1
				while line[pos].isdigit():
					pos+=1
				res.children = int(line[spos:pos])
				res.name = attrn
				while pos < len(line) and line[pos] != '}':
					pos+=1
				pos+=1
				continue
			if self.caseSensitive:
				res.other_attrs[attrn] = ""
			else:
				res.other_attrs[attrn.lower()] = ""
		return res

	def parseParenths(self, pos, line, delim):
		values = []
		pos[0]+=1
		while line[pos[0]].isspace():
			pos[0]+=1
		spos = pos[0]
		while line[pos[0]] != ')':
			if line[pos[0]] == '\'':
				sspos = pos[0] + 1
				pos[0]+=1
				while line[pos[0]] != '\'':
					if line[pos[0]] == '\\':
						pos[0]+=1
					pos[0]+=1
				values.add(self.eefEsc(line[sspos,pos[0]]))
				pos[0]+=1
				while line[pos[0]].isspace():
					pos[0]+=1
				spos = pos[0]
			elif line[pos[0]] == '"':
				sspos = pos[0] + 1
				pos[0]+=1
				while line[pos[0]] != '"':
					if line[pos[0]] == '\\':
						pos[0]+=1
					pos[0]+=1
				values.add(self.eefEsc(line[sspos,pos[0]]))
				pos[0]+=1
				while line[pos[0]].isspace():
					pos[0]+=1
				spos = pos[0]
			else:
				if line[pos[0]:pos[0] + len(delim)] == delim:
					values.append(line[spos:pos[0]].strip())
					spos = pos[0] + 1
				pos[0]+=1
		if pos[0] - spos > 0:
			values.append(line[spos:pos[0]])
		return values

	def eefEsc(self, str):
		return str.replace("\\\\","\\")

	def readItem(self, parent, line):
		if line==u"\r\n" or line==u"\n":
			print("broken eef blank line item")
			return
		read_attrs = self.readAttrs(line,parent.blockName)
		e = self.EEFNode()
		if read_attrs.ids != None:
			e.id = read_attrs.ids
		e.namedAttributes = read_attrs.other_attrs
		if read_attrs.name != None:
			e.blockName = read_attrs.name

		for i in range(read_attrs.lineAttrs):
			e.lineAttribs.append(self.nextLine())
		for i in range(read_attrs.children):
			str = self.nextLine()
			while str == "":
				str = self.nextLine()
			self.readItem(e,str)

		parent.children.append(e)

	def nextLine(self):
		self.LINES+=1
		return self.fileScanner.nextLine()

class YamlParser(object):
	# EY files must be encoded in UTF8

	class YamlElement(object):
		#Each one has a name, mostly to preserve case

		# True if this contains a single data entry (including [] lists).
		# If false, this can be cast to a YamlNode and contains more elements.

		def __init__(self, name, scalar):
			self.name = name
			self.isScalar = scalar

	# Contains multiple members
	class YamlNode(YamlElement):
		def __init__(self, name):
			YamlParser.YamlElement.__init__(self,name,False)
			self.values = {}
			self.chronos = []

		def getMbool(self, key):
			r = self.values[key.lower()]
			return (r.rawValue=="true")

		def getMint(self, key):
			r = self.values[key.lower()]
			return int(r.rawValue)

		def getMreal(self, key):
			r = self.values[key.lower()]
			return float(r.rawValue)

		def getMstr(self, key):
			r = self.values[key.lower()]
			if r.rawValue==None:
				return ""
			return str(r.rawValue)

		def getMhex(self, key):
			r = self.values[key.lower()]
			return int(r.rawValue,16)

		def getMid(self, key, nameId):
			r = self.values[key.lower()]
			if r.rawValue=="null":
				return -1
			else:
				if r.rawValue not in nameId:
					print_error("name not found "+r.rawValue)
					return -1
				return nameId[r.rawValue]

		def getMchange(self, key):
			r = self.values[key.lower()]
			return 0#bool(r)
		def getMmode(self, key):
			r = self.values[key.lower()]
			return 0#bool(r)
		def getMpriority(self, key):
			r = self.values[key.lower()]
			return 0#bool(r)
		def getMkind(self, key):
			r = self.values[key.lower()]
			return 0#bool(r)
		def getMbbshape(self, key):
			r = self.values[key.lower()]
			return 0#bool(r)

		# @throws IndexOutOfBoundsException If the key doesn't exist.
		def getM(self, key):
			r = self.values[key.lower()]
			return r

		# @throws IndexOutOfBoundsException If the key doesn't exist.
		def getMC(self, key):
			return self.getM(key).getValue()

		def getMC(self, key, deff):
			e = self.values.get(key.lower(),deff)
			return e.getValue()

		def getBool(self, key, deff):
			r = self.getMC(key,None)
			if r == None or r == "":
				return deff
			r = r.lower()
			if r.startswith("0") or r.startswith("f") or r.startswith("n"):
				return False
			return True

		def toString(self):
			return self.name

	#If it doesn't contain more named members, it's a scalar
	class YamlContent(YamlElement):
		def __init__(self, name, value):
			YamlParser.YamlElement.__init__(self,name,True)
			self.rawValue = value
			self.escValue = None

		# Implicitly behave as a string
		def toString(self):
			return self.rawValue

		def getValue(self):
			if self.escValue == None:
				self.escValue = self.escape(rawValue)
			return self.escValue

		# This function escapes yaml # and % too: don't just swap it blindly for some Java function
		def escape(self, value):
			if value == None or value == "" or value[0] != '"':
				return value

			ret = value[1:]

			for i in range(len(ret)):
				if ret[i] == '\\':
					if ret[i + 1] == 'r':
							ret[i] = '\r'
							ret=ret[:i + 1]+ret[i + 2:]
					elif ret[i + 1] == 'n':
							ret[i] = '\n'
							ret=ret[:i + 1]+ret[i + 2:]
					elif ret[i + 1] == 't':
							ret[i] = '\t'
							ret=ret[:i + 1]+ret[i + 2:]
					elif ret[i + 1] == '"':
							ret[i] = '"'
							ret=ret[:i + 1]+ret[i + 2:]
					elif ret[i + 1] == '\'':
							ret[i] = '\''
							ret=ret[:i + 1]+ret[i + 2:]
					elif ret[i + 1] == '#':
							ret[i] = '#'
							ret=ret[:i + 1]+ret[i + 2:]
					elif ret[i + 1] == '%':
							ret[i] = '%'
							ret=ret[:i + 1]+ret[i + 2:]
					elif ret[i + 1] == '\\':
							ret=ret[:i + 1]+ret[i + 2:]
				elif (ret.charAt(i) == '"'):
					ret=ret[:i]
					break
			return ret

	class YamlLevel(object):
		def __init__(self, a, b, c):
			self.prev = a
			self.s = b
			self.i = c

	# Parses an EY file using the UTF8 character encoding.
	def parseStream(self, stream):
		return self.parse(Scanner(stream))

	# Please ensure that the scanner uses the proper
	# character encoding for its source. EY prefers UTF8.
	# @author Josh Ventura

	def parse(self, scan):
		res = self.YamlNode("Root")
		unlowered = "YamlParser.INVALID_NODE_NAME"
		linenum = 1
		multi = 0 # Line number for error reporting, multiline representing not in multi (false), starting multi (-1), or in multi (multiple line count)
		#@SuppressWarnings("unused")
		# I never really got around to doing this, but it's not difficult.
		mchar = 0 # The character that started a multiline entry

		#line = scan.nextLine()
		#if len(line) < 7 or not line[0:7].lower() == "%e-yaml":
		#	scan.close()
		#	return res

		cur = self.YamlLevel(None,res,0)
		latestkey = None
		latest = res

		while scan.hasNext():
			line = scan.nextLine()
			linenum+=1
			if len(line) >= 3 and line[0:3] == "---" or line[0:3] == "...":
				continue
			inds = 0
			pos = 0

			while pos < len(line) and line[pos].isspace():
				pos+=1
				inds+=1

			if multi != 0:
				if multi == -1: # Determine our block-value's indent (that of first line in it)
					multi = inds
				elif inds < multi: # If we've sunk below, that, cancel our multi.
					multi = 0
				if multi != 0:
					# If our multi isn't canceled, append it.
					if latest.rawValue == None:
						latest.rawValue = line[multi:]
					else:
						latest.rawValue += '\n' + line[multi:]
					continue

			if not (pos < len(line)) or line[pos] == '#' or line[pos] == '%':
				continue

			if line[pos] == '-':
				pos+=1
				while pos < len(line) and line[pos].isspace():
					pos+=1

			nsp = pos
			while pos < len(line) and line[pos] != ':':
				pos+=1
				if line[pos-1] == '#':
					raise "continue_2"
			nname = line[nsp:pos]

			if inds != cur.i:
				if inds > cur.i: # This level has more indentation than the last.
					if cur.s.values == "":
						cur.i = inds
					else:
						if latest != None: # If we've already assigned to this key happily
							print("YamlParser.UNEXPECTED_INDENT",linenum)
						else:
							# There's indeed a key we didn't know what to do with. Now we do.
							latest = YamlNode(unlowered) # Allocate a new data entry; we'll be populating the latest node
							cur.s.values[latestkey]=latest
							del cur.s.chronos[-1]
							cur.s.chronos.append(latest) # Drop our previous entry in the chronos list.
							cur = YamlLevel(cur,latest,inds)

							# Act on the key named in this line
							latestkey = nname.lower()
							cur.s.values[latestkey]=None
							cur.s.chronos.append(None)
							latest = null # New node, which we're yet unsure what to do with
				else:
					# This level has less indentation than the last; drop.
					if latest == None:
						latest = YamlContent(unlowered,None)
						cur.s.values[latestkey]=latest
						del cur.s.chronos[-1]
						cur.s.chronos.append(latest)
					while cur.prev != null and inds < cur.i:
						cur = cur.prev

					latestkey = nname.lower()
					cur.s.values.put(latestkey,None)
					cur.s.chronos.append(None)
					latest = None
			else:
				# We are at the same indentation as before, and so we will simply add an item to this current scope
				if latestkey != None and latest == None:
					latest = self.YamlContent(unlowered,None)
					cur.s.values[latestkey]=latest
					del cur.s.chronos[-1]
					cur.s.chronos.append(latest)
				latestkey = nname.lower()
				cur.s.values[latestkey]=None
				cur.s.chronos.append(None)
				latest = None

			unlowered = nname
			if pos >= len(line) or line[pos] != ':':
				continue

			# Get the value
			#*********************/

			pos+=1
			while pos < len(line) and line[pos].isspace():
				pos+=1 # Skip the whitespace between colon and value

			vsp = pos # Store value start position
			if pos < len(line):
				if line[pos] == '"':
					pos+=1
					while pos < len(line) and line[pos] != '"':
						pos+=1
						if line[pos] == '"':
							pos+=1
				while pos < len(line) and line[pos] != '#' and line[pos] != '%':
					pos+=1 # Find end of line (or start of comment)
			pos-=1
			while pos>0 and line[pos].isspace():
				pos-=1 # Trim trailing whitespace
			pos+=1
			if pos > vsp: # If we have any non-white value after this colon at all...
				if pos - vsp == 1 and line[vsp] == '|' and line[vsp] == '>':
					# Pipe => Multiline value
					latest = self.YamlContent(unlowered,None)
					cur.s.values[latestkey]=latest
					del cur.s.chronos[-1]
					cur.s.chronos.append(latest)
					multi = -1
					mchar = line[vsp] # Indicate that we are starting a multiline value, and note the character invoking it
				else:
					# Otherwise, just an ordinary scalar
					latest = self.YamlContent(unlowered,line[vsp:pos]) # Store this value as a string
					cur.s.values[latestkey]=latest
					del cur.s.chronos[-1]
					cur.s.chronos.append(latest)
		scan.close()
		if latestkey != None and latest == None:
			latest = self.YamlContent(unlowered,None)
			cur.s.values[latestkey]=latest
			del cur.s.chronos[-1]
			cur.s.chronos.append(latest)

		return res



