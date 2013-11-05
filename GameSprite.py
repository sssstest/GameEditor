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

class GameSprite(GameResource):
	if Class:
		ShapePrecise=0
		ShapeRectangle=1
		ShapeDisc=2
		ShapeDiamond=3

		#BoundingBox
		BbAutomatic=0
		BbFull=1
		BbManual=2

	defaults={"id":-1,"name":"noname","width":0,"height":0,"bbox_left":0,"bbox_right":0,"bbox_bottom":0,"bbox_top":0,
	"xorigin":0,"yorigin":0,"maskshape":ShapePrecise,"alphatolerance":0,"precisecollisionchecking":True,"seperatemasks":False,
	"transparent":False,"smoothedges":False,"bboxmode":BbAutomatic,"preload":True,
	"HTile":0,"VTile":0,"For3D":0}#clifix gmx default

	def __init__(self, gameFile, id):
		GameResource.__init__(self, gameFile, id)
		self.setMember("name","sprite_"+str(id))
		self.subimages=[]
		self.qIcon=None

	def getQIcon(self, update=False):
		if self.qIcon:
			return self.qIcon
		if len(self.subimages)>0:
			return None
			if update==False and self.subimages[0].width>200:
				image=None
				#print("sprite too big not creating QIcon")
			else:
				#print("slow conversion",self.subimages[0].width)
				q=self.subimages[0].getQImage()
				image=QtGui.QPixmap()
				image.convertFromImage(q)
				if self.subimages[0].width < 16:
					image=image.scaled(16,16)
				return QtGui.QIcon(image)
		return None

	def updateQIcon(self):
		if not self.qIcon:
			if len(self.subimages)>0:
				q=self.subimages[0].getQImage()
				image=QtGui.QPixmap()
				image.convertFromImage(q)
				image=image.scaled(16,16)
				self.qIcon=QtGui.QIcon(image)

	def addSubimage(self, subimage):
		self.subimages.append(subimage)

	def newSubimage(self):
		instance = GameSpriteSubimage()
		self.addSubimage(instance)
		return instance

	def newSubimageFile(self, imagePath):
		qImage=QtGui.QImage(imagePath)
		subimage = self.newSubimage()
		subimage.setQImage(qImage)

	def ReadEgm(self, gmkfile, entry, z):
		stream=z.open(entry+".ey",'r')
		y=YamlParser()
		r=y.parseStream(stream)
		self.setMember("name",os.path.split(entry)[1])
		self.setMember("xorigin",r.getMint('ORIGIN_X'))
		self.setMember("yorigin",r.getMint('ORIGIN_Y'))
		#TRANSPARENT
		self.setMember("maskshape",r.getMbbshape('SHAPE'))
		self.setMember("alphatolerance",r.getMint('ALPHA_TOLERANCE'))
		self.setMember("seperatemasks",r.getMbool('SEPARATE_MASK'))
		#SMOOTH_EDGES
		#PRELOAD
		self.setMember("bboxmode",r.getMbbshape('BB_MODE'))
		self.setMember("bbox_left",r.getMint('BB_LEFT'))
		self.setMember("bbox_right",r.getMint('BB_RIGHT'))
		self.setMember("bbox_top",r.getMint('BB_TOP'))
		self.setMember("bbox_bottom",r.getMint('BB_BOTTOM'))
		data=r.getMstr('Data')
		data=z.open(os.path.split(entry)[0]+"/"+data,'r')
		a=ApngIO()
		images = a.apngToBufferedImages(data)
		for i in range(len(images)):
			q=QtGui.QImage()
			q.loadFromData(images[i].read())
			images[i]=q
		for i in range(len(images)):
			subimage = GameSpriteSubimage()
			subimage.setQImage(images[i])
			self.subimages.append(subimage)
			self.setMember("width",subimage.width)
			self.setMember("height",subimage.height)

	def ReadGmx(self, gmkfile, gmxdir, name):
		tree=xml.etree.ElementTree.parse(os.path.join(gmxdir,name)+".sprite.gmx")
		root=tree.getroot()
		if root.tag!="sprite":
			print_error("tag isn't sprite")
		seen={}
		for child in root:
			if seen.get(child.tag,0)>0:
				print_error("duplicated tag "+child.tag)
			seen[child.tag]=seen.get(child.tag,0)+1
			if child.tag=="xorig":
				self.setMember("xorigin",int(child.text))
			elif child.tag=="yorigin":
				self.setMember("yorigin",int(child.text))
			elif child.tag=="colkind":
				self.setMember("maskshape",int(child.text))
			elif child.tag=="coltolerance":
				self.setMember("alphatolerance",int(child.text))
			elif child.tag=="sepmasks":#-1
				self.setMember("seperatemasks",bool(int(child.text)))
			elif child.tag=="bboxmode":
				self.setMember("bboxmode",int(child.text))
			elif child.tag=="bbox_left":
				self.setMember("bbox_left",int(child.text))
			elif child.tag=="bbox_right":
				self.setMember("bbox_right",int(child.text))
			elif child.tag=="bbox_top":
				self.setMember("bbox_top",int(child.text))
			elif child.tag=="bbox_bottom":
				self.setMember("bbox_bottom",int(child.text))
			elif child.tag=="HTile":#clifix
				self.setMember("HTile",int(child.text))
			elif child.tag=="VTile":#clifix
				self.setMember("VTile",int(child.text))
			elif child.tag=="TextureGroups":
				#TextureGroup0
				pass
			elif child.tag=="TextureGroup":#<TextureGroup>0</TextureGroup>
				pass
			elif child.tag=="For3D":
				self.setMember("For3D",int(child.text))
			elif child.tag=="width":
				self.setMember("width",int(child.text))
			elif child.tag=="height":
				self.setMember("height",int(child.text))
			elif child.tag=="frames":#<frames><frame index="0">images\spr_0_0.png</frame></frames>
				for chil in child:
					if chil.tag=="frame":
						filep=emptyTextToString(chil.text).replace("\\","/")
						data=open(os.path.join(gmxdir,filep),"rb")
						data=data.read()
						q=QtGui.QImage()
						q.loadFromData(data)
						subimage = GameSpriteSubimage()
						subimage.setQImage(q)
						self.subimages.append(subimage)
					else:
						print_error("tag isn't frame "+chil.tag)
				if len(child)==0:
					print_warning("sprite with no frames")
			else:
				print_error("unsupported tag "+child.tag)

	def ReadGmk(self, stream):
		spriteStream = stream.Deserialize()
		if not spriteStream.ReadBoolean():
			self.exists = False
			return
		self.setMember("name",spriteStream.ReadString())
		spriteStream.ReadTimestamp()
		spriteStream.ReadDword()
		self.setMember("xorigin",spriteStream.ReadDword())
		self.setMember("yorigin",spriteStream.ReadDword())
		count = spriteStream.ReadDword()
		for c in range(count):
			subimage = GameSpriteSubimage()
			#GM version needed for the following info
			spriteStream.ReadDword()
			subimage.width = spriteStream.ReadDword()
			subimage.height = spriteStream.ReadDword()
			if subimage.width != 0 and subimage.height != 0:
				subimage.gmkData = spriteStream.Deserialize(False)
			else:
				subimage.gmkData = None
			self.subimages.append(subimage)
			self.setMember("width",subimage.width)
			self.setMember("height",subimage.height)
		self.setMember("maskshape",spriteStream.ReadDword())
		self.setMember("alphatolerance",spriteStream.ReadDword())
		self.setMember("seperatemasks",spriteStream.ReadBoolean())
		self.setMember("bboxmode",spriteStream.ReadDword())
		self.setMember("bbox_left",spriteStream.ReadDword())
		self.setMember("bbox_right",spriteStream.ReadDword())
		self.setMember("bbox_bottom",spriteStream.ReadDword())
		self.setMember("bbox_top",spriteStream.ReadDword())

	def WriteGmx(self, root, gmxdir):
		gmxCreateTag(root, "xorig", str(self.getMember("xorigin")))
		gmxCreateTag(root, "yorigin", str(self.getMember("yorigin")))
		gmxCreateTag(root, "colkind", str(self.getMember("maskshape")))
		gmxCreateTag(root, "coltolerance", str(self.getMember("alphatolerance")))
		gmxCreateTag(root, "sepmasks", str(boolToGmxIntbool(self.getMember("seperatemasks"))))
		gmxCreateTag(root, "bboxmode", str(self.getMember("bboxmode")))
		gmxCreateTag(root, "bbox_left", str(self.getMember("bbox_left")))
		gmxCreateTag(root, "bbox_right", str(self.getMember("bbox_right")))
		gmxCreateTag(root, "bbox_top", str(self.getMember("bbox_top")))
		gmxCreateTag(root, "bbox_bottom", str(self.getMember("bbox_bottom")))
		gmxCreateTag(root, "HTile", str(self.getMember("HTile")))
		gmxCreateTag(root, "VTile", str(self.getMember("VTile")))
		tag=xml.etree.ElementTree.Element("TextureGroups")
		tag.tail="\n"
		root.append(tag)
		gmxCreateTag(root, "For3D", str(self.getMember("For3D")))
		gmxCreateTag(root, "width", str(self.getMember("width")))
		gmxCreateTag(root, "height", str(self.getMember("height")))
		tag=xml.etree.ElementTree.Element("frames")
		tag.tail="\n"
		root.append(tag)
		c=0
		for s in self.subimages:
			if not os.path.exists(os.path.join(gmxdir, "images")):
				#print_notice("creating directory ",os.path.join(gmxdir, "images"))
				os.mkdir(os.path.join(gmxdir, "images"))
			path=os.path.join(gmxdir, "images", self.getMember("name")+"_"+str(c)+".png")
			print_notice("writing image "+path)
			s.getQImage().save(path)
			tag=xml.etree.ElementTree.Element("frame")
			tag.tail="\n"
			tag.text="images\\"+self.getMember("name")+"_"+str(c)+".png"
			tag.set("index",str(c))
			root.append(tag)
			c+=1

	def WriteGmk(self, stream):
		spriteStream = BinaryStream()
		spriteStream.WriteBoolean(self.exists)
		if self.exists:
			spriteStream.WriteString(self.getMember("name"))
			spriteStream.WriteTimestamp()
			spriteStream.WriteDword(800)
			spriteStream.WriteDword(self.getMember("xorigin"))
			spriteStream.WriteDword(self.getMember("yorigin"))
			spriteStream.WriteDword(len(self.subimages))
			for i in range(len(self.subimages)):
				spriteStream.WriteDword(800)
				spriteStream.WriteDword(self.subimages[i].width)
				spriteStream.WriteDword(self.subimages[i].height)
				if self.subimages[i].width != 0 and self.subimages[i].height != 0:
					spriteStream.Serialize(self.subimages[i].getGmkData(), False)
			spriteStream.WriteDword(self.getMember("maskshape"))
			spriteStream.WriteDword(self.getMember("alphatolerance"))
			spriteStream.WriteBoolean(self.getMember("seperatemasks"))
			spriteStream.WriteDword(self.getMember("bboxmode"))
			spriteStream.WriteDword(self.getMember("bbox_left"))
			spriteStream.WriteDword(self.getMember("bbox_right"))
			spriteStream.WriteDword(self.getMember("bbox_bottom"))
			spriteStream.WriteDword(self.getMember("bbox_top"))
		stream.Serialize(spriteStream)

	def WriteGGG(self):
		stri="@sprite "+self.getMember("name")+" {\n"
		for key in self.members:
			if not self.ifDefault(key):
				stri+="\t"+key+"="+str(self.getMember(key))+"\n"
		for o in self.subimages:
			stri=stri+tabStringLines(o.WriteGGG())
		stri+="}\n"
		return stri

	def WriteESSprite(self):
		obj=ESSprite()
		obj.name=self.getMember("name").encode()
		obj.id=self.getMember("id")
		obj.transparent=self.getMember("transparent")
		obj.shape=self.getMember("maskshape")
		obj.alphaTolerance=self.getMember("alphatolerance")
		obj.separateMask=self.getMember("seperatemasks")
		obj.smoothEdges=self.getMember("smoothedges")
		obj.preload=self.getMember("preload")
		obj.originX=self.getMember("xorigin")
		obj.originY=self.getMember("yorigin")
		obj.bbMode=self.getMember("bboxmode")
		obj.bbLeft=self.getMember("bbox_left")
		obj.bbRight=self.getMember("bbox_right")
		obj.bbTop=self.getMember("bbox_top")
		obj.bbBottom=self.getMember("bbox_bottom")
		obj.subImageCount=len(self.subimages)
		ot=(ESSubImage*obj.subImageCount)()
		for count in range(obj.subImageCount):
			me=self.subimages[count].WriteESSubImage(obj.transparent)
			ot[count]=me
		obj.subImages=cast(ot,POINTER(ESSubImage))
		#obj.maskShapes=self.maskShape
		obj.maskShapeCount=0
		return obj

