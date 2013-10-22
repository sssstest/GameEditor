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

class GameIncludeFile(GameResource):
	#ExportKind
	EkDont=0
	EkTempDirectory=1
	EkWorkingDirectory=2
	EkFollowingFolder=3

	defaults={"id":-1,"name":"noname","filename":"","filepath":"","originalFile":False,"originalFileSize":0,"data":None,
	"exportKind":EkDont,"exportPath":"","overwrite":False,"freeMemory":True,"removeAtEndOfGame":True}

	def __init__(self, gameFile, id):
		GameResource.__init__(self, gameFile, id)

	def WriteGGG(self):
		stri="@includefile {\n"
		for key in self.members:
			if not self.ifDefault(key):
				if key != "data":
					try:
						stri+="\t"+key+"="+str(self.getMember(key))+"\n"
					except:
						print_error("exception "+key)
		stri+="\t@data {\n"+str(self.getMember("data").EncodeBase64().decode())+"}\n"
		stri+="}\n"
		return stri

	def WriteGmk(self, stream):
		includeFileStream = BinaryStream()
		includeFileStream.WriteTimestamp()
		includeFileStream.WriteDword(800)
		includeFileStream.WriteString(self.getMember("filename"))
		includeFileStream.WriteString(self.getMember("filepath"))
		includeFileStream.WriteBoolean(self.getMember("originalFile"))
		includeFileStream.WriteDword(self.getMember("originalFileSize"))
		if self.getMember("data"):
			includeFileStream.WriteBoolean(True)
			includeFileStream.Serialize(self.getMember("data"), False)
		else:
			includeFileStream.WriteBoolean(False)
		includeFileStream.WriteDword(self.getMember("exportKind"))
		includeFileStream.WriteString(self.getMember("exportPath"))
		includeFileStream.WriteBoolean(self.getMember("overwrite"))
		includeFileStream.WriteBoolean(self.getMember("freeMemory"))
		includeFileStream.WriteBoolean(self.getMember("removeAtEndOfGame"))
		stream.Serialize(includeFileStream)

	def ReadGmk(self, stream):
		includeFileStream = stream.Deserialize()
		includeFileStream.ReadTimestamp()
		includeFileStream.ReadDword()
		self.setMember("filename",includeFileStream.ReadString())
		self.setMember("filepath",includeFileStream.ReadString())
		self.setMember("originalFile",includeFileStream.ReadBoolean())
		self.setMember("originalFileSize",includeFileStream.ReadDword())
		if includeFileStream.ReadBoolean():
			self.setMember("data", includeFileStream.Deserialize(False))
		self.setMember("exportKind",includeFileStream.ReadDword())
		self.setMember("exportPath",includeFileStream.ReadString())
		self.setMember("overwrite",includeFileStream.ReadBoolean())
		self.setMember("freeMemory",includeFileStream.ReadBoolean())
		self.setMember("removeAtEndOfGame",includeFileStream.ReadBoolean())
