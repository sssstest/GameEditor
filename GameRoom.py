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
from GameBackground import *

def ABGRtoARGB(color):
	return (color&0xff000000) | ((color&0xff)<<16) | (color&0xff00) | ((color&0xff0000)>>16)

def BuildColor(r, g, b):
	return (b << 16) | (g << 8) | r

class GameRoomBackground(GameResource):
	defaults={"visible":False,"foreground":False,"imageIndex":-1,"image":None,"x":0,"y":0,"tileHorizontal":True,
		  "tileVertical":True,"speedHorizontal":0,"speedVertical":0,"stretch":False}

	def __init__(self, gameFile):
		GameResource.__init__(self, gameFile, -1)

	def setMember(self, member, value):
		GameResource.setMember(self, member, value)
		if not self.gameFile.ifReadingFile:
			if member=="imageIndex":
				if value != -1:
					self.setMember("image", self.gameFile.GetResource(GameBackground, value))

	def ReadGmk(self, stream):
		self.setMember("visible",stream.ReadBoolean())
		self.setMember("foreground",stream.ReadBoolean())
		self.setMember("imageIndex",stream.readInt32())
		self.setMember("x",stream.ReadDword())
		self.setMember("y",stream.ReadDword())
		self.setMember("tileHorizontal",stream.ReadBoolean())
		self.setMember("tileVertical",stream.ReadBoolean())
		self.setMember("speedHorizontal",stream.ReadDword())
		self.setMember("speedVertical",stream.ReadDword())
		self.setMember("stretch",stream.ReadBoolean())

	def WriteGmk(self, stream):
		stream.WriteBoolean(self.getMember("visible"))
		stream.WriteBoolean(self.getMember("foreground"))
		if self.getMember("image"):
			stream.WriteDword(self.getMember("image").getMember("id"))
		else:
			stream.WriteDword(-1)
		stream.WriteDword(self.getMember("x"))
		stream.WriteDword(self.getMember("y"))
		stream.WriteBoolean(self.getMember("tileHorizontal"))
		stream.WriteBoolean(self.getMember("tileVertical"))
		stream.WriteDword(self.getMember("speedHorizontal"))
		stream.WriteDword(self.getMember("speedVertical"))
		stream.WriteBoolean(self.getMember("stretch"))

	def Finalize(self):
		if self.getMember("imageIndex") != -1:
			self.setMember("image", self.gameFile.GetResource(GameBackground, self.getMember("imageIndex")))

	def WriteGGG(self):
		stri="@roombackground {\n"
		for key in self.members:
			if not self.ifDefault(key):
				stri+="\t"+key+"="+str(self.getMember(key))+"\n"
		stri+="}\n"
		return stri

	def WriteESRoomBackground(self):
		obj=ESRoomBackground()
		obj.visible=self.getMember("visible")
		obj.foreground=self.getMember("foreground")
		obj.x=self.getMember("x")
		obj.y=self.getMember("y")
		obj.tileHoriz=self.getMember("tileHorizontal")
		obj.tileVert=self.getMember("tileVertical")
		obj.hSpeed=self.getMember("speedHorizontal")
		obj.vSpeed=self.getMember("speedVertical")
		obj.stretch=self.getMember("stretch")
		obj.backgroundId=self.getMemberId("image")
		return obj

class GameRoomView(GameResource):
	defaults={"visible":False,"viewX":0,"viewY":0,"viewW":640,"viewH":480,"portX":0,"portY":0,"portW":640,"portH":640,
	"horizontalBorder":32,"verticalBorder":32,"horizontalSpeed":-1,"verticalSpeed":-1,"objectFollowingIndex":-1,"objectFollowing":None}

	def __init__(self, gameFile):
		GameResource.__init__(self, gameFile, -1)

	def setMember(self, member, value):
		GameResource.setMember(self, member, value)
		if not self.gameFile.ifReadingFile:
			if member=="objectFollowingIndex":
				if value != -1:
					self.setMember("objectFollowing", self.gameFile.GetResource("GameObject", value))

	def ReadGmk(self, stream):
		self.setMember("visible",stream.ReadBoolean())
		self.setMember("viewX",stream.ReadDword())
		self.setMember("viewY",stream.ReadDword())
		self.setMember("viewW",stream.ReadDword())
		self.setMember("viewH",stream.ReadDword())
		self.setMember("portX",stream.ReadDword())
		self.setMember("portY",stream.ReadDword())
		self.setMember("portW",stream.ReadDword())
		self.setMember("portH",stream.ReadDword())
		self.setMember("horizontalBorder",stream.ReadDword())
		self.setMember("verticalBorder",stream.ReadDword())
		self.setMember("horizontalSpeed",stream.ReadDword())
		self.setMember("verticalSpeed",stream.ReadDword())
		self.setMember("objectFollowingIndex",stream.ReadDword())

	def WriteGmk(self, stream):
		stream.WriteBoolean(self.getMember("visible"))
		stream.WriteDword(self.getMember("viewX"))
		stream.WriteDword(self.getMember("viewY"))
		stream.WriteDword(self.getMember("viewW"))
		stream.WriteDword(self.getMember("viewH"))
		stream.WriteDword(self.getMember("portX"))
		stream.WriteDword(self.getMember("portY"))
		stream.WriteDword(self.getMember("portW"))
		stream.WriteDword(self.getMember("portH"))
		stream.WriteDword(self.getMember("horizontalBorder"))
		stream.WriteDword(self.getMember("verticalBorder"))
		stream.WriteDword(self.getMember("horizontalSpeed"))
		stream.WriteDword(self.getMember("verticalSpeed"))
		if self.getMember("objectFollowing"):
			stream.WriteDword(self.self.getMember("objectFollowing").getMember("id"))
		else:
			stream.WriteDword(-1)

	def Finalize(self):
		if self.getMember("objectFollowingIndex") != -1:
			self.setMember("objectFollowing", self.gameFile.GetResource("GameObject", self.getMember("objectFollowingIndex")))

	def WriteGGG(self):
		stri="@view {\n"
		for key in self.members:
			if not self.ifDefault(key):
				stri+="\t"+key+"="+str(self.getMember(key))+"\n"
		stri+="}\n"
		return stri

	def WriteESRoomView(self):
		obj=ESRoomView()
		obj.visible=self.getMember("visible")
		obj.viewX=self.getMember("viewX")
		obj.viewY=self.getMember("viewY")
		obj.viewW=self.getMember("viewW")
		obj.viewH=self.getMember("viewH")
		obj.portX=self.getMember("portX")
		obj.portY=self.getMember("portY")
		obj.portW=self.getMember("portW")
		obj.portH=self.getMember("portH")
		obj.borderH=self.getMember("horizontalBorder")
		obj.borderV=self.getMember("verticalBorder")
		obj.speedH=self.getMember("horizontalSpeed")
		obj.speedV=self.getMember("verticalSpeed")
		obj.objectId=self.getMemberId("objectFollowing")
		return obj

