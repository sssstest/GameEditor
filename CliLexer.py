#!/usr/bin/env python

#* some lexer code converted to python from https://github.com/enigma-dev/NaturalGM/blob/master/Source/Classes/Lexers/QsciLexerGML.cpp

#* @file QsciLexerGML.cpp
#* @breif Declares the GML lexer for QScintilla.
#*
#* @section License
#*
#* Copyright (C) 2013 Daniel Hrabovcak and Robert B. Colton
#* This file is a part of the Natural GM IDE.
#*
#* This program is free software: you can redistribute it and/or modify
#* it under the terms of the GNU General Public License as published by
#* the Free Software Foundation, either version 3 of the License, or
#* (at your option) any later version.
#*
#* This program is distributed in the hope that it will be useful,
#* but WITHOUT ANY WARRANTY; without even the implied warranty of
#* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#* GNU General Public License for more details.
#*
#* You should have received a copy of the GNU General Public License
#* along with this program. If not, see <http://www.gnu.org/licenses/>.

def GMLLexer(source,endCharacter=","):
	word = ""
	line = ""
	list = source.split("\n")
	level=0
	plevel=0
	Default=0
	String1=1
	String2=2
	Number=3
	Comment1=11
	Comment2=12
	type = Default
	totali=0
	i=0
	for line in list:
		totali+=i+1
		i = 0
		if type == Comment2:
			type = Default
		while i < len(line):
			if line[i] == '"':
				if type == Default:
					type = String2
					word = '"'
				elif type == String2:
					word = ""
					type = Default
				else:
					word += '"'
			elif line[i] == "'":
				if type == Default:
					type = String1
					word = "'"
				elif type == String1:	
					word = ""
					type = Default
				else:
					word += "'";
			elif type == Default and line[i] == "/":
				if line[i+1] == "*":
					type = Comment1
					word = ""
					i+=1
				elif line[i+1] == "/":
					type = Comment2
					word = ""
					i+=1
				else:
					word += line[i]
			elif type == Comment1 and line[i:i+2] == "*/":
				type = Default
				i+=1
			elif type == Default and line[i] == "{":
				level+=1
			elif type == Default and line[i] == "}":
				level-=1
				if level==-1:
					return totali+i,level,plevel,type
			elif type == Default and line[i] == "(":
				plevel+=1
			elif type == Default and line[i] == ")":
				plevel-=1
			elif endCharacter and type == Default and level == 0 and plevel == 0 and line[i] == endCharacter:
				return totali+i,level,plevel,type
			else:
				word += line[i]
			i+=1
	return totali+i,level,plevel,type

def GMLSplitArguments(source):
	i=0
	arguments=[]
	sources=source
	while sources:
		sources=sources[i:]
		i,level,plevel,type=GMLLexer(sources)
		if level != 0 or plevel != 0:
			return "unmatched "+sources[:i],[]
		arguments.append(sources[:i-1])
		if i>=len(sources):
			return "",arguments
	return "",[]