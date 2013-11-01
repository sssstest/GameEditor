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

class GameInformation(GameResource):
	defaults={"id":-1,"backgroundcolor":(255<<16) | (255<<8) | 255,#BuildColor(255, 255, 225)),
	"showInSeperateWindow":True,"caption":"Game Information","left":-1,
	"top":-1,"width":600,"height":400,"showborder":True,"sizeable":True,
	"alwaysontop":False,"freeze":True,"information":"""{\\rtf1\\ansi\\ansicpg1252\\deff0\\deflang1033
					  {\\fonttbl{\\f0\\fnil Arial;}}{\\colortbl ;\\red0\\green0\\blue0;}
					  \\viewkind4\\uc1\\pard\\cf1\\f0\\fs24}"""}

	def __init__(self, gameFile):
		GameResource.__init__(self, gameFile, -1)

	def ReadEgm(self, gmkfile, entry, z):
		stream=z.open(entry+".ey",'r')
		y=YamlParser()
		r=y.parseStream(stream)
		self.setMember("backgroundcolor",r.getMhex('BACKGROUND_COLOR'))
		self.setMember("showInSeperateWindow",r.getMbool('MIMIC_GAME_WINDOW'))#clifix
		self.setMember("caption",r.getMstr('FORM_CAPTION'))
		self.setMember("left",r.getMint('LEFT'))
		self.setMember("top",r.getMint('TOP'))
		self.setMember("width",r.getMint('WIDTH'))
		self.setMember("height",r.getMint('HEIGHT'))
		self.setMember("showborder",r.getMbool('SHOW_BORDER'))
		self.setMember("sizeable",r.getMbool('ALLOW_RESIZE'))
		self.setMember("alwaysontop",r.getMbool('STAY_ON_TOP'))
		self.setMember("freeze",r.getMbool('PAUSE_GAME'))
		data=r.getMstr("Data")
		information=z.open(data, "rU").read()
		self.setMember("information", information)

	def ReadGmk(self, stream):
		gameInfoStream = stream.Deserialize()
		self.setMember("backgroundcolor",gameInfoStream.ReadDword())
		self.setMember("showInSeperateWindow",gameInfoStream.ReadBoolean())
		self.setMember("caption",gameInfoStream.ReadString())
		self.setMember("left",gameInfoStream.readInt32())
		self.setMember("top",gameInfoStream.readInt32())
		self.setMember("width",gameInfoStream.ReadDword())
		self.setMember("height",gameInfoStream.ReadDword())
		self.setMember("showborder",gameInfoStream.ReadBoolean())
		self.setMember("sizeable",gameInfoStream.ReadBoolean())
		self.setMember("alwaysontop",gameInfoStream.ReadBoolean())
		self.setMember("freeze",gameInfoStream.ReadBoolean())
		gameInfoStream.ReadTimestamp()
		self.setMember("information",gameInfoStream.ReadString())
		#Background Color of Game Information
		if len(self.getMember("information"))>4000:
			print_warning("game information too big "+str(len(self.getMember("information"))))
			self.setMember("information","")

	def WriteGmk(self, stream):
		gameInfoStream = BinaryStream()
		gameInfoStream.writeUInt32(self.getMember("backgroundcolor"))
		gameInfoStream.WriteBoolean(self.getMember("showInSeperateWindow"))
		gameInfoStream.WriteString(self.getMember("caption"))
		gameInfoStream.WriteDword(self.getMember("left"))
		gameInfoStream.WriteDword(self.getMember("top"))
		gameInfoStream.WriteDword(self.getMember("width"))
		gameInfoStream.WriteDword(self.getMember("height"))
		gameInfoStream.WriteBoolean(self.getMember("showborder"))
		gameInfoStream.WriteBoolean(self.getMember("sizeable"))
		gameInfoStream.WriteBoolean(self.getMember("alwaysontop"))
		gameInfoStream.WriteBoolean(self.getMember("freeze"))
		gameInfoStream.WriteTimestamp()
		gameInfoStream.WriteString(self.getMember("information"))
		stream.Serialize(gameInfoStream)

	def SaveEgm(self, gmkfile, z):
		ey = "Data: Game Information.rtf\n"
		ey += "BACKGROUND_COLOR: "+hex(self.getMember("backgroundcolor"))+"\n"
		ey += "MIMIC_GAME_WINDOW: "+boolToEgmBool(self.getMember("showInSeperateWindow"))+"\n"
		ey += "FORM_CAPTION: "+self.getMember("caption")+"\n"
		ey += "LEFT: "+str(self.getMember("left"))+"\n"
		ey += "TOP: "+str(self.getMember("top"))+"\n"
		ey += "WIDTH: "+str(self.getMember("width"))+"\n"
		ey += "HEIGHT: "+str(self.getMember("height"))+"\n"
		ey += "SHOW_BORDER: "+boolToEgmBool(self.getMember("showborder"))+"\n"
		ey += "ALLOW_RESIZE: "+boolToEgmBool(self.getMember("sizeable"))+"\n"
		ey += "STAY_ON_TOP: "+boolToEgmBool(self.getMember("alwaysontop"))+"\n"
		ey += "PAUSE_GAME: "+boolToEgmBool(self.getMember("freeze"))+"\n"
		z.writestr("Game Information.ey", ey)
		z.writestr("Game Information.rtf", self.getMember("information"))

	def WriteGGG(self):
		stri="@gameinformation {\n"
		for key in self.members:
			if not self.ifDefault(key):
				if key != "information":
					stri+="\t"+key+"="+str(self.getMember(key))+"\n"
		stri+="\t@information {\n"+str(self.getMember("information"))+"}\n"
		stri+="}\n"
		return stri
