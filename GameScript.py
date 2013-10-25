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

class GameScript(GameResource):
	defaults={"id":-1,"name":"noname","value":""}

	def __init__(self, gameFile, id):
		GameResource.__init__(self, gameFile, id)
		self.setMember("name","script_"+str(id))

	def ReadEgm(self, gmkfile, entry, z):
		stream=z.open(entry+".ey",'r')
		y=YamlParser()
		r=y.parseStream(stream)
		self.setMember("name",os.path.split(entry)[1])
		self.setMember("value",z.open(os.path.split(entry)[0]+"/"+r.getMstr('Data'),'r').read())

	def ReadGmx(self, gmkfile, gmxdir, name):
		self.setMember("name",os.path.splitext(name)[0])
		self.setMember("value",open(os.path.join(gmxdir,name),"r").read())

	def ReadGmk(self, stream):
		scriptStream = stream.Deserialize()
		if not scriptStream.ReadBoolean():
			self.exists = False
			return
		self.setMember("name",scriptStream.ReadString())
		scriptStream.ReadTimestamp()
		scriptStream.ReadDword()
		self.setMember("value",scriptStream.ReadString())
		self.exists = True

	def WriteGmk(self, stream):
		scriptStream = BinaryStream()
		scriptStream.WriteBoolean(self.exists)
		if self.exists:
			scriptStream.WriteString(self.getMember("name"))
			scriptStream.WriteTimestamp()
			scriptStream.WriteDword(800)
			scriptStream.WriteString(self.getMember("value"))
		stream.Serialize(scriptStream)

	def WriteGGG(self):
		stri="@script "+self.getMember("name")+" {\n"
		for x in self.getMember("value").split("\n"):
			stri+="\t"+x+"\n"
		stri+="}\n"
		return stri

	def WriteESScript(self):
		obj=ESScript()
		obj.name=self.getMember("name").encode()
		obj.id=self.getMember("id")
		obj.code=self.getMember("value").encode()
		return obj
