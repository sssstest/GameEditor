#!/usr/bin/env python

#@section License
#
#Copyright (C) 2013 ssss
#This file is a part of the GameEditor.
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program. If not, see <http://www.gnu.org/licenses/>.

from GameResource import *

class GameShader(GameResource):
	defaults={"id":-1,"name":"noname","vertex":"","fragment":"","type":"GLSL","precompile":False}

	def __init__(self, gameFile, id):
		GameResource.__init__(self, gameFile, id)
		self.setMember("name","shader_"+str(id))

	def ReadEgm(self, gmkfile, entry, z):
		stream=z.open(entry+".ey",'r')
		y=YamlParser()
		r=y.parseStream(stream)
		self.setMember("name",os.path.split(entry)[1])
		self.setMember("vertex",z.open(os.path.split(entry)[0]+"/"+r.getMstr('vertex'),'r').read().decode())
		self.setMember("fragment",z.open(os.path.split(entry)[0]+"/"+r.getMstr('fragment'),'r').read().decode())
		self.setMember("type",r.getMstr('type'))
		self.setMember("precompile",r.getMbool('precompile'))

	def WriteGGG(self):
		stri="@shader "+self.getMember("name")+" {\n"
		for key in ["name","id","type","precompile"]:
			if not self.ifDefault(key):
				stri+="\t"+key+"="+str(self.getMember(key))+"\n"
		stri+="\t@vertex {\n"
		for x in self.getMember("vertex").split("\n"):
			stri+="\t\t"+x+"\n"
		stri+="\t}\t@fragment {\n"
		for x in self.getMember("fragment").split("\n"):
			stri+="\t\t"+x+"\n"
		stri+="\t}\n"
		stri+="}\n"
		return stri

	def WriteESShader(self):
		obj=ESShader()
		obj.name=self.getMember("name").encode()
		obj.id=self.getMember("id")
		obj.vertex=self.getMember("vertex").encode()
		obj.fragment=self.getMember("fragment").encode()
		obj.type=self.getMember("type").encode()
		obj.precompile=self.getMember("precompile")
		return obj
