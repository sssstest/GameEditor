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

class GamePath(GameResource):
	if Class:
		RoomIndexNone=-1

		#ConnectionKind
		KindStraight=0
		KindSmooth=1

	defaults={"id":-1,"name":"noname","connectionKind":KindStraight,"closed":True,"precision":4,"roomIndex":-1,"room":None,"snapX":16,"snapY":16}

	def __init__(self, gameFile, id):
		GameResource.__init__(self, gameFile, id)
		self.setMember("name","path_"+str(id))
		self.points=[]

	def setMember(self, member, value):
		GameResource.setMember(self, member, value)
		if not self.gameFile.readingFile:
			if member=="roomIndex":
				if value != GameObject.SpriteIndexNone:
					self.setMember("room", self.gameFile.GetResource(GameRoom, value))

	def addPoint(self, point):
		self.points.append(point)
		for callBack in self.listeners:
			callBack("subresource","points",None,None)

	def ReadGmx(self, gmkfile, gmxdir, name):
		print_warning("gmx path unsupported")

	def ReadGmk(self, stream):
		pathStream = stream.Deserialize()
		if not pathStream.ReadBoolean():
			self.exists = False
			return
		self.setMember("name",pathStream.ReadString())
		pathStream.ReadTimestamp()
		pathStream.ReadDword()
		self.setMember("connectionKind",pathStream.ReadDword())
		self.setMember("closed",pathStream.ReadBoolean())
		self.setMember("precision",pathStream.ReadDword())
		self.setMember("roomIndex",pathStream.ReadDword())
		self.setMember("snapX",pathStream.ReadDword())
		self.setMember("snapY",pathStream.ReadDword())
		count = pathStream.ReadDword()
		for i in range(count):#Point x,y,speed
			x = pathStream.readDouble()
			y = pathStream.readDouble()
			speed = pathStream.readDouble()

			self.addPoint((x,y,speed))

	def WriteGmk(self, stream):
		pathStream = BinaryStream()
		pathStream.WriteBoolean(self.exists)
		pathStream.WriteString(self.getMember("name"))
		pathStream.WriteTimestamp()
		pathStream.WriteDword(530)
		pathStream.WriteDword(self.getMember("connectionKind"))
		pathStream.WriteBoolean(self.getMember("closed"))
		pathStream.WriteDword(self.getMember("precision"))
		if self.getMember("room"):
			pathStream.WriteDword(self.room.getMember("id"))
		else:
			pathStream.WriteDword(GamePath.RoomIndexNone)
		pathStream.WriteDword(self.getMember("snapX"))
		pathStream.WriteDword(self.getMember("snapY"))
		pathStream.WriteDword(len(self.points))
		for i in range(len(self.points)):
			pathStream.WriteDouble(points[i][0])
			pathStream.WriteDouble(points[i][1])
			pathStream.WriteDouble(points[i][2])
		stream.Serialize(pathStream)

	def WriteGGG(self):
		stri="@path "+self.getMember("name")+" {\n"
		for key in self.members:
			if not self.ifDefault(key):
				stri+="\t"+key+"="+str(self.getMember(key))+"\n"
		for o in self.points:
			stri+="\t@point "+str(o[0])+","+str(o[1])+","+str(o[2])+"\n"
		stri+="}\n"
		return stri

	def WriteESPath(self):
		obj=ESPath()
		obj.name=self.getMember("name").encode()
		obj.id=self.getMember("id")
		obj.smooth=self.getMember("connectionKind")
		obj.closed=self.getMember("closed")
		obj.precision=self.getMember("precision")
		obj.snapX=self.getMember("snapX")
		obj.snapY=self.getMember("snapY")
		obj.pointCount=len(self.points)
		ot=(ESPathPoint*obj.pointCount)()
		for count in range(obj.pointCount):
			me=ESPathPoint()
			me.x=int(self.points[count][0])#gmk doubles
			me.y=int(self.points[count][1])
			me.speed=int(self.points[count][2])
			ot[count]=me
		obj.points=cast(ot,POINTER(ESPathPoint))
		return obj

	def Finalize(self):
		if self.getMember("roomIndex") != GamePath.RoomIndexNone:
			self.setMember("room", self.gameFile.GetResource(GameRoom, self.getMember("roomIndex")))