class GameRoomInstance(GameResource):
	defaults={"x":0,"y":0,"objectIndex":-1,"object":None,"id":0,"creationCode":"","locked":False,
	"scaleX":0,"scaleY":0,"color":0,"rotation":0}

	def __init__(self, gameFile):
		GameResource.__init__(self, gameFile, -1)

	def setMember(self, member, value):
		GameResource.setMember(self, member, value)
		if not self.gameFile.ifReadingFile:
			if member=="objectIndex":
				if value != -1:
					self.setMember("object", self.gameFile.GetResource("GameObject", value))

	def ReadGmk(self, stream):
		self.setMember("x",stream.ReadDword())
		self.setMember("y",stream.ReadDword())
		self.setMember("objectIndex",stream.readInt32())
		self.setMember("id",stream.ReadDword())
		self.setMember("creationCode",stream.ReadString())
		self.setMember("locked",stream.ReadBoolean())

	def WriteGmk(self, stream):
		stream.WriteDword(self.getMember("x"))
		stream.WriteDword(self.getMember("y"))
		if self.getMember("object"):
			stream.WriteDword(self.getMember("object").getMember("id"))
		else:
			stream.WriteDword(-1)
		stream.WriteDword(self.getMember("id"))
		stream.WriteString(self.getMember("creationCode"))
		stream.WriteBoolean(self.getMember("locked"))

	def Finalize(self):
		if self.getMember("objectIndex") != -1:
			self.setMember("object", self.gameFile.GetResource("GameObject", self.getMember("objectIndex")))

	def WriteGGG(self):
		stri="@instance {\n"
		for key in self.members:
			if not self.ifDefault(key):
				stri+="\t"+key+"="+str(self.getMember(key))+"\n"
		stri+="}\n"
		return stri

	def WriteESRoomInstance(self):
		obj=ESRoomInstance()
		obj.x=self.getMember("x")
		obj.y=self.getMember("y")
		obj.objectId=self.getMemberId("object")
		obj.id=self.getMember("id")
		obj.creationCode=self.getMember("creationCode").encode()
		obj.locked=self.getMember("locked")
		return obj

class GameRoomTile(GameResource):
	defaults={"x":0,"y":0,"backgroundIndex":-1,"background":None,"tileX":0,"tileY":0,"width":0,"height":0,"layer":1000000,"id":0,"locked":False}

	def __init__(self, gameFile):
		GameResource.__init__(self, gameFile, -1)

	def setMember(self, member, value):
		GameResource.setMember(self, member, value)
		if not self.gameFile.ifReadingFile:
			if member=="backgroundIndex":
				if value != -1:
					self.setMember("background", self.gameFile.GetResource("GameObject", value))

	def ReadGmk(self, stream):
		self.setMember("x",stream.ReadDword())
		self.setMember("y",stream.ReadDword())
		self.setMember("backgroundIndex",stream.readInt32())
		self.setMember("tileX",stream.ReadDword())
		self.setMember("tileY",stream.ReadDword())
		self.setMember("width",stream.ReadDword())
		self.setMember("height",stream.ReadDword())
		self.setMember("layer",stream.ReadDword())
		self.setMember("id",stream.ReadDword())
		self.setMember("locked",stream.ReadBoolean())

	def Finalize(self):
		if self.getMember("backgroundIndex") != -1:
			self.setMember("background", self.gameFile.GetResource(GameBackground, self.getMember("backgroundIndex")))

	def WriteGGG(self):
		stri="@tile {\n"
		for key in self.members:
			if not self.ifDefault(key):
				stri+="\t"+key+"="+str(self.getMember(key))+"\n"
		stri+="}\n"
		return stri

	def WriteESRoomTile(self):
		obj=ESRoomTile()
		obj.bgX=self.getMember("tileX")
		obj.bgY=self.getMember("tileY")
		obj.roomX=self.getMember("x")
		obj.roomY=self.getMember("y")
		obj.width=self.getMember("width")
		obj.height=self.getMember("height")
		obj.depth=self.getMember("layer")
		obj.backgroundId=self.getMemberId("background")
		obj.id=self.getMember("id")
		obj.locked=self.getMember("locked")
		return obj

