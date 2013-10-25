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

class GameMoment(object):
	def __init__(self):
		self.position=0
		actions=[]

class GameTimeline(GameResource):
	defaults={"id":-1,"name":"noname"}

	def __init__(self, gameFile, id):
		GameResource.__init__(self, gameFile, id)
		self.moments=[]

	def addMoment(self, point):
		self.moments.append(point)
		for callBack in self.listeners:
			callBack("subresource","moments",None,None)

	def ReadGmx(self, gmkfile, gmxdir, name):
		print_warning("gmx timeline unsupported")

	def ReadGmk(self, stream):
		timelineStream = stream.Deserialize()
		if not timelineStream.ReadBoolean():
			self.exists = False
			return
		self.setMember("name",timelineStream.ReadString())
		timelineStream.ReadTimestamp()
		timelineStream.ReadDword()
		count = timelineStream.ReadDword()
		for i in range(count):
			moment=GameMoment()
			moment.position = timelineStream.ReadDword()
			timelineStream.ReadDword()
			actionCount = timelineStream.ReadDword()
			for i in range(actionCount):
				action = GameAction(self.gameFile)
				action.Read(timelineStream)
				moment.actions.append(action)
			self.addMoment(moment)

	def WriteGmk(self, stream):
		timelineStream = BinaryStream()
		timelineStream.WriteBoolean(self.exists)
		timelineStream.WriteString(self.getMember("name"))
		timelineStream.WriteTimestamp()
		timelineStream.WriteDword(500)
		timelineStream.WriteDword(len(self.moments))
		for i in range(len(self.moments)):
			timelineStream.WriteDword(self.moments[i].position)
			timelineStream.WriteDword(400)
			timelineStream.WriteDword(len(self.moments[i].actions))
			for j in len(self.moments[i].actions):
				moments[i].actions[j].WriteGmk(timelineStream)
		stream.Serialize(timelineStream)

	def WriteGGG(self):
		stri="@timeline "+self.getMember("name")+" {\n"
		for o in self.moments:
			stri=stri+tabStringLines(o.WriteGGG())
		stri+="}\n"
		return stri

	def WriteESTimeline(self):
		obj=ESTimeline()
		print_warning("ES timeline unsupported")
		return obj

	def Finalize(self):
		for i in range(len(self.moments)):
			for j in len(self.moments[i].actions):
				self.moments[i].actions[j].Finalize()
