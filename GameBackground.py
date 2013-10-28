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
from GameSprite import *

class GameBackground(GameResource):
	defaults={"id":-1,"name":"noname","transparent":False,"smoothEdges":False,"preload":False,"useAsTileset":False,
	"tileWidth":16,"tileHeight":16,"tileHorizontalOffset":0,"tileVerticalOffset":0,"tileHorizontalSeperation":0,"tileVerticalSeperation":0,
	"data":None,"width":0,"height":0,"For3D":0}

	def __init__(self, gameFile, id):
		GameResource.__init__(self, gameFile, id)
		self.setMember("name","background_"+str(id))

	def ReadEgm(self, gmkfile, entry, z):
		stream=z.open(entry+".ey",'r')
		y=YamlParser()
		r=y.parseStream(stream)
		self.setMember("name",os.path.split(entry)[1])
		self.setMember("preload",r.getMbool('preload'))
		self.setMember("smoothEdges",r.getMbool('smooth_edges'))
		self.setMember("tileHorizontalOffset",r.getMint('h_offset'))
		self.setMember("tileHeight",r.getMint('tile_height'))
		self.setMember("tileVerticalSeperation",r.getMint('v_sep'))
		self.setMember("tileHorizontalSeperation",r.getMint('h_sep'))
		self.setMember("tileVerticalOffset",r.getMint('v_offset'))
		self.setMember("tileWidth",r.getMint('tile_width'))
		self.setMember("useAsTileset",r.getMbool('use_as_tileset'))
		self.setMember("transparent",r.getMbool('transparent'))
		data=r.getMstr('Data')
		data=z.open(os.path.split(entry)[0]+"/"+data,'r')
		images = ApngIO().apngToBufferedImages(data)
		image=QtGui.QImage()
		image.loadFromData(images[0].read())
		width,height,data=GameSpriteSubimage.FromQImage(image)
		self.setMember("data",data)
		self.setMember("width",width)
		self.setMember("height",height)

	def ReadGmx(self, gmkfile, gmxdir, name):
		tree=xml.etree.ElementTree.parse(os.path.join(gmxdir,name)+".background.gmx")
		root=tree.getroot()
		if root.tag!="background":
			print_error("tag isn't background "+root.tag)
		seen={}
		for child in root:
			if seen.get(child.tag,0)>0:
				print_error("duplicated tag "+child.tag)
			seen[child.tag]=seen.get(child.tag,0)+1
			if child.tag=="istileset":
				self.setMember("useAsTileset",bool(int(child.text)))
			elif child.tag=="tilewidth":
				self.setMember("tileWidth",int(child.text))
			elif child.tag=="tileheight":
				self.setMember("tileHeight",int(child.text))
			elif child.tag=="tilexoff":
				self.setMember("tileHorizontalOffset",int(child.text))
			elif child.tag=="tileyoff":
				self.setMember("tileVerticalOffset",int(child.text))
			elif child.tag=="tilehsep":
				self.setMember("tileHorizontalSeperation",int(child.text))
			elif child.tag=="tilevsep":
				self.setMember("tileVerticalSeperation",int(child.text))
			elif child.tag=="HTile":
				pass
			elif child.tag=="VTile":
				pass
			elif child.tag=="TextureGroups":
				pass
			elif child.tag=="TextureGroup":
				pass
			elif child.tag=="For3D":
				self.setMember("For3D",int(child.text))
			elif child.tag=="width":
				self.setMember("width",int(child.text))
			elif child.tag=="height":
				self.setMember("height",int(child.text))
			elif child.tag=="data":
				filep=emptyTextToString(child.text).replace("\\","/")
				if os.path.exists(os.path.join(gmxdir,filep)):
					data=open(os.path.join(gmxdir,filep),"rb")
					data=data.read()
					image=QtGui.QImage()
					image.loadFromData(data)
					width,height,data=GameSpriteSubimage.FromQImage(image)
					self.setMember("data",data)
					if width == 0 or height == 0:
						print_error("background size is 0")
				else:
					self.setMember("data",b"")
			else:
				print_error("unsupported tag "+child.tag)

	def ReadGmk(self, stream):
		backgroundStream = stream.Deserialize()
		if not backgroundStream:
			return
		self.exists = backgroundStream.ReadBoolean()
		if not self.exists:
			self.exists = False
			return
		self.setMember("name",backgroundStream.ReadString())
		backgroundStream.ReadTimestamp()
		backgroundStream.ReadDword()
		self.setMember("useAsTileset",backgroundStream.ReadBoolean())
		self.setMember("tileWidth",backgroundStream.ReadDword())
		self.setMember("tileHeight",backgroundStream.ReadDword())
		self.setMember("tileHorizontalOffset",backgroundStream.ReadDword())
		self.setMember("tileVerticalOffset",backgroundStream.ReadDword())
		self.setMember("tileHorizontalSeperation",backgroundStream.ReadDword())
		self.setMember("tileVerticalSeperation",backgroundStream.ReadDword())
		backgroundStream.ReadDword()
		self.setMember("width",backgroundStream.ReadDword())
		self.setMember("height",backgroundStream.ReadDword())
		if (self.getMember("width") != 0 and self.getMember("height") != 0):
			self.setMember("data",backgroundStream.Deserialize(False))
		if not self.getMember("data"):
			print_warning("background has no data")

	def WriteGmk(self, stream):
		backgroundStream = BinaryStream()
		backgroundStream.WriteBoolean(self.exists)
		backgroundStream.WriteString(self.getMember("name"))
		backgroundStream.WriteTimestamp()
		backgroundStream.WriteDword(710)
		backgroundStream.WriteBoolean(self.getMember("useAsTileset"))
		backgroundStream.WriteDword(self.getMember("tileWidth"))
		backgroundStream.WriteDword(self.getMember("tileHeight"))
		backgroundStream.WriteDword(self.getMember("tileHorizontalOffset"))
		backgroundStream.WriteDword(self.getMember("tileVerticalOffset"))
		backgroundStream.WriteDword(self.getMember("tileHorizontalSeperation"))
		backgroundStream.WriteDword(self.getMember("tileVerticalSeperation"))
		backgroundStream.WriteDword(800)
		backgroundStream.WriteDword(self.getMember("width"))
		backgroundStream.WriteDword(self.getMember("height"))
		if self.getMember("width") != 0 and self.getMember("height") != 0:
			backgroundStream.Serialize(self.getMember("data"), False)
		stream.Serialize(backgroundStream)

	def WriteGGG(self):
		stri="@background "+self.getMember("name")+"{\n"
		for key in self.members:
			if not self.ifDefault(key):
				if key != "data":
					stri+="\t"+key+"="+str(self.getMember(key))+"\n"
		stri+="\t@data {\n"+str(self.getMember("data").EncodeBase64().decode())+"}\n"
		
		#stri+="\tdata="+str(self.getMember("data"))+"\n"
		stri+="}\n"
		return stri

	def WriteESBackground(self):
		obj=ESBackground()
		obj.name=self.getMember("name").encode()
		obj.id=self.getMember("id")
		obj.transparent=self.getMember("transparent")
		obj.smoothEdges=self.getMember("smoothEdges")
		obj.preload=self.getMember("preload")
		obj.useAsTileset=self.getMember("useAsTileset")
		obj.tileWidth=self.getMember("tileWidth")
		obj.tileHeight=self.getMember("tileHeight")
		obj.hOffset=self.getMember("tileHorizontalOffset")
		obj.vOffset=self.getMember("tileVerticalOffset")
		obj.hSep=self.getMember("tileHorizontalSeperation")
		obj.vSep=self.getMember("tileVerticalSeperation")
		me=GameSpriteSubimage()
		me.width=self.getMember("width")
		me.height=self.getMember("height")
		me.setGmkData(self.getMember("data"))
		if not self.getMember("data"):
			print_error("background has no data")
		es=me.WriteESSubImage(obj.transparent)
		obj.backgroundImage=es
		return obj