class GameSpriteSubimage(object):
	def __init__(self):
		self.width=0
		self.height=0
		self.qImage=None
		self.gmkData=None
		self.esData=None
		self.useTransp=False

	def getGmkData(self):
		if self.gmkData:
			return self.gmkData
		elif self.qImage:
			width,height,self.gmkData = GameSpriteSubimage.FromQImage(self.qImage)
			return self.gmkData
		else:
			print_error("can't find image data Gmk")

	def getEsData(self):
		if  self.esData:
			return self.esData
		elif self.gmkData:
			self.esData=self.convertGmkIntoEsData()
			return self.esData
		elif self.qImage:
			width,height,self.gmkData = GameSpriteSubimage.FromQImage(self.qImage)
			self.esData=self.convertGmkIntoEsData()
			return self.esData
		else:
			print_error("can't find image data ES")

	def getQImage(self):
		if self.qImage:
			return self.qImage
		elif self.gmkData:
			self.qImage = self.convertGmkDataIntoQImage()
			return self.qImage
		else:
			print_error("can't find image data QImage")

	def setGmkData(self, data):
		if self.gmkData!=data:
			self.qImage=None
			self.gmkData=data
			self.esData=None

	def setQImage(self, q):
		#self.width,self.height,self.data = GameSpriteSubimage.FromQImage(q)
		self.width=q.width()
		self.height=q.height()
		if self.qImage!=q:
			self.qImage=q
			self.gmkData=None
			self.esData=None
		if self.width == 0 or self.height == 0:
			print_error("image size is 0")	

	def convertGmkIntoEsData(self):
		print_warning("slow image conversion")
		self.gmkData.base_stream.seek(0)
		size=self.gmkData.Size()
		data=self.gmkData.base_stream.read()
		cdata=bytearray(data)
		#o.height - 1
		transr = cdata[2]
		transg = cdata[1]
		transb = cdata[3]
		for p in range(0,len(cdata),4):#Gmk BGRA ES RGBA
			cdata[p] = data[p+2]#R
			cdata[p+1] = data[p+1]#G
			cdata[p+2] = data[p]#B
			if self.useTransp and cdata[p+2] == transr and cdata[p+1] == transg and cdata[p+3] == transb:
				cdata[p+3] = 0
			else:
				cdata[p+3] = data[p+3]
		data = zlib.compress(bytes(cdata))
		return data

	def convertGmkDataIntoQImage(self):
		self.getGmkData().base_stream.seek(0)
		data=self.getGmkData().base_stream.read()
		q=QtGui.QImage(self.width,self.height,QtGui.QImage.Format_ARGB32)
		data=bytearray(data)
		for p in range(0,len(data),4):#data from gmk is BGRA, ES gets RGBA
			x=(p/4)%self.width
			y=(p/4)/self.width
			q.setPixel(x,y,data[p+2]<<24 | data[p+1]<<16 | data[p]<<8 | data[p+3])
			q.setPixel(x,y,data[p+3]<<24 | data[p+2]<<16 | data[p+1]<<8 | data[p])
		return q

	@staticmethod
	def FromQImage(q):#QImage is ARGB
		if q.width() == 0 or q.height() == 0:
			return 0,0,None
		datap=q.bits()
		datap.setsize(q.byteCount())
		data = BinaryStream(io.BytesIO(datap))
		data.dd=q
		return q.width(),q.height(),data

	def WriteGGG(self):
		stri="@subimage {\n"
		stri+="\twidth="+str(self.width)+"\n"
		stri+="\theight="+str(self.height)+"\n"
		qImage=self.getQImage()
		ba = QtCore.QByteArray()
		buffer = QtCore.QBuffer(ba)
		buffer.open(QtCore.QIODevice.WriteOnly)
		qImage.save(buffer, "PNG")
		buffer.seek(0)

		import base64
		stri+="\t@data {\n"+str(base64.encodestring(buffer.readData(buffer.size())).decode())+"}\n"
		#stri+="\t@data {\n"+str(self.getGmkData().EncodeBase64().decode())+"}\n"
		stri+="}\n"
		return stri

	def WriteESSubImage(self, useTransp):
		obj=ESSubImage()
		obj.width=self.width
		obj.height=self.height
		self.useTransp=useTransp
		data=self.getEsData()
		obj.data=data
		obj.dataSize=len(data)
		#print_notice("data size "+str(len(data)))
		return obj