class GameRoom(GameResource):
	defaults={"id":-1,"name":"noname","caption":"","width":640,"height":480,"hsnap":16,"vsnap":16,"isometric":False,
	"speed":30,"persistent":False,"color":BuildColor(192, 192, 192),
	"bgFlags":3,"showcolor":True,"clearViewBackground":True,"code":"","enableViews":False,
	"rememberRoomEditorInfo":True,"roomEditorWidth":646,"roomEditorHeight":488,"showGrid":True,
	"showObjects":True,"showTiles":True,"showBackgrounds":True,"showForegrounds":True,"showViews":False,
	"deleteUnderlyingObj":True,"deleteUnderlyingTiles":True,"page":0,"xoffset":0,"yoffset":0,
	"PhysicsWorld":0,"PhysicsWorldTop":0,"PhysicsWorldLeft":0,"PhysicsWorldRight":0,"PhysicsWorldBottom":0,"PhysicsWorldGravityX":0,
	"PhysicsWorldGravityY":0,"PhysicsWorldGravityY":0,"PhysicsWorldPixToMeters":0.0}

	def __init__(self, gameFile, id):
		GameResource.__init__(self, gameFile, id)
		self.setMember("name","room_"+str(id))
		self.views=[]
		self.instances=[]
		self.tiles=[]
		self.backgrounds=[]

	def addView(self, point):
		if point in self.views:
			print_error("add duplicate")
		self.views.append(point)
		for callBack in self.listeners:
			callBack("subresource","views",None,None)

	def addInstance(self, point):
		if point in self.instances:
			print_error("add duplicate")
		self.instances.append(point)
		for callBack in self.listeners:
			callBack("subresource","instances",None,None)

	def addTile(self, point):
		if point in self.tiles:
			print_error("add duplicate")
		self.tiles.append(point)
		for callBack in self.listeners:
			callBack("subresource","tiles",None,None)

	def addBackground(self, point):
		if point in self.backgrounds:
			print_error("add duplicate")
		self.backgrounds.append(point)
		for callBack in self.listeners:
			callBack("subresource","backgrounds",None,None)

	def GetInstanceHighestId(self):
		highest=100000
		for s in self.instances:
			id = s.getMember("id")
			if id>highest:
				highest=id
		return highest

	def newView(self):
		instance = GameRoomView(self.gameFile)
		self.addView(instance)
		return instance

	def newInstance(self):
		instance = GameRoomInstance(self.gameFile)
		instance.setMember("id",self.GetInstanceHighestId()+1)
		self.addInstance(instance)
		return instance

	def newTile(self):
		instance = GameRoomTile(self.gameFile)
		self.addTile(instance)
		return instance

	def newBackground(self):
		instance = GameRoomBackground(self.gameFile)
		self.addBackground(instance)
		return instance

	def ReadEgm(self, gmkfile, entry, z):
		stream=z.open(entry+".ey",'r')
		y=YamlParser()
		r=y.parseStream(stream)
		self.setMember("name",os.path.split(entry)[1])
		self.setMember("caption",r.getMstr('CAPTION'))
		self.setMember("width",r.getMint('WIDTH'))
		self.setMember("height",r.getMint('HEIGHT'))
		self.setMember("vsnap",r.getMint('SNAP_X'))
		self.setMember("hsnap",r.getMint('SNAP_Y'))
		self.setMember("isometric",r.getMbool('ISOMETRIC'))
		self.setMember("speed",r.getMint('SPEED'))
		self.setMember("persistent",r.getMbool('PERSISTENT'))
		self.setMember("color",r.getMhex('BACKGROUND_COLOR'))
		self.setMember("showcolor",r.getMbool('DRAW_BACKGROUND_COLOR'))
		#self.setMember("clearViewBackground
		#self.setMember("code
		self.setMember("enableViews",r.getMbool('ENABLE_VIEWS'))
		self.setMember("rememberRoomEditorInfo",r.getMbool('REMEMBER_WINDOW_SIZE'))#clifix
		self.setMember("roomEditorWidth",r.getMint('EDITOR_WIDTH'))
		self.setMember("roomEditorHeight",r.getMint('EDITOR_HEIGHT'))
		self.setMember("showGrid",r.getMbool('SHOW_GRID'))
		self.setMember("showObjects",r.getMbool('SHOW_OBJECTS'))
		self.setMember("showTiles",r.getMbool('SHOW_TILES'))
		self.setMember("showBackgrounds",r.getMbool('SHOW_BACKGROUNDS'))
		self.setMember("showForegrounds",r.getMbool('SHOW_FOREGROUNDS'))
		self.setMember("showViews",r.getMbool('SHOW_VIEWS'))
		self.setMember("deleteUnderlyingObj",r.getMbool('DELETE_UNDERLYING_OBJECTS'))
		self.setMember("deleteUnderlyingTiles",r.getMbool('DELETE_UNDERLYING_TILES'))
		self.setMember("page",r.getMint('CURRENT_TAB'))
		self.setMember("xoffset",r.getMint('SCROLL_BAR_X'))
		self.setMember("yoffset",r.getMint('SCROLL_BAR_Y'))
		data=r.getMstr('Data')
		data=z.open(os.path.split(entry)[0]+"/"+data,'r')
		data=data.read()
		stream = BinaryStream(io.BytesIO(data))
		code = stream.ReadString()

		nobackgrounds=stream.ReadDword()
		#print_notice(entry+" nobackgrounds "+str(nobackgrounds))
		for count in range(nobackgrounds):
			background = self.newBackground()
			background.setMember("visible",stream.ReadBoolean())
			background.setMember("foreground",stream.ReadBoolean())
			imageName=stream.ReadString()
			if len(imageName)>0:
				background.setMember("imageIndex",gmkfile.egmNameId[imageName])
			background.setMember("x",stream.ReadDword())
			background.setMember("y",stream.ReadDword())
			background.setMember("tileHorizontal",stream.ReadBoolean())
			background.setMember("tileVertical",stream.ReadBoolean())
			background.setMember("speedHorizontal",stream.ReadDword())
			background.setMember("speedVertical",stream.ReadDword())
			background.setMember("stretch",stream.ReadBoolean())
		noviews=stream.ReadDword()
		#print_notice(entry+" noviews "+str(noviews))
		for count in range(noviews):
			view = self.newView()
			view.setMember("visible",stream.ReadBoolean())
			view.setMember("viewX",stream.ReadDword())
			view.setMember("viewY",stream.ReadDword())
			view.setMember("viewW",stream.ReadDword())
			view.setMember("viewH",stream.ReadDword())
			view.setMember("portX",stream.ReadDword())
			view.setMember("portY",stream.ReadDword())
			view.setMember("portW",stream.ReadDword())
			view.setMember("portH",stream.ReadDword())
			view.setMember("horizontalBorder",stream.ReadDword())
			view.setMember("verticalBorder",stream.ReadDword())
			#view.setMember("objectFollowingIndex",stream.readInt32())
			view.setMember("horizontalSpeed",stream.ReadDword())
			view.setMember("verticalSpeed",stream.ReadDword())
			objectFollowing=stream.ReadString()
			#print("objectFollowing",objectFollowing)
		noinstances=stream.ReadDword()
		#print_notice(entry+" noinstances "+str(noinstances))
		if noinstances==-1:
			print_error("unsupported format rmg")
		for count in range(noinstances):
			instance = self.newInstance()
			instance.setMember("x",stream.ReadDword())
			instance.setMember("y",stream.ReadDword())
			instanceObject=stream.ReadString()
			if instanceObject=="":
				instance.setMember("objectIndex",-1)
			else:
				instance.setMember("objectIndex",gmkfile.egmNameId[instanceObject])
			instance.setMember("id",stream.ReadDword())
			instance.setMember("creationCode",stream.ReadString())
			instance.setMember("locked",stream.ReadBoolean())
		notiles=stream.ReadDword()
		#print_notice(entry+" notiles "+str(notiles))
		for count in range(notiles):
			tile=self.newTile()
			tile.setMember("x",stream.ReadDword())
			tile.setMember("y",stream.ReadDword())
			backgroundName=stream.ReadString()
			if backgroundName=="":
				tile.setMember("backgroundIndex",-1)
			else:
				tile.setMember("backgroundIndex",gmkfile.egmNameId[backgroundName])
			tile.setMember("tileX",stream.ReadDword())
			tile.setMember("tileY",stream.ReadDword())
			tile.setMember("width",stream.ReadDword())
			tile.setMember("height",stream.ReadDword())
			tile.setMember("layer",stream.ReadDword())
			tile.setMember("id",stream.readInt32())
			tile.setMember("locked",stream.ReadBoolean())

	def ReadGmx(self, gmkfile, gmxdir, name):
		tree=xml.etree.ElementTree.parse(os.path.join(gmxdir,name)+".room.gmx")
		root=tree.getroot()
		if root.tag!="room":
			print_error("tag isn't room "+root.tag)
		seen={}
		for child in root:
			if seen.get(child.tag,0)>0:
				print_error("duplicated tag "+child.tag)
			seen[child.tag]=seen.get(child.tag,0)+1
			if child.tag=="caption":
				self.setMember("caption",emptyTextToString(child.text))
			elif child.tag=="width":
				self.setMember("width",int(child.text))
			elif child.tag=="height":
				self.setMember("height",int(child.text))
			elif child.tag=="vsnap":
				self.setMember("vsnap",int(child.text))
			elif child.tag=="hsnap":
				self.setMember("hsnap",int(child.text))
			elif child.tag=="isometric":
				self.setMember("isometric",bool(int(child.text)))
			elif child.tag=="speed":
				self.setMember("speed",int(child.text))
			elif child.tag=="persistent":
				self.setMember("persistent",bool(int(child.text)))
			elif child.tag=="colour":
				self.setMember("color",int(child.text))
			elif child.tag=="showcolour":
				self.setMember("showcolor",bool(int(child.text)))
			elif child.tag=="code":
				self.setMember("code",emptyTextToString(child.text))
			elif child.tag=="enableViews":
				self.setMember("enableViews",bool(int(child.text)))
			elif child.tag=="clearViewBackground":
				self.setMember("clearViewBackground",bool(int(child.text)))
			elif child.tag=="makerSettings":
				for chil in child:
					if chil.tag=="isSet":
						self.setMember("rememberRoomEditorInfo",bool(int(chil.text)))
					elif chil.tag=="w":
						self.setMember("roomEditorWidth",int(chil.text))
					elif chil.tag=="h":
						self.setMember("roomEditorHeight",int(chil.text))
					elif chil.tag=="showGrid":
						self.setMember("showGrid",bool(int(chil.text)))
					elif chil.tag=="showObjects":
						self.setMember("showObjects",bool(int(chil.text)))
					elif chil.tag=="showTiles":
						self.setMember("showTiles",bool(int(chil.text)))
					elif chil.tag=="showBackgrounds":
						self.setMember("showBackgrounds",bool(int(chil.text)))
					elif chil.tag=="showForegrounds":
						self.setMember("showForegrounds",bool(int(chil.text)))
					elif chil.tag=="showViews":
						self.setMember("showViews",bool(int(chil.text)))
					elif chil.tag=="deleteUnderlyingObj":
						self.setMember("deleteUnderlyingObj",bool(int(chil.text)))
					elif chil.tag=="deleteUnderlyingTiles":
						self.setMember("deleteUnderlyingTiles",bool(int(chil.text)))
					elif chil.tag=="page":
						self.setMember("page",int(chil.text))
					elif chil.tag=="xoffset":
						self.setMember("xoffset",int(chil.text))
					elif chil.tag=="yoffset":
						self.setMember("yoffset",int(chil.text))
					else:
						print_error("unsupported makerSetting "+chil.tag)
				if len(child)==0:
					print_error("tag isn't makerSettings "+child.tag)
			elif child.tag=="backgrounds":
				#<backgrounds><background visible="0" foreground="0" name="" x="0" y="0" htiled="-1" vtiled="-1" hspeed="0" vspeed="0" stretch="0"/></backgrounds>
				for chil in child:
					if chil.tag=="background":
						background = self.newBackground()
						background.setMember("visible",bool(int(chil.attrib["visible"])))
						background.setMember("foreground",bool(int(chil.attrib["foreground"])))
						if chil.attrib["name"]=="":
							background.imageIndex=-1
						else:
							background.imageIndex		= gmkfile.egmNameId[chil.attrib["name"]]
						background.setMember("x",int(chil.attrib["x"]))
						background.setMember("y",int(chil.attrib["y"]))
						background.setMember("tileHorizontal",bool(int(chil.attrib["htiled"])))
						background.setMember("tileVertical",bool(int(chil.attrib["vtiled"])))
						background.setMember("speedHorizontal",int(chil.attrib["hspeed"]))
						background.setMember("speedVertical",int(chil.attrib["vspeed"]))
						background.setMember("stretch",bool(int(chil.attrib["stretch"])))
					else:
						print_error("tag isn't background "+chil.tag)
				if len(child)==0:
					print_error("no backgrounds")
			elif child.tag=="views":
				#<view visible="0" objName="" xview="0" yview="0" wview="640" hview="480" xport="0" yport="0" wport="640" hport="480" hborder="32" vborder="32" hspeed="-1" vspeed="-1"/>
				for chil in child:
					if chil.tag=="view":
						view = self.newView()
						view.setMember("visible",bool(int(chil.attrib["visible"])))
						if chil.attrib["objName"]=="":
							view.objectFollowingIndex=-1
						else:
							view.objectFollowingIndex		= gmkfile.egmNameId[chil.attrib["objName"]]
						view.setMember("viewX",int(chil.attrib["xview"]))
						view.setMember("viewY",int(chil.attrib["yview"]))
						view.setMember("viewW",int(chil.attrib["wview"]))
						view.setMember("viewH",int(chil.attrib["hview"]))
						view.setMember("portX",int(chil.attrib["xport"]))
						view.setMember("portY",int(chil.attrib["yport"]))
						view.setMember("portW",int(chil.attrib["wport"]))
						view.setMember("portH",int(chil.attrib["hport"]))
						view.setMember("horizontalBorder",int(chil.attrib["hborder"]))
						view.setMember("verticalBorder",int(chil.attrib["vborder"]))
						view.setMember("horizontalSpeed",int(chil.attrib["hspeed"]))
						view.setMember("verticalSpeed",int(chil.attrib["vspeed"]))
					else:
						print_error("tag isn't view "+chil.tag)
				if len(child)==0:
					print_error("no views")
			elif child.tag=="instances":
				#<instance objName="obj_ball" x="64" y="16" name="inst_C0E071DD" locked="0" code="" scaleX="1" scaleY="1" colour="4294967295" rotation="0"/>
				#<instance index="2" objName="oControl" x="512" y="720" name="inst_AF8F4250" locked="0" code=""/>
				c=100001
				for chil in child:
					if chil.tag=="instance":
						instance = self.newInstance()
						instance.setMember("objectIndex",gmkfile.egmNameId[chil.attrib["objName"]])
						instance.setMember("x",int(chil.attrib["x"]))
						instance.setMember("y",int(chil.attrib["y"]))
						#chil.attrib["name"]
						instance.setMember("id",c)
						instance.setMember("locked",bool(int(chil.attrib["locked"])))
						instance.setMember("creationCode",emptyTextToString(chil.attrib["code"]))
						if "scaleX" in chil.attrib:instance.setMember("scaleX",int(chil.attrib["scaleX"]))
						if "scaleY" in chil.attrib:instance.setMember("scaleY",int(chil.attrib["scaleY"]))
						if "colour" in chil.attrib:instance.setMember("color",int(chil.attrib["colour"]))
						if "rotation" in chil.attrib:instance.setMember("rotation",int(chil.attrib["rotation"]))
						c+=1
					else:
						print_error("tag isn't instance "+chil.tag)
				#if len(child)==0:
				#	print_error("no instances")
			elif child.tag=="tiles":
				for chil in child:
					print_warning("gmx tiles unsupported")
			elif child.tag=="PhysicsWorld":
				self.setMember("PhysicsWorld",int(child.text))
			elif child.tag=="PhysicsWorldTop":
				self.setMember("PhysicsWorldTop",int(child.text))
			elif child.tag=="PhysicsWorldLeft":
				self.setMember("PhysicsWorldLeft",int(child.text))
			elif child.tag=="PhysicsWorldRight":
				self.setMember("PhysicsWorldRight",int(child.text))
			elif child.tag=="PhysicsWorldBottom":
				self.setMember("PhysicsWorldBottom",int(child.text))
			elif child.tag=="PhysicsWorldGravityX":
				self.setMember("PhysicsWorldGravityX",int(child.text))
			elif child.tag=="PhysicsWorldGravityY":
				self.setMember("PhysicsWorldGravityY",int(child.text))
			elif child.tag=="PhysicsWorldPixToMeters":
				self.setMember("PhysicsWorldPixToMeters",gmxFloat(child.text))
			else:
				print_error("unsupported tag "+child.tag)

	def ReadGmk(self, stream):
		roomStream = stream.Deserialize()
		if not roomStream.ReadBoolean():
			self.exists = False
			return
		self.setMember("name",roomStream.ReadString())
		roomStream.ReadTimestamp()
		roomStream.ReadDword()
		self.setMember("caption",roomStream.ReadString())
		self.setMember("width",roomStream.ReadDword())
		self.setMember("height",roomStream.ReadDword())
		self.setMember("vsnap",roomStream.ReadDword())
		self.setMember("hsnap",roomStream.ReadDword())
		self.setMember("isometric",roomStream.ReadBoolean())
		self.setMember("speed",roomStream.ReadDword())
		self.setMember("persistent",roomStream.ReadBoolean())
		self.setMember("color",ABGRtoARGB(roomStream.ReadDword()))
		self.setMember("bgFlags",roomStream.ReadDword())
		self.setMember("showcolor",bool(self.getMember("bgFlags")&1))
		self.setMember("clearViewBackground",not self.getMember("bgFlags")&2)
		self.setMember("code",roomStream.ReadString())
		count = roomStream.ReadDword()
		while count>0:
			background = self.newBackground()
			background.ReadGmk(roomStream)
			count=count-1
		self.setMember("enableViews",roomStream.ReadBoolean())
		count = roomStream.ReadDword()
		while count>0:
			view = self.newView()
			view.ReadGmk(roomStream)
			count=count-1
		count = roomStream.ReadDword()
		while count>0:
			instance = self.newInstance()
			instance.ReadGmk(roomStream)
			count=count-1
		count = roomStream.ReadDword()
		while count>0:
			tile = self.newTile()
			tile.ReadGmk(roomStream)
			count=count-1
		self.setMember("rememberRoomEditorInfo",roomStream.ReadBoolean())
		self.setMember("roomEditorWidth",roomStream.ReadDword())
		self.setMember("roomEditorHeight",roomStream.ReadDword())
		self.setMember("showGrid",roomStream.ReadBoolean())
		self.setMember("showObjects",roomStream.ReadBoolean())
		self.setMember("showTiles",roomStream.ReadBoolean())
		self.setMember("showBackgrounds",roomStream.ReadBoolean())
		self.setMember("showForegrounds",roomStream.ReadBoolean())
		self.setMember("showViews",roomStream.ReadBoolean())
		self.setMember("deleteUnderlyingObj",roomStream.ReadBoolean())
		self.setMember("deleteUnderlyingTiles",roomStream.ReadBoolean())
		self.setMember("page",roomStream.ReadDword())
		self.setMember("xoffset",roomStream.ReadDword())
		self.setMember("yoffset",roomStream.ReadDword())

	def WriteGmx(self, root):
		gmxCreateTag(root, "caption", self.getMember("caption"))
		gmxCreateTag(root, "width", str(self.getMember("width")))
		gmxCreateTag(root, "height", str(self.getMember("height")))
		gmxCreateTag(root, "vsnap", str(self.getMember("vsnap")))
		gmxCreateTag(root, "hsnap", str(self.getMember("hsnap")))
		gmxCreateTag(root, "isometric", str(boolToGmxIntbool(self.getMember("isometric"))))
		gmxCreateTag(root, "speed", str(self.getMember("speed")))
		gmxCreateTag(root, "persistent", str(boolToGmxIntbool(self.getMember("persistent"))))
		gmxCreateTag(root, "colour", str(self.getMember("color")))
		gmxCreateTag(root, "showcolour", str(boolToGmxIntbool(self.getMember("showcolor"))))
		gmxCreateTag(root, "code", self.getMember("code"))
		gmxCreateTag(root, "enableViews", str(boolToGmxIntbool(self.getMember("enableViews"))))
		gmxCreateTag(root, "clearViewBackground", str(boolToGmxIntbool(self.getMember("clearViewBackground"))))
		makerSettings=xml.etree.ElementTree.Element("makerSettings")
		makerSettings.tail="\n"
		root.append(makerSettings)
		gmxCreateTag(makerSettings, "isSet", str(boolToGmxIntbool(self.getMember("rememberRoomEditorInfo"))))
		gmxCreateTag(makerSettings, "w", str(self.getMember("roomEditorWidth")))
		gmxCreateTag(makerSettings, "h", str(self.getMember("roomEditorHeight")))
		gmxCreateTag(makerSettings, "showGrid", str(boolToGmxIntbool(self.getMember("showGrid"))))
		gmxCreateTag(makerSettings, "showObjects", str(boolToGmxIntbool(self.getMember("showObjects"))))
		gmxCreateTag(makerSettings, "showTiles", str(boolToGmxIntbool(self.getMember("showTiles"))))
		gmxCreateTag(makerSettings, "showBackgrounds", str(boolToGmxIntbool(self.getMember("showBackgrounds"))))
		gmxCreateTag(makerSettings, "showForegrounds", str(boolToGmxIntbool(self.getMember("showForegrounds"))))
		gmxCreateTag(makerSettings, "showViews", str(boolToGmxIntbool(self.getMember("showViews"))))
		gmxCreateTag(makerSettings, "deleteUnderlyingObj", str(boolToGmxIntbool(self.getMember("deleteUnderlyingObj"))))
		gmxCreateTag(makerSettings, "deleteUnderlyingTiles", str(boolToGmxIntbool(self.getMember("deleteUnderlyingTiles"))))
		gmxCreateTag(makerSettings, "page", str(self.getMember("page")))
		gmxCreateTag(makerSettings, "xoffset", str(self.getMember("xoffset")))
		gmxCreateTag(makerSettings, "yoffset", str(self.getMember("yoffset")))
		backgrounds=xml.etree.ElementTree.Element("backgrounds")
		backgrounds.tail="\n"
		root.append(backgrounds)
		for b in self.backgrounds:
			background=xml.etree.ElementTree.Element("background")
			background.tail="\n"
			backgrounds.append(background)
			background.set("visible", str(boolToGmxIntbool(b.getMember("visible"))))
			background.set("foreground", str(boolToGmxIntbool(b.getMember("foreground"))))
			if b.getMember("image"):
				image=b.getMember("image").getMember("name")
			else:
				image=""
			background.set("name", image)
			background.set("x", str(b.getMember("x")))
			background.set("y", str(b.getMember("y")))
			background.set("htiled", str(boolToGmxIntbool(b.getMember("tileHorizontal"))))
			background.set("vtiled", str(boolToGmxIntbool(b.getMember("tileVertical"))))
			background.set("hspeed", str(b.getMember("speedHorizontal")))
			background.set("vspeed", str(b.getMember("speedVertical")))
			background.set("stretch", str(boolToGmxIntbool(b.getMember("stretch"))))
			#<background visible="0" foreground="0" name="" x="0" y="0" htiled="-1" vtiled="-1" hspeed="0" vspeed="0" stretch="0"/>
		views=xml.etree.ElementTree.Element("views")
		views.tail="\n"
		root.append(views)
		for v in self.views:
			view=xml.etree.ElementTree.Element("view")
			view.tail="\n"
			views.append(view)
			view.set("visible", str(boolToGmxIntbool(v.getMember("visible"))))
			if v.getMember("objectFollowing"):
				objName=v.getMember("objectFollowing").getMember("name")
			else:
				objName="<undefined>"
			view.set("objName", objName)
			view.set("xview", str(v.getMember("viewX")))
			view.set("yview", str(v.getMember("viewY")))
			view.set("wview", str(v.getMember("viewW")))
			view.set("hview", str(v.getMember("viewH")))
			view.set("xport", str(v.getMember("portX")))
			view.set("yport", str(v.getMember("portY")))
			view.set("wport", str(v.getMember("portW")))
			view.set("hport", str(v.getMember("portH")))
			view.set("hborder", str(v.getMember("horizontalBorder")))
			view.set("vborder", str(v.getMember("verticalBorder")))
			view.set("hspeed", str(v.getMember("horizontalSpeed")))
			view.set("vspeed", str(v.getMember("verticalSpeed")))
			#<view visible="0" objName="&lt;undefined&gt;" xview="0" yview="0" wview="640" hview="480" xport="0" yport="0" wport="640" hport="480" hborder="32" vborder="32" hspeed="-1" vspeed="-1"/>
		instances=xml.etree.ElementTree.Element("instances")
		instances.tail="\n"
		root.append(instances)
		for v in self.instances:
			instance=xml.etree.ElementTree.Element("instance")
			instance.tail="\n"
			instances.append(instance)
			if v.getMember("object"):
				objName=v.getMember("object").getMember("name")
			else:
				objName="<undefined>"
			instance.set("objName", objName)
			instance.set("x", str(v.getMember("x")))
			instance.set("y", str(v.getMember("y")))
			instance.set("name", "inst_"+str(v.getMember("id")))#clifix
			instance.set("locked", str(boolToGmxIntbool(v.getMember("locked"))))
			instance.set("code", str(v.getMember("creationCode")))
			instance.set("scaleX", str(v.getMember("scaleX")))
			instance.set("scaleY", str(v.getMember("scaleY")))
			instance.set("colour", str(v.getMember("color")))
			instance.set("rotation", str(v.getMember("rotation")))
			#<instance objName="object4" x="64" y="32" name="inst_E2A72CD3" locked="0" code="" scaleX="1" scaleY="1" colour="4294967295" rotation="0"/>

		tiles=xml.etree.ElementTree.Element("tiles")
		tiles.tail="\n"
		root.append(tiles)
		for v in self.tiles:
			tile=xml.etree.ElementTree.Element("tile")
			tile.tail="\n"
			tiles.append(tile)
			print_error("gmx tiles")
		gmxCreateTag(root, "PhysicsWorld", str(self.getMember("PhysicsWorld")))
		gmxCreateTag(root, "PhysicsWorldTop", str(self.getMember("PhysicsWorldTop")))
		gmxCreateTag(root, "PhysicsWorldLeft", str(self.getMember("PhysicsWorldLeft")))
		gmxCreateTag(root, "PhysicsWorldRight", str(self.getMember("PhysicsWorldRight")))
		gmxCreateTag(root, "PhysicsWorldBottom", str(self.getMember("PhysicsWorldBottom")))
		gmxCreateTag(root, "PhysicsWorldGravityX", str(self.getMember("PhysicsWorldGravityX")))
		gmxCreateTag(root, "PhysicsWorldGravityY", str(self.getMember("PhysicsWorldGravityY")))
		gmxCreateTag(root, "PhysicsWorldPixToMeters", str(self.getMember("PhysicsWorldPixToMeters")))

	def WriteGmk(self, stream):
		roomStream = BinaryStream()
		roomStream.WriteBoolean(self.exists)
		if self.exists:
			roomStream.WriteString(self.getMember("name"))
			roomStream.WriteTimestamp()
			roomStream.WriteDword(541)
			roomStream.WriteString(self.getMember("caption"))
			roomStream.WriteDword(self.getMember("width"))
			roomStream.WriteDword(self.getMember("height"))
			roomStream.WriteDword(self.getMember("vsnap"))
			roomStream.WriteDword(self.getMember("hsnap"))
			roomStream.WriteBoolean(self.getMember("isometric"))
			roomStream.WriteDword(self.getMember("speed"))
			roomStream.WriteBoolean(self.getMember("persistent"))
			roomStream.writeUInt32(self.getMember("color"))
			roomStream.WriteDword(((not self.getMember("clearViewBackground") & 0x01) << 1) | (self.getMember("showcolor") & 0x01))
			roomStream.WriteString(self.getMember("code"))
			roomStream.WriteDword(len(self.backgrounds))
			for i in range(len(self.backgrounds)):
				self.backgrounds[i].WriteGmk(roomStream)
			roomStream.WriteBoolean(self.getMember("enableViews"))
			roomStream.WriteDword(len(self.views))
			for i in range(len(self.views)):
				self.views[i].WriteGmk(roomStream)
			roomStream.WriteDword(len(self.instances))
			for i in range(len(self.instances)):
				self.instances[i].WriteGmk(roomStream)
			roomStream.WriteDword(len(self.tiles))
			for i in range(len(self.tiles)):
				self.tiles[i].WriteGmk(roomStream)
			roomStream.WriteBoolean(self.getMember("rememberRoomEditorInfo"))
			roomStream.WriteDword(self.getMember("roomEditorWidth"))
			roomStream.WriteDword(self.getMember("roomEditorHeight"))
			roomStream.WriteBoolean(self.getMember("showGrid"))
			roomStream.WriteBoolean(self.getMember("showObjects"))
			roomStream.WriteBoolean(self.getMember("showTiles"))
			roomStream.WriteBoolean(self.getMember("showBackgrounds"))
			roomStream.WriteBoolean(self.getMember("showForegrounds"))
			roomStream.WriteBoolean(self.getMember("showViews"))
			roomStream.WriteBoolean(self.getMember("deleteUnderlyingObj"))
			roomStream.WriteBoolean(self.getMember("deleteUnderlyingTiles"))
			roomStream.WriteDword(self.getMember("page"))
			roomStream.WriteDword(self.getMember("xoffset"))
			roomStream.WriteDword(self.getMember("yoffset"))
		stream.Serialize(roomStream)

	def Finalize(self):
		for i in range(len(self.backgrounds)):
			self.backgrounds[i].Finalize()
		for i in range(len(self.views)):
			self.views[i].Finalize()
		for i in range(len(self.instances)):
			self.instances[i].Finalize()
		for i in range(len(self.tiles)):
			self.tiles[i].Finalize()

	def WriteGGG(self):
		stri="@room "+self.getMember("name")+" {\n"
		for key in self.members:
			if not self.ifDefault(key):
				stri+="\t"+key+"="+str(self.getMember(key))+"\n"
		#for o in self.backgrounds:
		#	stri=stri+tabStringLines(o.WriteGGG())
		#for o in self.views:
		#	stri=stri+tabStringLines(o.WriteGGG())
		for o in self.instances:
			stri=stri+tabStringLines(o.WriteGGG())
		for o in self.tiles:
			stri=stri+tabStringLines(o.WriteGGG())
		stri+="}\n"
		return stri

	def WriteESRoom(self):
		obj=ESRoom()
		obj.name=self.getMember("name").encode()
		obj.id=self.getMember("id")
		obj.caption=self.getMember("caption").encode()
		obj.width=self.getMember("width")
		obj.height=self.getMember("height")
		obj.snapX=self.getMember("hsnap")
		obj.snapY=self.getMember("vsnap")
		obj.isometric=self.getMember("isometric")
		obj.speed=self.getMember("speed")
		obj.persistent=self.getMember("persistent")
		obj.backgroundColor=0xff|ARGBtoRGBA(self.getMember("color"))
		obj.drawBackgroundColor=self.getMember("showcolor")
		obj.creationCode=self.getMember("code").encode()
		obj.rememberWindowSize=self.getMember("rememberRoomEditorInfo")
		obj.editorWidth=self.getMember("roomEditorWidth")
		obj.editorHeight=self.getMember("roomEditorHeight")
		obj.showGrid=self.getMember("showGrid")
		obj.showObjects=self.getMember("showObjects")
		obj.showTiles=self.getMember("showTiles")
		obj.showBackgrounds=self.getMember("showBackgrounds")
		obj.showViews=self.getMember("showViews")
		obj.deleteUnderlyingObjects=self.getMember("deleteUnderlyingObj")
		obj.deleteUnderlyingTiles=self.getMember("deleteUnderlyingTiles")
		obj.currentTab=self.getMember("page")
		obj.scrollBarX=self.getMember("xoffset")
		obj.scrollBarY=self.getMember("yoffset")
		obj.enableViews=self.getMember("enableViews")
		obj.backgroundDefCount=len(self.backgrounds)
		ot=(ESRoomBackground*obj.backgroundDefCount)()
		for count in range(obj.backgroundDefCount):
			me=self.backgrounds[count].WriteESRoomBackground()
			ot[count]=me
		obj.backgroundDefs=cast(ot,POINTER(ESRoomBackground))
		obj.viewCount=len(self.views)
		ot=(ESRoomView*obj.viewCount)()
		for count in range(obj.viewCount):
			me=self.views[count].WriteESRoomView()
			ot[count]=me
		obj.views=cast(ot,POINTER(ESRoomView))
		obj.instanceCount=len(self.instances)
		ot=(ESRoomInstance*obj.instanceCount)()
		for count in range(obj.instanceCount):
			me=self.instances[count].WriteESRoomInstance()
			ot[count]=me
		obj.instances=cast(ot,POINTER(ESRoomInstance))
		obj.tileCount=len(self.tiles)
		ot=(ESRoomTile*obj.tileCount)()
		for count in range(obj.tileCount):
			me=self.tiles[count].WriteESRoomTile()
			ot[count]=me
		obj.tiles=cast(ot,POINTER(ESRoomTile))
		return obj

