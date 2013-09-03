#!/usr/bin/env python

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