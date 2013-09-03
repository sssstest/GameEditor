#!/usr/bin/env python

#* some gmk code converted to python from https://github.com/DatZach/Gmk

#Copyright (c) 2013 Zachary Reedy
#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

#* some gmk code converted to python from https://github.com/RobertBColton/LateralGM/blob/master/org/lateralgm/file/GmFileReader.java

#* Copyright (C) 2006-2011 IsmAvatar <IsmAvatar@gmail.com>
#* Copyright (C) 2006, 2007, 2008 Clam <clamisgood@gmail.com>
#* Copyright (C) 2007, 2008, 2009 Quadduc <quadduc@gmail.com>
#* Copyright (C) 2013, Robert B. Colton
#* 
#* This file is part of LateralGM.
#* LateralGM is free software and comes with ABSOLUTELY NO WARRANTY.
#* See LICENSE for details.

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

import os.path
import zlib
import zipfile
import random
import subprocess
import xml.etree.ElementTree
import tempfile#gmz
import shutil#gmz
from PyQt4 import QtGui, QtCore#font
from CliApng import *
from CliEefReader import *
from CliPrintColors import *
from CliBinaryStream import *
from CliEnigmaStruct import *
from CliLexer import *

cliDir = "GameEditor/"
Class=1

#converted to python from https://github.com/enigma-dev/enigma-dev/blob/master/pluginsource/org/enigma/EnigmaWriter.java

#* Copyright (C) 2008, 2009 IsmAvatar <IsmAvatar@gmail.com>
#* 
#* Enigma Plugin is free software: you can redistribute it and/or modify
#* it under the terms of the GNU General Public License as published by
#* the Free Software Foundation, either version 3 of the License, or
#* (at your option) any later version.
#* 
#* Enigma Plugin is distributed in the hope that it will be useful,
#* but WITHOUT ANY WARRANTY; without even the implied warranty of
#* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#* GNU General Public License (COPYING) for more details.
#* 
#* You should have received a copy of the GNU General Public License
#* along with this program. If not, see <http://www.gnu.org/licenses/>.

def getActionsCode(actions):
	code=""
	numberOfBraces = 0
	numberOfIfs = 0
	for act in actions:
		#la = act.getLibAction()
		#if (la == null)
		#	print_error("EnigmaWriter.UNSUPPORTED_DND")
		#	continue
		if act.getMember("kind")==GameAction.ACT_BEGIN:
			code+='{'
			numberOfBraces+=1
		elif act.getMember("kind")==GameAction.ACT_CODE:
			#surround with brackets (e.g. for if conditions before it) and terminate dangling comments
			code+='{'+act.argumentValue[0]+"/**/\n}\n"
		elif act.getMember("kind")==GameAction.ACT_ELSE:
			if numberOfIfs > 0:
				code+="else "
				numberOfIfs-=1
		elif act.getMember("kind")==GameAction.ACT_END:
			if numberOfBraces > 0:
				code+='}'
				numberOfBraces-=1
		elif act.getMember("kind")==GameAction.ACT_EXIT:
			code+="exit "
		elif act.getMember("kind")==GameAction.ACT_REPEAT:
			code+="repeat ("+act.argumentValue[0]+") "
		elif act.getMember("kind")==GameAction.ACT_VARIABLE:
			if act.getMember("relative"):
				code+=act.argumentValue[0]+" += "+act.argumentValue[1]+"\n"
			else:
				code+=act.argumentValue[0]+" = "+act.argumentValue[1]+"\n"
		elif act.getMember("kind")==GameAction.ACT_NORMAL:
			if act.getMember("type") == GameAction.EXEC_NONE:
				return ""
			if act.getMember("appliesToSomething") and act.getMember("appliesToObject") != GameObject.OBJECT_SELF:
				if act.question:
					# Question action using with statement
					if act.getMember("appliesToObject") == GameObject.OBJECT_OTHER:
						code+="with (other) "
					elif act.getMember("appliesToObject"):
						code+="with ("+str(act.appliesToObject)+") "
					else:
						code+="/*null with!*/"
				else:
					if act.getMember("appliesToObject") == GameObject.OBJECT_OTHER:
						code+="with (other) {"
						numberOfBraces+=1#clifixed
					elif act.getMember("appliesToObject"):
						code+="with ("+str(act.appliesToObject)+") {"
						numberOfBraces+=1#clifixed
					else:
						code+="/*null with!*/{"
						numberOfBraces+=1#clifixed
			if act.getMember("question"):
				code+="if "
				numberOfIfs+=1
			if act.getMember("notFlag"): code+='!'
			if act.getMember("mayBeRelative"):
				if act.getMember("question"):
					code+="(argument_relative := "+str(act.getMember("relative"))+", "
				else:
					code+="{argument_relative := "+str(act.getMember("relative"))+"; "
					numberOfBraces+=1#clifixed

			if act.getMember("question") and act.getMember("type") == GameAction.EXEC_CODE:
				code+="lib"+str(act.getMember("parentId"))+"_action"+str(act.getMember("id"))
			else:
				code+=act.getMember("functionName")
				if act.getMember("functionCode"):
					code+=act.getMember("functionCode")
			if act.getMember("type") == GameAction.EXEC_FUNCTION:
				code+='('
				for i in xrange(act.getMember("argumentsUsed")):
					if i != 0: code+=','
					code+=argToString(act.argumentValue[i],act.argumentKind[i])
				code+=')'
			if act.getMember("relative"):
				if act.getMember("question"):
					code+=')'
				else:
					code+="\n}"
					numberOfBraces-=1#clifixed
			code+="\n"

			if act.getMember("appliesToSomething") and act.getMember("appliesToObject") != GameObject.OBJECT_SELF and not act.getMember("question"):
				code+="\n}"
				numberOfBraces-=1#clifixed

	if numberOfBraces > 0:
		#someone forgot the closing block action
		for i in xrange(numberOfBraces):
			code+="\n}"
	return code

def argToString(val, kind):
		if kind==Argument.ARG_BOTH:
			#treat as literal if starts with quote (")
			if val.startswith("\"") or val.startswith("'"):
				return val
			#else fall through
		if kind==Argument.ARG_STRING:
			return "\"" + val.replace("\\","\\\\").replace("\"","\"+'\"'+\"") + "\""
		elif kind==Argument.ARG_BOOLEAN:
			return str(not val=="0")
		elif kind==Argument.ARG_MENU:
			return val
		elif kind==Argument.ARG_COLOR:
			return "$"+hex(int(val))
		else:
			if kind == 0:
				return val
			#	return arg.getRes().get().getName()
			#val = "-1"
			return val#clifix name

class Argument(object):
	ARG_EXPRESSION = 0
	ARG_STRING = 1
	ARG_BOTH = 2
	ARG_BOOLEAN = 3
	ARG_MENU = 4
	ARG_COLOR = 13

	ARG_FONTSTRING = 15
	ARG_SPRITE = 5
	ARG_SOUND = 6
	ARG_BACKGROUND = 7
	ARG_PATH = 8
	ARG_SCRIPT = 9
	ARG_GMOBJECT = 10
	ARG_ROOM = 11
	ARG_FONT = 12
	ARG_TIMELINE = 14

def ede_dia_open():
	pass

def ede_dia_add(text):
	pass
	#print_notice("ede_dia_add "+text)

def ede_dia_clear():
	pass

def ede_dia_progress(progress):
	print_notice("ede_dia_progress "+str(progress))

def ede_dia_progress_text(caption):
	print_notice("ede_dia_progress_text "+caption)

def ede_output_redirect_file(filepath):
	print_notice("ede_output_redirect_file "+filepath)

def ede_output_redirect_reset():
	print_notice("ede_output_redirect_reset")

def emptyTextToString(chil):
	if not chil:
		return ""
	return chil

def ifCleanArgumentValue(chil):
	for child in "(),\n":
		if child in chil:
			return False
	return True

def ifWordArgumentValue(chil):
	for child in chil:
		if child not in "1234567890abcdefghijklmnopqrstuvwxyz_":
			return False
	return True

def ABGRtoARGB(color):
	return (color&0xff000000) | ((color&0xff)<<16) | (color&0xff00) | ((color&0xff0000)>>16)

def ARGBtoRGBA(color):
	return ((color&0xff0000)<<8) | ((color&0xff00)<<8) | ((color&0xff)<<8) | ((color&0xff000000)>>24)

def BuildColor(r, g, b):
	return (b << 16) | (g << 8) | r

def tabStringLines(stri,tab="\t"):
	stri="\n".join([tab+y for y in stri.strip().split("\n")])+"\n"
	return stri

def gmxFloat(string):
	return float(string.replace(",","."))

class GameResource(object):
	def __init__(self, gameFile, id=-1):
		self.gameFile=gameFile
		self.exists=True
		self.members={}
		self.listeners=[]
		if id!=-1:
			self.members["id"]=id

	def ifDefault(self, member):
		if not self.defaults.has_key(member):
			print_error("no defalt for "+member)
		if self.defaults[member]==self.getMember(member):
			return True
		return False

	def getMemberId(self, member):
		member=self.getMember(member)
		if member:
			return member.getMember("id")
		else:
			return -1

	def getMember(self, member):
		if self.members.has_key(member):
			return self.members[member]
		elif self.defaults.has_key(member):
			return self.defaults[member]
		else:
			print_error("unsupported member "+member)

	def setMember(self, member, val):
		if not self.defaults.has_key(member):
			print_warning("setting member not in defaults "+member)
		if type(self.defaults[member])!=type(val) and type(self.defaults[member])!=type(None):
			print_error("changed type of "+member+" "+str(type(self.defaults[member]))+" "+str(type(val)))
		if member not in self.members or self.members[member]!=val:
			for callBack in self.listeners:
				callBack("property",member,self.members[member],val)
		self.members[member]=val

	def addListener(self, callBack):
		self.listeners.append(callBack)

	def deleteListener(self, callBack):
		self.listeners.remove(callBack)

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
		for i in xrange(len(images)):
			q=QtGui.QImage()
			q.loadFromData(images[i].read())
			images[i]=q
		for i in xrange(len(images)):
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
						data=open(os.path.join(gmxdir,filep),"r")
						data=data.read()
						q=QtGui.QImage()
						q.loadFromData(data)
						subimage = GameSpriteSubimage()
						subimage.setQImage(q)
						self.subimages.append(subimage)
					else:
						print_error("tag isn't frame "+chil.tag)
				if len(child)==0:
					print_error("no frames")
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
		for c in xrange(count):
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
			for i in xrange(len(self.subimages)):
				spriteStream.WriteDword(800)
				spriteStream.WriteDword(self.subimages[i].width)
				spriteStream.WriteDword(self.subimages[i].height)
				if self.subimages[i].width != 0 and self.subimages[i].height != 0:
					spriteStream.Serialize(self.subimages[i].data, False)
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
		obj.name=self.getMember("name")
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
		for count in xrange(obj.subImageCount):
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
		cdata=""
		#o.height - 1
		transr = data[2]
		transg = data[1]
		transb = data[3]
		for p in xrange(0,len(data),4):#Gmk BGRA ES RGBA
			cdata += data[p+2]#R
			cdata += data[p+1]#G
			cdata += data[p]#B
			if self.useTransp and data[p+2] == transr and data[p+1] == transg and data[p+3] == transb:
				cdata += chr(0)
			else:
				cdata += data[p+3]
		data = zlib.compress(cdata)
		return data

	def convertGmkDataIntoQImage(self):
		self.getGmkData().base_stream.seek(0)
		data=self.getGmkData().base_stream.read()
		q=QtGui.QImage(self.width,self.height,QtGui.QImage.Format_ARGB32)
		for p in xrange(0,len(data),4):#data from gmk is BGRA, ES gets RGBA
			x=(p/4)%self.width
			y=(p/4)/self.width
			q.setPixel(x,y,ord(data[p+2])<<24 | ord(data[p+1])<<16 | ord(data[p])<<8 | ord(data[p+3]))
			q.setPixel(x,y,ord(data[p+3])<<24 | ord(data[p+2])<<16 | ord(data[p+1])<<8 | ord(data[p]))
		return q

	@staticmethod
	def FromQImage(q):#QImage is ARGB
		if q.width() == 0 or q.height() == 0:
			return 0,0,None
		print_notice("image "+str(q.width())+" "+str(q.height()))
		datap=q.bits()
		datap.setsize(q.byteCount())
		data = BinaryStream(cStringIO.StringIO(datap))
		data.dd=q
		return q.width(),q.height(),data

	def WriteGGG(self):
		stri="@subimage {\n"
		stri+="\twidth="+str(self.width)+"\n"
		stri+="\theight="+str(self.height)+"\n"
		#stri+="\tdata="+str(self.data)+"\n"
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
		print_notice("data size "+str(len(data)))
		return obj

class GameSound(GameResource):
	if Class:
		KindNormal=0
		KindBackground=1
		Kind3D=2
		KindMultimedia=3

		EffectNone				= 0x00
		EffectChorus			= 0x01
		EffectEcho				= 0x02
		EffectFlanger			= 0x04
		EffectGargle			= 0x08
		EffectReverb			= 0x10

	defaults={"id":-1,"name":"noname","kind":KindNormal,
	"extension":"","origname":"","effects":EffectNone,
	"volume":1.0,"pan":0.0,"mp3BitRate":0,"oggQuality":0,"preload":True,"data":None}

	def __init__(self, gameFile, id):
		GameResource.__init__(self, gameFile, id)
		self.setMember("name","sound_"+str(id))

	def ReadEgm(self, gmkfile, entry, z):
		stream=z.open(entry+".ey",'r')
		y=YamlParser()
		r=y.parseStream(stream)
		self.setMember("name",os.path.split(entry)[1])
		self.setMember("kind",r.getMkind('KIND'))
		self.setMember("extension",r.getMstr('FILE_TYPE'))
		self.setMember("origname",r.getMstr('FILE_NAME'))
		#CHORUS: false
		#ECHO: false
		#FLANGER: false
		#GARGLE: false
		#REVERB: false
		#self.effects			= r.getMbool('START_FULLSCREEN')
		self.setMember("volume",r.getMreal('VOLUME'))
		self.setMember("pan",r.getMreal('PAN'))
		self.setMember("preload",r.getMbool('PRELOAD'))
		data=r.getMstr('Data')
		data=z.open(os.path.split(entry)[0]+"/"+data,'r')#.read()
		data=data.read()
		self.setMember("data",BinaryStream(cStringIO.StringIO(data)))

	def ReadGmx(self, gmkfile, gmxdir, name):
		tree=xml.etree.ElementTree.parse(os.path.join(gmxdir,name)+".sound.gmx")
		root=tree.getroot()
		if root.tag!="sound":
			print_error("tag isn't sound "+root.tag)
		seen={}
		for child in root:
			if seen.get(child.tag,0)>0:
				print_error("duplicated tag "+child.tag)
			seen[child.tag]=seen.get(child.tag,0)+1
			if child.tag=="kind":
				self.setMember("kind",int(child.text))
			elif child.tag=="extension":
				self.setMember("extension",emptyTextToString(child.text))
			elif child.tag=="origname":
				self.setMember("origname",emptyTextToString(child.text))
			elif child.tag=="effects":
				self.setMember("effects",int(child.text))
			elif child.tag=="volume":
				self.setMember("volume",gmxFloat(child.text))
			elif child.tag=="pan":
				self.setMember("pan",gmxFloat(child.text))
			elif child.tag=="mp3BitRate":
				self.setMember("mp3BitRate",int(child.text))
			elif child.tag=="oggQuality":
				self.setMember("oggQuality",int(child.text))
			elif child.tag=="preload":
				self.setMember("preload",bool(int(child.text)))
			elif child.tag=="data":#<data>snd_0.wav</data>
				name=emptyTextToString(child.text)
				data=open(os.path.join(gmxdir, "audio", name), "r")
				data=data.read()
				self.setMember("data",BinaryStream(cStringIO.StringIO(data)))
			else:
				print_error("unsupported tag "+child.tag)

	def ReadGmk(self, stream):
		soundStream = stream.Deserialize()
		if not soundStream.ReadBoolean():
			self.exists = False
			return
		self.setMember("name",soundStream.ReadString())
		soundStream.ReadTimestamp()
		soundStream.ReadDword()
		self.setMember("kind",soundStream.ReadDword())
		self.setMember("extension",soundStream.ReadString())
		self.setMember("origname",soundStream.ReadString())
		if soundStream.ReadBoolean():
			self.setMember("data",soundStream.Deserialize(False))
		self.setMember("effects",soundStream.ReadDword())
		self.setMember("volume",soundStream.readDouble())
		self.setMember("pan",soundStream.readDouble())
		self.setMember("preload",soundStream.ReadBoolean())

	def WriteGmk(self, stream):
		soundStream = BinaryStream()
		soundStream.WriteBoolean(self.exists)
		if self.exists:
			soundStream.WriteString(self.getMember("name"))
			soundStream.WriteTimestamp()
			soundStream.WriteDword(800)
			soundStream.WriteDword(self.getMember("kind"))
			soundStream.WriteString(self.getMember("extension"))
			soundStream.WriteString(self.getMember("origname"))
			if self.data:
				soundStream.WriteBoolean(True)
				soundStream.Serialize(self.getMember("data"), False)
			else:
				soundStream.WriteBoolean(False)
			soundStream.WriteDword(self.getMember("effects"))
			soundStream.WriteDouble(self.getMember("volume"))
			soundStream.WriteDouble(self.getMember("pan"))
			soundStream.WriteBoolean(self.getMember("preload"))
		stream.Serialize(soundStream)

	def WriteGGG(self):
		stri="@sound "+self.getMember("name")+" {\n"
		for key in self.members:
			if not self.ifDefault(key):
				stri+="\t"+key+"="+str(self.getMember(key))+"\n"
		#stri+="\tdata="+str(self.data)+"\n"
		stri+="}\n"
		return stri

	def WriteESSound(self):
		os=ESSound()
		os.name = self.getMember("name")
		os.id = self.getMember("id")
		os.kind = self.getMember("kind")
		os.fileType = self.getMember("extension")
		os.fileName = self.getMember("origname")
		os.chorus = False
		os.echo = False
		os.flanger = False
		os.gargle = False
		os.reverb = False
		os.volume = self.getMember("volume")
		os.pan = self.getMember("pan")
		os.preload = self.getMember("preload")
		if self.getMember("data") == None:
			os.size = 0
			return os
		self.getMember("data").base_stream.seek(0)
		data = self.getMember("data").base_stream.read()
		os.data = data
		os.size = len(data)
		return os

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
				data=open(os.path.join(gmxdir,filep),"r")
				data=data.read()
				image=QtGui.QImage()
				image.loadFromData(data)
				width,height,data=GameSpriteSubimage.FromQImage(image)
				self.setMember("data",data)
				if width == 0 or height == 0:
					print_error("background size is 0")
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
			print_error("background has no data")

	def WriteGGG(self):
		stri="@background "+self.getMember("name")+"{\n"
		for key in self.members:
			if not self.ifDefault(key):
				stri+="\t"+key+"="+str(self.getMember(key))+"\n"
		#stri+="\tdata="+str(self.getMember("data"))+"\n"
		stri+="}\n"
		return stri

	def WriteESBackground(self):
		obj=ESBackground()
		obj.name=self.getMember("name")
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
					self.setMember("room", self.gameFile.GetResource(GameFile.RtRoom, value))

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
		for i in xrange(count):#Point x,y,speed
			x = pathStream.readDouble()
			y = pathStream.readDouble()
			speed = pathStream.readDouble()

			self.addPoint((x,y,speed))

	def WriteGmk(self, stream):
		pathStream = BinaryStream()
		pathStream.WriteBoolean(exists)
		pathStream.WriteString(self.getMember("name"))
		pathStream.WriteTimestamp()
		pathStream.WriteDword(530)
		pathStream.WriteDword(self.getMember("connectionKind"))
		pathStream.WriteBoolean(self.getMember("closed"))
		pathStream.WriteDword(self.getMember("precision"))
		if self.room:
			pathStream.WriteDword(self.room.getMember("id"))
		else:
			pathStream.WriteDword(GamePath.RoomIndexNone)
		pathStream.WriteDword(self.getMember("snapX"))
		pathStream.WriteDword(self.getMember("snapY"))
		pathStream.WriteDword(len(self.points))
		for i in xrange(len(self.points)):
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
		obj.name=self.getMember("name")
		obj.id=self.getMember("id")
		obj.smooth=self.getMember("connectionKind")
		obj.closed=self.getMember("closed")
		obj.precision=self.getMember("precision")
		obj.snapX=self.getMember("snapX")
		obj.snapY=self.getMember("snapY")
		obj.pointCount=len(self.points)
		ot=(ESPathPoint*obj.pointCount)()
		for count in xrange(obj.pointCount):
			me=ESPathPoint()
			me.x=int(self.points[count][0])#gmk doubles
			me.y=int(self.points[count][1])
			me.speed=int(self.points[count][2])
			ot[count]=me
		obj.points=cast(ot,POINTER(ESPathPoint))
		return obj

	def Finalize(self):
		if self.getMember("roomIndex") != GamePath.RoomIndexNone:
			self.setMember("room", self.gameFile.GetResource(GameFile.RtRoom, self.getMember("roomIndex")))

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
		print_warning("unsupported gmx shaders")

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
		obj.name=self.getMember("name")
		obj.id=self.getMember("id")
		obj.code=self.getMember("value")
		return obj

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
		self.setMember("vertex",z.open(os.path.split(entry)[0]+"/"+r.getMstr('vertex'),'r').read())
		self.setMember("fragment",z.open(os.path.split(entry)[0]+"/"+r.getMstr('fragment'),'r').read())
		self.setMember("type",r.getMstr('type'))
		self.setMember("precompile",r.getMbool('precompile'))

	def WriteGGG(self):
		stri="@shader "+self.getMember("name")+" {\n"
		for key in ["name","id","type","precompile"]:
			if not self.ifDefault(key):
				stri+="\t"+key+"="+str(self.getMember(key))+"\n"
		for x in self.getMember("vertex").split("\n"):
			stri+="\t"+x+"\n"
		for x in self.getMember("fragment").split("\n"):
			stri+="\t"+x+"\n"
		stri+="}\n"
		return stri

	def WriteESShader(self):
		obj=ESShader()
		obj.name=self.getMember("name")
		obj.id=self.getMember("id")
		obj.vertex=self.getMember("vertex")
		obj.fragment=self.getMember("fragment")
		obj.type=self.getMember("type")
		obj.precompile=self.getMember("precompile")
		return obj

class GameFont(GameResource):
	if Class:
		#AntiAliasingLevel
		AaOff = 1
		Aa1 = 2
		Aa2 = 3
		Aa3 = 4

		#CharacterSet
		ANSI_CHARSET		= 0x00
		DEFAULT_CHARSET		= 0x00
		EASTEUROPE_CHARSET	= 0xEE
		RUSSIAN_CHARSET		= 0xCC
		SYMBOL_CHARSET		= 0x02
		SHIFTJIS_CHARSET	= 0x80
		HANGEUL_CHARSET		= 0x81
		GB2312_CHARSET		= 0x86
		CHINESEBIG5_CHARSET	= 0x88
		JOHAB_CHARSET		= 0x82
		HEWBREW_CHARSET		= 0xB1
		ARABIC_CHARSET		= 0xB2
		GREEK_CHARSET		= 0xA1
		TURKISH_CHARSET		= 0xA2
		VIETNAMESE_CHARSET	= 0xA3
		THAI_CHARSET		= 0xDE
		MAC_CHARSET			= 0x4D
		BALTIC_CHARSET		= 0xBA
		OEM_CHARSET			= 0xFF

	defaults={"id":-1,"name":"noname","fontName":"","size":12,"bold":False,"italic":False,
	"characterRangeBegin":32,"characterRangeEnd":127,"characterSet":DEFAULT_CHARSET,"antiAliasing":Aa3,"value":0}

	def __init__(self, gameFile, id):
		GameResource.__init__(self, gameFile, id)
		self.setMember("name","font_"+str(id))

	def ReadEgm(self, gmkfile, entry, z):
		stream=z.open(entry+".ey",'r')
		y=YamlParser()
		r=y.parseStream(stream)
		self.setMember("name",os.path.split(entry)[1])
		self.setMember("fontName",r.getMstr('font_name'))
		self.setMember("bold",r.getMbool('bold'))
		self.setMember("italic",r.getMbool('italic'))
		self.setMember("size",r.getMint('size'))
		self.setMember("characterRangeBegin",r.getMint('range_min'))
		self.setMember("characterRangeEnd",r.getMint('range_max'))
		self.setMember("characterSet",r.getMint('charset'))
		self.setMember("antiAliasing",r.getMint('antialias'))

	def ReadGmx(self, gmkfile, gmxdir, name):
		tree=xml.etree.ElementTree.parse(os.path.join(gmxdir,name)+".font.gmx")
		root=tree.getroot()
		if root.tag!="font":
			print_error("tag isn't font "+root.tag)
		seen={}
		for child in root:
			if seen.get(child.tag,0)>0:
				print_error("duplicated tag "+child.tag)
			seen[child.tag]=seen.get(child.tag,0)+1
			if child.tag=="name":
				self.setMember("fontName",emptyTextToString(child.text))
			elif child.tag=="size":
				self.setMember("size",int(child.text))
			elif child.tag=="bold":
				self.setMember("bold",bool(int(child.text)))
			elif child.tag=="italic":
				self.setMember("italic",bool(int(child.text)))
			elif child.tag=="charset":
				self.setMember("characterSet",int(child.text))
			elif child.tag=="aa":
				self.setMember("antiAliasing",int(child.text))
			elif child.tag=="texgroups":#<texgroup0>0</texgroup0>
				pass
			elif child.tag=="first":
				self.setMember("characterRangeBegin",int(child.text))
			elif child.tag=="last":
				self.setMember("characterRangeEnd",int(child.text))
			elif child.tag=="texgroup":
				pass
			elif child.tag=="ranges":#<range0>32,127</range0>
				pass#self.characterRangeBegin=int(child.text)
				#characterRangeEnd
			elif child.tag=="glyphs":#<glyph character="113" x="11" y="54" w="7" h="17" shift="9" offset="1"/>
				pass
			elif child.tag=="kerningPairs":
				pass
			elif child.tag=="image":
				pass
			else:
				print_error("unsupported tag "+child.tag)

	def ReadGmk(self, stream):
		fontStream = stream.Deserialize()
		if not fontStream.ReadBoolean():
			self.exists = False
			return
		self.setMember("name",fontStream.ReadString())
		fontStream.ReadTimestamp()
		fontStream.ReadDword()
		self.setMember("fontName",fontStream.ReadString())
		self.setMember("size",fontStream.ReadDword())
		self.setMember("bold",fontStream.ReadBoolean())
		self.setMember("italic",fontStream.ReadBoolean())
		self.setMember("value",fontStream.ReadDword())
		self.setMember("characterSet",(self.getMember("value") >> 16) & 0xFF)
		self.setMember("antiAliasing",(self.getMember("value") >> 24) & 0xFF)
		self.setMember("characterRangeBegin",self.getMember("value") & 0xFFFF)
		self.setMember("characterRangeEnd",fontStream.ReadDword())

	def WriteGGG(self):
		stri="@font "+self.getMember("name")+" {\n"
		for key in self.members:
			if not self.ifDefault(key):
				stri+="\t"+key+"="+str(self.getMember(key))+"\n"
		stri+="}\n"
		return stri

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
		for i in xrange(count):
			moment=GameMoment()
			moment.position = timelineStream.ReadDword()
			timelineStream.ReadDword()
			actionCount = timelineStream.ReadDword()
			for i in xrange(actionCount):
				action = GameAction(self.gameFile)
				action.Read(timelineStream)
				moment.actions.append(action)
			self.addMoment(moment)

	def WriteGmk(self, stream):
		timelineStream = BinaryStream()
		timelineStream.WriteBoolean(exists)
		timelineStream.WriteString(name)
		timelineStream.WriteTimestamp()
		timelineStream.WriteDword(500)
		timelineStream.WriteDword(moments.size())
		for i in len(self.moments):
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
		for i in xrange(len(self.moments)):
			for j in len(self.moments[i].actions):
				self.moments[i].actions[j].Finalize()

class GameObject(GameResource):
	if Class:
		OBJECT_SELF = -1
		OBJECT_OTHER = -2
		
		SpriteIndexNone		= -1
		ParentIndexNone		= -100
		MaskIndexNone			= -1

	defaults={"id":-1,"name":"noname","spriteIndex":SpriteIndexNone,"sprite":None,
	"solid":False,"visible":True,"depth":0,"persistent":False,"parentIndex":ParentIndexNone,"parent":None,"maskIndex":MaskIndexNone,"mask":None,
	"PhysicsObject":0,"PhysicsObjectSensor":0,"PhysicsObjectShape":0,"PhysicsObjectDensity":0.0,
	"PhysicsObjectRestitution":0.0,"PhysicsObjectGroup":0,"PhysicsObjectLinearDamping":0.0,"PhysicsObjectAngularDamping":0.0,
	"PhysicsObjectFriction":0.0,"PhysicsObjectAwake":0,"PhysicsObjectKinematic":0,"PhysicsShapePoints":0}

	def __init__(self, gameFile, id):
		GameResource.__init__(self, gameFile, id)
		self.setMember("name","object_"+str(id))
		self.events=[]

	def setMember(self, member, value):
		GameResource.setMember(self, member, value)
		if not self.gameFile.readingFile:
			if member=="spriteIndex":
				if value != GameObject.SpriteIndexNone:
					self.setMember("sprite", self.gameFile.GetResource(GameFile.RtSprite, value))
			elif member=="parentIndex":
				if value not in [GameObject.ParentIndexNone, -1]:
					self.setMember("parent", self.gameFile.GetResource(GameFile.RtObject, value))
			elif member=="maskIndex":
				if value != GameObject.SpriteIndexNone:
					self.setMember("mask", self.gameFile.GetResource(GameFile.RtSprite, value))

	def addEvent(self, event):
		self.events.append(event)
		for callBack in self.listeners:
			callBack("subresource","events",None,None)

	def ReadEgm(self, gmkfile, entry, z):
		stream=z.open(entry+".ey",'r')
		y=YamlParser()
		r=y.parseStream(stream)
		self.setMember("name",os.path.split(entry)[1])
		self.setMember("spriteIndex",r.getMid('SPRITE',gmkfile.egmNameId))
		self.setMember("solid",r.getMbool('SOLID'))
		self.setMember("visible",r.getMbool('VISIBLE'))
		self.setMember("depth",r.getMint('DEPTH'))
		self.setMember("persistent",r.getMbool('PERSISTENT'))
		self.setMember("parentIndex",r.getMid('PARENT',gmkfile.egmNameId))
		self.setMember("maskIndex",r.getMid('MASK',gmkfile.egmNameId))
		data=r.getMstr('Data')
		eef = z.open(os.path.split(entry)[0]+"/"+data,'r')
		e=EEFReader()
		r = e.parseStream(eef)
		r=r.children[0]
		if r.blockName != "Events":
			print_error("block isn't Events "+r.blockName)
		for mevent in r.children:
			event = GameEvent(self.gameFile)
			event.eventNumber = int(mevent.id[1])
			eventKind = mevent.id[0]
			if event.eventNumber==4:
				event.setMember("eventKind", gmkfile.egmNameId[eventKind])
			else:
				if not eventKind.isdigit():
					print_error("eventKind isn't a number "+eventKind)
				event.setMember("eventKind", int(eventKind))
			for eevent in mevent.children:
				actionId=int(eevent.id[0])
				libraryId=int(eevent.id[1])
				action = GameAction(self.gameFile)
				action.setMember("libraryId",libraryId)
				action.setMember("actionId",actionId)
				if libraryId==1:
					if GameAction.actionIdFunctionName.has_key(actionId):
						action.setMember("type",GameAction.EXEC_FUNCTION)
						action.setMember("functionName",GameAction.actionIdFunctionName[actionId])
						i=0
						for a in GameAction.actionIdArgumentKinds[actionId]:
							action.argumentKind[i]=a
							i+=1
						action.setMember("argumentsUsed",len(GameAction.actionIdArgumentKinds[actionId]))
						if GameAction.actionIdKind.has_key(actionId):
							action.setMember("kind",GameAction.actionIdKind[actionId])
						if GameAction.actionIdQuestion.has_key(actionId):
							action.setMember("question",GameAction.actionIdQuestion[actionId])
						if GameAction.actionIdMayBeRelative.has_key(actionId):
							action.setMember("mayBeRelative",GameAction.actionIdMayBeRelative[actionId])
					else:
						print_error("unsupported actionId "+str(actionId))
				else:
					print_error("unsupported libraryId "+str(libraryId))
				event.actions.append(action)
				if libraryId==1 and actionId==603:
					action.argumentValue[0]="".join(eevent.lineAttribs)
				else:
					for i in xrange(len(eevent.lineAttribs)):
						action.argumentValue[i]=eevent.lineAttribs[i].strip()
						if GameAction.actionIdArgumentKinds[actionId][i] in [GameAction.ArgumentKindSprite,GameAction.ArgumentKindSound,GameAction.ArgumentKindBackground,GameAction.ArgumentKindPath,
						GameAction.ArgumentKindScript,GameAction.ArgumentKindObject,GameAction.ArgumentKindRoom,GameAction.ArgumentKindFont,GameAction.ArgumentKindTimeline]:
							action.argumentValue[i]=str(action.GetArgumentReferenceName(i).getMember("id"))
				if len(action.argumentValue) != len(action.argumentKind):
					if action.actionId==603:
						code="\n".join(action.argumentValue)
						action.argumentValue=[code]
					else:
						print_error("argument length")
				for na in eevent.namedAttributes:
					nea = na.strip()
					if nea=="relative":
						action.setMember("relative",True)
			self.addEvent(event)

	def ReadGmx(self, gmkfile, gmxdir, name):
		tree=xml.etree.ElementTree.parse(os.path.join(gmxdir,name)+".object.gmx")
		root=tree.getroot()
		if root.tag!="object":
			print_error("tag isn't object "+root.tag)
		seen={}
		for child in root:
			if seen.get(child.tag,0)>0:
				print_error("duplicated tag "+child.tag)
			seen[child.tag]=seen.get(child.tag,0)+1
			if child.tag=="spriteName":
				self.setMember("spriteIndex",gmkfile.egmNameId[emptyTextToString(child.text)])
			elif child.tag=="solid":
				self.setMember("solid",bool(int(child.text)))
			elif child.tag=="visible":
				self.setMember("visible",bool(int(child.text)))
			elif child.tag=="depth":
				self.setMember("depth",int(child.text))
			elif child.tag=="persistent":
				self.setMember("persistent",bool(int(child.text)))
			elif child.tag=="parentName":
				self.setMember("parentIndex",gmkfile.egmNameId[emptyTextToString(child.text)])
			elif child.tag=="maskName":
				self.setMember("maskIndex",gmkfile.egmNameId[emptyTextToString(child.text)])
			elif child.tag=="events":
				for chil in child:
					if chil.tag=="event":
						event = GameEvent(self.gameFile)
						event.eventNumber = int(chil.attrib["eventtype"])
						if event.eventNumber==4:
							event.setMember("eventKind", gmkfile.egmNameId[chil.attrib["ename"]])
						else:
							event.setMember("eventKind", int(chil.attrib["enumb"]))
						for chile in chil:
							if chile.tag=="action":
								action = GameAction(self.gameFile)
								for chila in chile:
									if chila.tag=="libid":
										action.setMember("libraryId",int(chila.text))
									elif chila.tag=="id":
										action.setMember("actionId",int(chila.text))
									elif chila.tag=="kind":
										action.setMember("kind",int(chila.text))
									elif chila.tag=="userelative":
										action.setMember("mayBeRelative",bool(int(chila.text)))
									elif chila.tag=="isquestion":
										action.setMember("question",bool(int(chila.text)))
									elif chila.tag=="useapplyto":
										action.setMember("appliesToSomething",bool(int(chila.text)))
									elif chila.tag=="exetype":
										action.setMember("type",int(chila.text))
									elif chila.tag=="functionname":
										action.setMember("functionName",emptyTextToString(chila.text))
									elif chila.tag=="codestring":
										action.setMember("functionCode",emptyTextToString(chila.text))
									elif chila.tag=="whoName":
										if chila.text=="self":
											action.setMember("appliesToObject",GameObject.OBJECT_SELF)
										else:
											print_error("gmx object applies to")
										#action.appliesToObject=int(chila.text)
									elif chila.tag=="relative":
										action.setMember("relative",bool(int(chila.text)))
									elif chila.tag=="isnot":
										action.setMember("notFlag",bool(int(chila.text)))
									elif chila.tag=="arguments":
										#<argument><kind>1</kind><string>010000000</string></argument><argument>
										if action.getMember("actionId")<100:
											print_error("unsupported actionId "+str(action.actionId))
										i=0
										for chilaa in chila:
											if chilaa.tag=="argument":
												if chilaa[0].tag!="kind":
													print_error("tag isn't kind "+chilaa[0].tag)
												kind=int(chilaa[0].text)
												action.argumentKind[i]=kind
												value=emptyTextToString(chilaa[1].text).strip()
												action.argumentValue[i]=value
												if kind in [GameAction.ArgumentKindSprite,GameAction.ArgumentKindSound,GameAction.ArgumentKindBackground,GameAction.ArgumentKindPath,
												GameAction.ArgumentKindScript,GameAction.ArgumentKindObject,GameAction.ArgumentKindRoom,GameAction.ArgumentKindFont,GameAction.ArgumentKindTimeline]:
													action.argumentValue[i]=str(action.GetArgumentReferenceName(i).getMember("id"))
												i+=1
									else:
										print_error("unsupported actions "+chila.tag)
								action.setMember("argumentsUsed",len(GameAction.actionIdArgumentKinds[action.getMember("actionId")]))
								event.actions.append(action)
							else:
								print_error("tag isn't action "+chile.tag)
						self.addEvent(event)
					else:
						print_error("tag isn't event "+chil.tag)
			elif child.tag=="PhysicsObject":
				self.setMember("PhysicsObject",int(child.text))
			elif child.tag=="PhysicsObjectSensor":
				self.setMember("PhysicsObjectSensor",int(child.text))
			elif child.tag=="PhysicsObjectShape":
				self.setMember("PhysicsObjectShape",int(child.text))
			elif child.tag=="PhysicsObjectDensity":
				self.setMember("PhysicsObjectDensity",gmxFloat(child.text))
			elif child.tag=="PhysicsObjectRestitution":
				self.setMember("PhysicsObjectRestitution",gmxFloat(child.text))
			elif child.tag=="PhysicsObjectGroup":
				self.setMember("PhysicsObjectGroup",int(child.text))
			elif child.tag=="PhysicsObjectLinearDamping":
				self.setMember("PhysicsObjectLinearDamping",gmxFloat(child.text))
			elif child.tag=="PhysicsObjectAngularDamping":
				self.setMember("PhysicsObjectAngularDamping",gmxFloat(child.text))
			elif child.tag=="PhysicsObjectFriction":
				self.setMember("PhysicsObjectFriction",gmxFloat(child.text))
			elif child.tag=="PhysicsObjectAwake":
				self.setMember("PhysicsObjectAwake",int(child.text))
			elif child.tag=="PhysicsObjectKinematic":
				self.setMember("PhysicsObjectKinematic",int(child.text))
			elif child.tag=="PhysicsShapePoints":
				for chil in child:
					print_warning("PhysicsShapePoints")
			else:
				print_error("unsupported tag "+child.tag)

	def ReadGmk(self, stream):
		objectStream = stream.Deserialize()

		if not objectStream.ReadBoolean():
			self.exists = False
			return

		self.setMember("name",objectStream.ReadString())
		#last changed
		objectStream.ReadTimestamp()
		#GM version needed for the following info
		objectStream.ReadDword()
		self.setMember("spriteIndex",objectStream.readInt32())
		self.setMember("solid",objectStream.ReadBoolean())
		self.setMember("visible",objectStream.ReadBoolean())
		self.setMember("depth",objectStream.readInt32())
		self.setMember("persistent",objectStream.ReadBoolean())
		self.setMember("parentIndex",objectStream.readInt32())
		self.setMember("maskIndex",objectStream.readInt32())
		count = objectStream.ReadDword() + 1
		for i in xrange(count):
			while 1:
				first = objectStream.readInt32()

				if first == -1:
					break

				#12 MainEvents
				event = GameEvent(self.gameFile)
				event.eventNumber = i
				event.setMember("eventKind", first)

				#clifix Event Numb
				objectStream.ReadDword()

				actionCount = objectStream.ReadDword()
				while actionCount>0:
					action = GameAction(self.gameFile)
					action.ReadGmk(objectStream)

					event.actions.append(action)
					actionCount=actionCount-1

				self.addEvent(event)

	def ReadGGG(self, value):
		self.events=[]
		eventNumber=None
		eventKind=None
		event=None
		action=None
		codei=False
		code=""
		tabs=0
		i=0
		c=0
		n=value.find("\n")
		if n>-1:
			l=value[:n]
		else:
			l=value
		while c<len(value):
			if codei:
				i,level,plevel,type=GMLLexer(value[c:],"")
				codel=value[c:c+i-1]
				code=""
				for codel in codel.split("\n"):
					if codel.startswith("\t"*(tabs+2)):
						codel=codel[tabs+2:]
					code+=codel+"\n"
				c=c+i-1
			n=value.find("\n",c)
			if n>-1:
				l=value[c:n]
				chil=c
				c=n+1
			else:
				l=value[c:]
				chil=c
				c=len(value)
			a=l.replace(" ","").split()
			if len(a)>0 and a[0].startswith("@ev_"):
				if a[0][-1] != "{":
					print_error("line "+str(i)+" need { after @event")
				a[0]=a[0][:-1]
				eventName = a[0][4:].split("(")[0]
				eventNumber=GameEvent.eventNameNumber(eventName)
				if eventNumber>1:
					eventKind=a[0][4+len(eventName):]
					if eventKind[0] != "(":
						print_error("line "+str(i)+" need ( before eventKind")
					if eventKind[-1] != ")":
						print_error("line "+str(i)+" need ) after eventKind")
					eventKind=eventKind[1:-1]
					if eventNumber==6:
						eventKind=int(eventKind)
					else:
						eventKind = GameEvent.eventKindNumber(eventNumber,eventKind,self.gameFile)
				else:
					eventKind=0
				event = GameEvent(self.gameFile)
				event.eventNumber = eventNumber
				event.setMember("eventKind", eventKind)
				self.addEvent(event)
				codei=False
				tabs=l.count("\t")
			elif len(a)>0 and a[0].startswith("@action_"):
				action = a[0][1:]
				actionName = action.split("(")[0].strip()
				arguments = action[len(actionName):]
				if arguments[0] != "(":
					print_error("line "+str(i)+" need ( before arguments")
				if arguments[-1] != ")":
					print_error("line "+str(i)+" need ) after arguments")
				argumentsi=arguments[1:-1]
				error,arguments=GMLSplitArguments(argumentsi)
				if error:
					print_error("line "+str(i)+" "+error)
				action = GameAction(self.gameFile)
				event.actions.append(action)
				action.setMember("libraryId",1)
				actionId=GameAction.actionNameId(actionName)
				action.setMember("actionId",actionId)
				#action.setMember("appliesToSomething",True)
				if GameAction.actionIdKind.has_key(actionId):
					action.setMember("kind",GameAction.actionIdKind[actionId])
				action.setMember("functionName",actionName)
				for i in xrange(len(GameAction.actionIdArgumentKinds[actionId])):
					action.argumentKind[i]=GameAction.actionIdArgumentKinds[actionId][i]
					action.argumentValue[i]=arguments[i]
				action.setMember("argumentsUsed",len(GameAction.actionIdArgumentKinds[actionId]))
				if GameAction.actionIdQuestion.has_key(actionId):
					action.setMember("question",GameAction.actionIdQuestion[actionId])
				if GameAction.actionIdMayBeRelative.has_key(actionId):
					action.setMember("mayBeRelative",GameAction.actionIdMayBeRelative[actionId])
				if GameAction.actionIdType.has_key(actionId):
					action.setMember("type",GameAction.actionIdType[actionId])
				else:
					action.setMember("type",1)
				codei=False
				tabs=l.count("\t")
			elif len(a)>0 and a[0].startswith("@comment"):
				print_error("comment")
				codei=False
			elif len(a)>0 and a[0]=="@code{":
				print_notice("line "+str(i)+" start code action")
				codei=True
				tabs=l.count("\t")
			elif len(a)>0 and a[0]=="}":
				if codei:
					codei=False
					print_notice("line "+str(i)+" done code action")
				else:
					print_notice("line "+str(i)+" done event")
					eventNumber=None
					eventKind=None
				if code!="":
					action = GameAction(self.gameFile)
					event.actions.append(action)
					action.setMember("libraryId",1)
					actionId=603
					action.setMember("actionId",actionId)
					if GameAction.actionIdKind.has_key(actionId):
						action.setMember("kind",GameAction.actionIdKind[actionId])
					action.argumentValue[0]=code
					action.setMember("argumentsUsed",len(GameAction.actionIdArgumentKinds[actionId]))
					code=""
			elif len(a)>0 and a[0]=="":
				print_notice("line "+str(i)+" empty")
				pass
			else:
				if codei:
					print_error("code outside of code block")
					print_notice("line "+str(i)+" code")
				else:
					print_error("line "+str(i)+" new code")
					print value[chil:]
					i,level,plevel,type=GMLLexer(value[chil:],"")
					codel=value[chil:chil+i-1]
					code=""
					for codel in codel.split("\n"):
						if codel.startswith("\t"*(tabs+2)):
							codel=codel[tabs+2:]
						code+=codel+"\n"
					c=chil+i-1
			i+=1

	def WriteGmk(self, stream):
		objectStream = BinaryStream()
		
		objectStream.WriteBoolean(self.exists)
		if self.exists:
			objectStream.WriteString(self.getMember("name"))
			objectStream.WriteTimestamp()
			objectStream.WriteDword(430)
			if self.getMember("sprite"):
				objectStream.WriteDword(self.getMember("sprite").getMember("id"))
			else:
				objectStream.WriteDword(GameObject.SpriteIndexNone)
			objectStream.WriteBoolean(self.getMember("solid"))
			objectStream.WriteBoolean(self.getMember("visible"))
			objectStream.WriteDword(self.getMember("depth"))
			objectStream.WriteBoolean(self.getMember("persistent"))
			if self.getMember("parent"):
				objectStream.WriteDword(self.getMember("parent").getMember("id"))
			else:
				objectStream.WriteDword(GameObject.ParentIndexNone)
			if self.getMember("mask"):
				objectStream.WriteDword(self.getMember("mask").getMember("id"))
			else:
				objectStream.WriteDword(GameObject.MaskIndexNone)

			objectStream.WriteDword(11)
			for i in xrange(12):
				for j in xrange(len(self.events)):
					if self.events[j].eventNumber == i:
						objectStream.WriteDword(self.events[j].getMember("eventKind"))
						objectStream.WriteDword(400)

						objectStream.WriteDword(len(self.events[j].actions))
						for k in xrange(len(self.events[j].actions)):
							self.events[j].actions[k].WriteGmk(objectStream)

				objectStream.WriteDword(-1)

		stream.Serialize(objectStream)
		
	def Finalize(self):
		if self.getMember("spriteIndex") != GameObject.SpriteIndexNone:
			self.setMember("sprite", self.gameFile.GetResource(GameFile.RtSprite, self.getMember("spriteIndex")))
		if self.getMember("parentIndex") not in [GameObject.ParentIndexNone, -1]:
			self.setMember("parent", self.gameFile.GetResource(GameFile.RtObject, self.getMember("parentIndex")))
		if self.getMember("maskIndex") != GameObject.MaskIndexNone:
			self.setMember("mask", self.gameFile.GetResource(GameFile.RtSprite, self.getMember("maskIndex")))

		for i in xrange(len(self.events)):
			self.events[i].Finalize()
			for j in xrange(len(self.events[i].actions)):
				self.events[i].actions[j].Finalize()

	def WriteGGG(self, ful=True):
		stri=""
		if ful:
			stri="@object "+self.getMember("name")+" {\n"
		tab=""
		if ful:
			tab="\t"
			for key in self.members:
				if not self.ifDefault(key):
					stri+=tab+key+"="+str(self.getMember(key))+"\n"
		for o in self.events:
			stri=stri+tabStringLines(o.WriteGGG(),tab)
		if ful:
			stri+="}\n"
		return stri

	def WriteESObject(self):
		obj=ESObject()
		obj.name=self.getMember("name")
		obj.id=self.getMember("id")
		obj.spriteId=self.getMemberId("sprite")
		obj.solid=self.getMember("solid")
		obj.visible=self.getMember("visible")
		obj.depth=self.getMember("depth")
		obj.persistent=self.getMember("persistent")
		obj.parentId=self.getMemberId("parent")
		obj.maskId=self.getMemberId("mask")
		obj.mainEventCount=12
		if obj.mainEventCount==0:
			return
		ot=(ESMainEvent*obj.mainEventCount)()
		mes={}
		for ec in self.events:
			if not mes.has_key(ec.eventNumber):
				mes[ec.eventNumber]=[]
			ev=ESEvent()
			ev.code = getActionsCode(ec.actions)
			ev.id = ec.getMember("eventKind")
			mes[ec.eventNumber].append(ev)
		for count in xrange(obj.mainEventCount):
			es=mes.get(count,[])
			me=ESMainEvent()
			me.id=count
			me.eventCount=len(es)
			ote=(ESEvent*me.eventCount)()
			for counte in xrange(me.eventCount):
				ote[counte]=es[counte]
			me.events=cast(pointer(ote),POINTER(ESEvent))
			ot[count]=me
		obj.mainEvents=cast(ot,POINTER(ESMainEvent))
		return obj

class GameEvent(GameResource):
	defaults={"id":-1,"name":"noname","eventKind":0}

	if Class:
		#Gmk eventKind ES Event id
		EnNormal = 0
		EnStepNormal = 0
		EnStepBegin = 1
		EnStepEnd = 2
		EnDrawNormal = 0
		EnDrawGUI = 64
		EnDrawResize = 64
		EnOtherOutsideRoom = 0
		EnOtherIntersectBoundary = 1
		EnOtherGameStart = 2
		EnOtherGameEnd = 3
		EnOtherRoomStart = 4
		EnOtherRoomEnd = 5
		EnOtherNoMoreLives = 6
		EnOtherAnimationEnd = 7
		EnOtherEndOfPath = 8
		EnOtherNoMoreHealth = 9
		EnOtherUser0 = 10
		EnOtherUser1 = 11
		EnOtherUser2 = 12
		EnOtherUser3 = 13
		EnOtherUser4 = 14
		EnOtherUser5 = 15
		EnOtherUser6 = 16
		EnOtherUser7 = 17
		EnOtherUser8 = 18
		EnOtherUser9 = 19
		EnOtherUser10 = 20
		EnOtherUser11 = 21
		EnOtherUser12 = 22
		EnOtherUser13 = 23
		EnOtherUser14 = 24
		EnOtherUser15 = 25
		EnOtherOutsideView0 = 40
		EnOtherOutsideView1 = 41
		EnOtherOutsideView2 = 42
		EnOtherOutsideView3 = 43
		EnOtherOutsideView4 = 44
		EnOtherOutsideView5 = 45
		EnOtherOutsideView6 = 46
		EnOtherOutsideView7 = 47
		EnOtherBoundaryView0 = 50
		EnOtherBoundaryViewView1 = 51
		EnOtherBoundaryViewView2 = 52
		EnOtherBoundaryViewView3 = 53
		EnOtherBoundaryViewView4 = 54
		EnOtherBoundaryViewView5 = 55
		EnOtherBoundaryViewView6 = 56
		EnOtherBoundaryViewView7 = 57
		EnOtherAyscDialog = 63
		EnOtherAyscIAP = 66
		EnOtherAyscCloud = 67
		EnOtherAyscNetworking = 68
		EnKeyboardBackspace = 8
		EnKeyboardEnter = 13
		EnKeyboardShift = 16
		EnKeyboardControl = 17
		EnKeyboardAlt = 18
		EnKeyboardEscape = 27
		EnKeyboardSpace = 32
		EnKeyboardPageUp = 33
		EnKeyboardPageDown = 34
		EnKeyboardEnd = 35
		EnKeyboardHome = 36
		EnKeyboardArrowLeft = 37
		EnKeyboardArrowUp = 38
		EnKeyboardArrowRight = 39
		EnKeyboardArrowDown = 40
		EnKeyboardInsert = 45
		EnKeyboardDelete = 46
		EnKeyboard0 = 48
		EnKeyboard1 = 49
		EnKeyboard2 = 50
		EnKeyboard3 = 51
		EnKeyboard4 = 52
		EnKeyboard5 = 53
		EnKeyboard6 = 54
		EnKeyboard7 = 55
		EnKeyboard8 = 56
		EnKeyboard9 = 57
		EnKeyboardA = 65
		EnKeyboardB = 66
		EnKeyboardC = 67
		EnKeyboardD = 68
		EnKeyboardE = 69
		EnKeyboardF = 70
		EnKeyboardG = 71
		EnKeyboardH = 72
		EnKeyboardI = 73
		EnKeyboardJ = 74
		EnKeyboardK = 75
		EnKeyboardL = 76
		EnKeyboardM = 77
		EnKeyboardN = 78
		EnKeyboardO = 79
		EnKeyboardP = 80
		EnKeyboardQ = 81
		EnKeyboardR = 82
		EnKeyboardS = 83
		EnKeyboardT = 84
		EnKeyboardU = 85
		EnKeyboardV = 86
		EnKeyboardW = 87
		EnKeyboardX = 88
		EnKeyboardY = 89
		EnKeyboardZ = 90
		EnKeyboardKeyPad0 = 96
		EnKeyboardKeyPad1 = 97
		EnKeyboardKeyPad2 = 98
		EnKeyboardKeyPad3 = 99
		EnKeyboardKeyPad4 = 100
		EnKeyboardKeyPad5 = 101
		EnKeyboardKeyPad6 = 102
		EnKeyboardKeyPad7 = 103
		EnKeyboardKeyPad8 = 104
		EnKeyboardKeyPad9 = 105
		EnKeyboardKeyPadMultiply = 106
		EnKeyboardKeyPadAdd = 107
		EnKeyboardKeyPadSubstract = 109
		EnKeyboardKeyPadPeriod = 110
		EnKeyboardKeyPadSlash = 111
		EnKeyboardF1 = 112
		EnKeyboardF2 = 113
		EnKeyboardF3 = 114
		EnKeyboardF4 = 115
		EnKeyboardF5 = 116
		EnKeyboardF6 = 117
		EnKeyboardF7 = 118
		EnKeyboardF8 = 119
		EnKeyboardF9 = 120
		EnKeyboardF10 = 121
		EnKeyboardF11 = 122
		EnKeyboardF12 = 123

		kindNames={0:{0:"NORMAL"},
		3:{#Step
		0:"Normal",1:"Begin",2:"End"},
		8:{#Draw
		0:"Normal",64:"GUI"},
		7:{#Other
		0:"OutsideRoom",1:"IntersectBoundary",2:"GameStart",3:"GameEnd",4:"RoomStart",5:"RoomEnd",6:"NoMoreLives",7:"AnimationEnd",
		8:"EndOfPath",9:"NoMoreHealth",
		10:"User0",11:"User1",12:"User2",13:"User3",14:"User4",15:"User5",16:"User6",17:"User7",
		18:"User8",19:"User9",20:"User10",21:"User11",22:"User12",23:"User13",24:"User14",25:"User15",
		40:"OutsideView0",41:"OutsideView1",42:"OutsideView2",43:"OutsideView3",44:"OutsideView4",45:"OutsideView5",
		46:"OutsideView6",47:"OutsideView7",
		50:"BoundaryView0",51:"BoundaryViewView1",52:"BoundaryViewView2",53:"BoundaryViewView3",
		54:"BoundaryViewView4",55:"BoundaryViewView5",56:"BoundaryViewView6",57:"BoundaryViewView7",
		63:"AyscDialog",66:"AyscIAP",67:"AyscCloud",68:"AyscNetworking"},
		5:{#Keyboard
		8:"Backspace",13:"Enter",16:"Shift",17:"Control",18:"Alt",27:"Escape",32:"Space",33:"PageUp",
		34:"PageDown",35:"End",36:"Home",37:"ArrowLeft",38:"ArrowUp",39:"ArrowRight",40:"ArrowDown",45:"Insert",
		46:"Delete",48:"Keyboard0",49:"Keyboard1",50:"Keyboard2",51:"Keyboard3",52:"Keyboard4",53:"Keyboard5",54:"Keyboard6",
		55:"Keyboard7",56:"Keyboard8",57:"Keyboard9",65:"A",66:"B",67:"C",68:"D",69:"E",
		70:"F",71:"G",72:"H",73:"I",74:"J",75:"K",76:"L",77:"M",
		78:"N",79:"O",80:"P",81:"Q",82:"R",83:"S",84:"T",85:"U",
		86:"V",87:"W",88:"X",89:"Y",90:"Z",96:"KeyPad0",97:"KeyPad1",98:"KeyPad2",
		99:"KeyPad3",100:"KeyPad4",101:"KeyPad5",102:"KeyPad6",103:"KeyPad7",104:"KeyPad8",105:"KeyPad9",106:"KeyPadMultiply",
		107:"KeyPadAdd",109:"KeyPadSubstract",110:"KeyPadPeriod",111:"KeyPadSlash",112:"F1",113:"F2",114:"F3",115:"F4",
		116:"F5",117:"F6",118:"F7",119:"F8",120:"F9",121:"F10",122:"F11",123:"F12"}}

		#Gmk eventNumber ES MainEvent id
		EkCreate = 0
		EkDestroy = 1
		EkAlarm = 2#Gmk eventKind alarm number
		EkStep = 3
		EkCollision = 4
		EkKeyboard = 5#Gmk eventKind key
		EkMouse = 6
		EkOther = 7
		EkDraw = 8
		EkPress = 9#Gmk eventKind key
		EkRelease = 10#Gmk eventKind key
		EkAsyncronous = 11
		EkUnknown = 12

		eventNames=["CREATE","DESTROY","ALARM","STEP","COLLISION","KEYBOARD","MOUSE","OTHER","DRAW","PRESS","RELEASE","ASYNC","UNKNOWN"]

	def __init__(self, gameFile):
		GameResource.__init__(self, gameFile, -1)
		self.eventNumber=0
		self.eventCollisionObject=None
		self.actions=[]

	def setMember(self, member, value):
		GameResource.setMember(self, member, value)
		if not self.gameFile.readingFile:
			if self.eventNumber == 4 and member=="eventKind":
				if value != GameObject.SpriteIndexNone:
					self.eventCollisionObject = self.gameFile.GetResource(GameFile.RtObject, value)

	@staticmethod
	def eventKindNumber(eventNumber,name,gameFile):
		if eventNumber in [9,10]:
			eventNumber=5
		if eventNumber == 4:
			return gameFile.GetResourceName(GameFile.RtObject, name).getMember("id")
		if eventNumber == 2:
			return int(name)
		kindNames=GameEvent.kindNames[eventNumber]
		for i in kindNames.keys():
			if kindNames[i].lower()==name.lower():
				return i
		print_error("unsupported kind name "+name)

	@staticmethod
	def eventNameNumber(name):
		for i in xrange(len(GameEvent.eventNames)):
			if GameEvent.eventNames[i].lower()==name.lower():
				return i
		print_error("unsupported event name "+name)

	def eventNumberName(self, n):
		if n in xrange(13):
			return self.eventNames[n].lower()
		return str(n)

	def eventKindName(self, n, k):
		if n==GameEvent.EkStep:
			return self.kindNames[GameEvent.EkStep].get(k,str(k)).lower()
		elif n in [GameEvent.EkKeyboard,GameEvent.EkPress,GameEvent.EkRelease]:
			return self.kindNames[GameEvent.EkKeyboard].get(k,str(k)).lower()
		elif n==GameEvent.EkOther:
			return self.kindNames[GameEvent.EkOther].get(k,str(k)).lower()
		elif n==GameEvent.EkDraw:
			return self.kindNames[GameEvent.EkDraw].get(k,str(k)).lower()
		elif n==GameEvent.EkAsyncronous:
			return self.kindNames[GameEvent.EkOther].get(k,str(k)).lower()
		return str(k)

	def WriteGGG(self):
		if self.eventNumber in [GameEvent.EkCreate,GameEvent.EkDestroy] and self.getMember("eventKind")==0:
			stri="@ev_"+self.eventNumberName(self.eventNumber)+" {\n"
		elif self.eventNumber == GameEvent.EkCollision:
			if self.eventCollisionObject:
				stri="@ev_"+self.eventNumberName(self.eventNumber)+"("+self.eventCollisionObject.getMember("name")+") {\n"
			else:
				print_warning("collision event didn't find eventCollisionObject "+str(self.getMember("eventKind")))
				stri="@ev_"+self.eventNumberName(self.eventNumber)+"("+self.eventKindName(self.eventNumber,self.getMember("eventKind"))+") {\n"
		else:
			stri="@ev_"+self.eventNumberName(self.eventNumber)+"("+self.eventKindName(self.eventNumber,self.getMember("eventKind"))+") {\n"
		for o in self.actions:
			stri=stri+tabStringLines(o.WriteGGG(len(self.actions)))
		stri+="}\n"
		return stri

	def Finalize(self):
		if self.eventNumber==GameEvent.EkCollision:
			self.eventCollisionObject=self.gameFile.GetResource(GameFile.RtObject, self.getMember("eventKind"))

class GameAction(GameResource):
	if Class:
		ACT_NORMAL = 0
		ACT_BEGIN = 1
		ACT_END = 2
		ACT_ELSE = 3
		ACT_EXIT = 4
		ACT_REPEAT = 5
		ACT_VARIABLE = 6
		ACT_CODE = 7
		ACT_PLACEHOLDER = 8
		ACT_SEPARATOR = 9
		ACT_LABEL = 10

		EXEC_NONE = 0
		EXEC_FUNCTION = 1
		EXEC_CODE = 2

		ARGUMENT_COUNT = 8;

		ActionKindNormal=0
		ActionKindBeginGroup=1
		ActionKindEndGroup=2
		ActionKindElse=3
		ActionKindExit=4
		ActionKindRepeat=5
		ActionKindVariable=6
		ActionKindCode=7

		ArgumentKindExpression=0	#<string>
		ArgumentKindString=1		#<string>test&#xD;..</string>
		ArgumentKindBoth=2		#<string></string>
		ArgumentKindBoolean=3		#<string>0</string>
		ArgumentKindMenu=4		#<string>0</string>
		ArgumentKindSprite=5		#<sprite>-1</sprite>
		ArgumentKindSound=6		#<sound>-1</sound>
		ArgumentKindBackground=7	#<background>-1</background>
		ArgumentKindPath=8		#<path>-1</path>
		ArgumentKindScript=9		#<script>-1</script>
		ArgumentKindObject=10		#<object>-100</object>
		ArgumentKindRoom=11		#<room>-1</room>
		ArgumentKindFont=12		#<font>-1</font>
		ArgumentKindColor=13		#<string>16777215</string><string>255</string>
		ArgumentKindTimeline=14	#<timeline>-1</timeline>
		ArgumentKindFontString=15
		ArgumentKindCount=16

		#ActionType
		AtNothing=0
		AtFunction=1
		AtCode=2

		#AppliesTo
		ApObject		= 0	#// >= 0 refers to an object index
		ApSelf			= -1
		ApOther			= -2

	if Class:
		#kind0 type1 lib actionId
		actionIdFunctionName={}#appliesToObject=-1 relative=False appliesToSomething=True question=False appliesToSomething=False 
		actionIdArgumentKinds={}#notFlag=False
		actionIdKind={}
		actionIdMayBeRelative={}
		actionIdQuestion={}
		actionIdType={}
		actionIdFunctionName[101]="action_move"
		actionIdArgumentKinds[101]=[1,0]
		actionIdMayBeRelative[101]=True
		actionIdFunctionName[102]="action_set_motion"
		actionIdArgumentKinds[102]=[0,0]
		actionIdMayBeRelative[102]=True
		actionIdFunctionName[103]="action_set_hspeed"
		actionIdArgumentKinds[103]=[0]
		actionIdMayBeRelative[103]=True
		actionIdFunctionName[104]="action_set_vspeed"
		actionIdArgumentKinds[104]=[0]
		actionIdMayBeRelative[104]=True
		actionIdFunctionName[105]="action_move_point"
		actionIdArgumentKinds[105]=[0,0,0]
		actionIdMayBeRelative[105]=True
		actionIdFunctionName[107]="action_set_gravity"
		actionIdArgumentKinds[107]=[0,0]
		actionIdMayBeRelative[107]=True
		actionIdFunctionName[108]="action_set_friction"
		actionIdArgumentKinds[108]=[0]
		actionIdMayBeRelative[108]=True
		actionIdFunctionName[109]="action_move_to"
		actionIdArgumentKinds[109]=[0,0]
		actionIdMayBeRelative[109]=True
		actionIdFunctionName[110]="action_move_start"
		actionIdArgumentKinds[110]=[]
		actionIdFunctionName[111]="action_move_random"
		actionIdArgumentKinds[111]=[0,0]
		actionIdFunctionName[112]="action_wrap"
		actionIdArgumentKinds[112]=[4]
		actionIdFunctionName[113]="action_reverse_xdir"
		actionIdArgumentKinds[113]=[]
		actionIdFunctionName[114]="action_reverse_ydir"
		actionIdArgumentKinds[114]=[]
		actionIdFunctionName[115]="action_bounce"
		actionIdArgumentKinds[115]=[4,4]
		actionIdFunctionName[116]="action_move_contact"
		actionIdArgumentKinds[116]=[0,0,4]
		actionIdFunctionName[117]="action_snap"
		actionIdArgumentKinds[117]=[0,0]
		actionIdFunctionName[119]="action_path"
		actionIdArgumentKinds[119]=[8,0,4,4]
		actionIdFunctionName[120]="action_linear_step"
		actionIdArgumentKinds[120]=[0,0,0,4]
		actionIdMayBeRelative[120]=True
		actionIdFunctionName[121]="action_potential_step"
		actionIdArgumentKinds[121]=[0,0,0,4]
		actionIdMayBeRelative[121]=True
		actionIdFunctionName[122]="action_path_position"
		actionIdArgumentKinds[122]=[0]
		actionIdMayBeRelative[122]=True
		actionIdFunctionName[123]="action_path_speed"
		actionIdArgumentKinds[123]=[0]
		actionIdMayBeRelative[123]=True
		actionIdFunctionName[124]="action_path_end"
		actionIdArgumentKinds[124]=[]
		actionIdFunctionName[201]="action_create_object"
		actionIdArgumentKinds[201]=[10,0,0]
		actionIdMayBeRelative[201]=True
		actionIdFunctionName[202]="action_change_object"
		actionIdArgumentKinds[202]=[10,4]
		actionIdFunctionName[203]="action_kill_object"
		actionIdArgumentKinds[203]=[]
		actionIdFunctionName[204]="action_kill_position"
		actionIdArgumentKinds[204]=[0,0]
		actionIdMayBeRelative[204]=True
		actionIdFunctionName[206]="action_create_object_motion"
		actionIdArgumentKinds[206]=[10,0,0,0,0]
		actionIdMayBeRelative[206]=True
		actionIdFunctionName[207]="action_create_object_random"
		actionIdArgumentKinds[207]=[10,10,10,10,0,0]
		actionIdMayBeRelative[207]=True
		actionIdFunctionName[211]="action_sound"
		actionIdArgumentKinds[211]=[6,3]
		actionIdFunctionName[212]="action_end_sound"
		actionIdArgumentKinds[212]=[6]
		actionIdFunctionName[213]="action_if_sound"
		actionIdArgumentKinds[213]=[6]
		actionIdQuestion[213]=True
		actionIdFunctionName[221]="action_previous_room"
		actionIdArgumentKinds[221]=[4]
		#actionIdArgumentKinds[221]=[]#from gmx
		actionIdFunctionName[222]="action_next_room"
		actionIdArgumentKinds[222]=[4]
		#actionIdArgumentKinds[222]=[]#from gmx
		actionIdFunctionName[223]="action_current_room"
		actionIdArgumentKinds[223]=[4]
		#actionIdArgumentKinds[223]=[]#from gmx
		actionIdFunctionName[224]="action_another_room"
		actionIdArgumentKinds[224]=[11,4]
		#actionIdArgumentKinds[223]=[11]#from gmx
		actionIdFunctionName[225]="action_if_previous_room"
		actionIdArgumentKinds[225]=[]
		actionIdQuestion[225]=True
		actionIdFunctionName[226]="action_if_next_room"
		actionIdArgumentKinds[226]=[]
		actionIdQuestion[226]=True
		actionIdFunctionName[301]="action_set_alarm"
		actionIdArgumentKinds[301]=[0,4]
		actionIdQuestion[301]=True#from gmk not
		actionIdFunctionName[302]="action_sleep"#not in gmx
		actionIdArgumentKinds[302]=[0,3]
		actionIdFunctionName[303]="action_set_timeline"#not in gmx
		actionIdArgumentKinds[303]=[14,0]
		actionIdFunctionName[304]="action_set_timeline_position"
		actionIdArgumentKinds[304]=[0]
		actionIdQuestion[304]=True#not from gmx
		actionIdFunctionName[305]="action_timeline_set"#from gmx <userelative>0</userelative>
		actionIdArgumentKinds[305]=[14,0,4,4]
		actionIdFunctionName[306]="action_timeline_start"#from gmx
		actionIdArgumentKinds[306]=[]
		actionIdFunctionName[307]="action_timeline_pause"#from gmx
		actionIdArgumentKinds[307]=[]
		actionIdFunctionName[308]="action_timeline_stop"#from gmx
		actionIdArgumentKinds[308]=[]
		actionIdFunctionName[309]="action_set_timeline_speed"#from gmx
		actionIdArgumentKinds[309]=[0]
		actionIdFunctionName[321]="action_message"
		actionIdArgumentKinds[321]=[2]
		actionIdFunctionName[322]="action_show_info"
		actionIdArgumentKinds[322]=[]
		#from gmx kind=0 exetype=2 <codestring>url_open(argument0);</codestring>
		#actionIdArgumentKinds[322]=[1]#<string>http://www.yoyogames.com</string>
		actionIdFunctionName[323]="action_show_video"#not in gmx
		actionIdArgumentKinds[323]=[2,4,4]
		actionIdFunctionName[331]="action_restart_game"
		actionIdArgumentKinds[331]=[]
		actionIdFunctionName[332]="action_end_game"
		actionIdArgumentKinds[332]=[]
		actionIdFunctionName[333]="action_save_game"
		actionIdArgumentKinds[333]=[2]
		actionIdFunctionName[334]="action_load_game"
		actionIdArgumentKinds[334]=[2]
		actionIdFunctionName[401]="action_if_empty"
		actionIdArgumentKinds[401]=[0,0,4]
		actionIdQuestion[401]=True
		actionIdMayBeRelative[401]=True
		actionIdFunctionName[402]="action_if_collision"
		actionIdArgumentKinds[402]=[0,0,4]
		actionIdQuestion[402]=True
		actionIdMayBeRelative[402]=True
		actionIdFunctionName[403]="action_if_object"
		actionIdArgumentKinds[403]=[10,0,0]
		actionIdQuestion[403]=True
		actionIdMayBeRelative[403]=True
		actionIdFunctionName[404]="action_if_number"
		actionIdArgumentKinds[404]=[10,0,4]
		actionIdQuestion[404]=True
		actionIdFunctionName[405]="action_if_dice"
		actionIdArgumentKinds[405]=[0]
		actionIdQuestion[405]=True
		actionIdFunctionName[407]="action_if_question"
		actionIdArgumentKinds[407]=[2]
		actionIdQuestion[407]=True
		actionIdFunctionName[408]="action_if"
		actionIdArgumentKinds[408]=[0]
		actionIdQuestion[408]=True
		actionIdFunctionName[409]="action_if_mouse"
		actionIdArgumentKinds[409]=[4]
		actionIdQuestion[409]=True
		actionIdFunctionName[410]="action_if_aligned"
		actionIdArgumentKinds[410]=[0,0]
		actionIdQuestion[410]=True
		actionIdFunctionName[421]=""#else
		actionIdArgumentKinds[421]=[]
		actionIdKind[421]=3
		actionIdType[421]=2
		actionIdFunctionName[422]=""#start of block
		actionIdArgumentKinds[422]=[]
		actionIdKind[422]=1
		actionIdType[422]=2
		actionIdFunctionName[423]=""#repeat 3 times
		actionIdArgumentKinds[423]=[0]
		actionIdKind[423]=5
		actionIdType[423]=2
		actionIdFunctionName[424]=""#end of block
		actionIdArgumentKinds[424]=[]
		actionIdKind[424]=2
		actionIdType[424]=2
		actionIdFunctionName[425]=""#exit this event
		actionIdArgumentKinds[425]=[]
		actionIdKind[425]=4
		actionIdType[425]=2
		actionIdFunctionName[500]=""#exetype=2 #clifix type #from gmx #<codestring>draw_self();</codestring>
		actionIdArgumentKinds[500]=[]
		actionIdKind[500]=0
		actionIdFunctionName[501]="action_draw_sprite"
		actionIdArgumentKinds[501]=[5,0,0,0]
		actionIdMayBeRelative[501]=True
		actionIdFunctionName[502]="action_draw_background"
		actionIdArgumentKinds[502]=[7,0,0,3]
		actionIdMayBeRelative[502]=True
		actionIdFunctionName[511]="action_draw_rectangle"
		actionIdArgumentKinds[511]=[0,0,0,0,4]
		actionIdMayBeRelative[511]=True
		actionIdFunctionName[512]="action_draw_ellipse"
		actionIdArgumentKinds[512]=[0,0,0,0,4]
		actionIdMayBeRelative[512]=True
		actionIdFunctionName[513]="action_draw_line"
		actionIdArgumentKinds[513]=[0,0,0,0]
		actionIdMayBeRelative[513]=True
		actionIdFunctionName[514]="action_draw_text"
		actionIdArgumentKinds[514]=[2,0,0]
		actionIdMayBeRelative[514]=True
		actionIdFunctionName[515]="action_draw_arrow"
		actionIdArgumentKinds[515]=[0,0,0,0,0]
		actionIdMayBeRelative[515]=True
		actionIdFunctionName[516]="action_draw_gradient_hor"
		actionIdArgumentKinds[516]=[0,0,0,0,13,13]
		actionIdMayBeRelative[516]=True
		actionIdFunctionName[517]="action_draw_gradient_vert"
		actionIdArgumentKinds[517]=[0,0,0,0,13,13]
		actionIdMayBeRelative[517]=True
		actionIdFunctionName[518]="action_draw_ellipse_gradient"
		actionIdArgumentKinds[518]=[0,0,0,0,13,13]
		actionIdMayBeRelative[518]=True
		actionIdFunctionName[519]="action_draw_text_transformed"
		actionIdArgumentKinds[519]=[2,0,0,0,0,0]
		actionIdMayBeRelative[519]=True
		actionIdFunctionName[524]="action_color"
		actionIdArgumentKinds[524]=[13]
		actionIdFunctionName[526]="action_font"
		actionIdArgumentKinds[526]=[12,4]
		actionIdFunctionName[531]="action_fullscreen"
		actionIdArgumentKinds[531]=[4]
		actionIdFunctionName[532]="action_effect"
		actionIdArgumentKinds[532]=[4,0,0,4,13,4]
		actionIdMayBeRelative[532]=True
		actionIdFunctionName[541]="action_sprite_set"
		actionIdArgumentKinds[541]=[5,0,0]
		actionIdFunctionName[542]="action_sprite_transform"
		actionIdArgumentKinds[542]=[0,0,0,4]
		actionIdFunctionName[543]="action_sprite_color"
		actionIdArgumentKinds[543]=[13,0]
		actionIdFunctionName[601]="action_execute_script"
		actionIdArgumentKinds[601]=[9,0,0,0,0,0]
		actionIdFunctionName[603]=""#code
		actionIdArgumentKinds[603]=[1]
		actionIdKind[603]=7
		actionIdType[603]=2
		actionIdFunctionName[604]="action_inherited"
		actionIdArgumentKinds[604]=[]
		actionIdFunctionName[605]=""#comment
		actionIdArgumentKinds[605]=[1]
		actionIdKind[605]=0
		actionIdType[605]=0
		actionIdFunctionName[611]=""#set var x
		actionIdArgumentKinds[611]=[1]
		#actionIdArgumentKinds[611]=[1,0]#from gmx
		actionIdMayBeRelative[611]=True
		actionIdKind[611]=6
		actionIdType[611]=2
		actionIdFunctionName[612]="action_if_variable"
		actionIdArgumentKinds[612]=[0,0,4]
		actionIdQuestion[612]=True
		actionIdFunctionName[613]="action_draw_variable"
		actionIdArgumentKinds[613]=[0,0,0]
		actionIdMayBeRelative[613]=True
		actionIdFunctionName[701]="action_set_score"
		actionIdArgumentKinds[701]=[0]
		actionIdMayBeRelative[701]=True
		actionIdFunctionName[702]="action_if_score"
		actionIdArgumentKinds[702]=[0,4]
		actionIdQuestion[702]=True
		actionIdFunctionName[703]="action_draw_score"
		actionIdArgumentKinds[703]=[0,0,1]
		actionIdMayBeRelative[703]=True
		actionIdFunctionName[707]="action_highscore_clear"
		actionIdArgumentKinds[707]=[]
		actionIdFunctionName[709]="action_highscore_show"#not in gmx
		actionIdArgumentKinds[709]=[7,4,13,13,15]
		actionIdFunctionName[711]="action_set_life"
		actionIdArgumentKinds[711]=[0]
		actionIdMayBeRelative[711]=True
		actionIdFunctionName[712]="action_if_life"
		actionIdArgumentKinds[712]=[0,4]
		actionIdQuestion[712]=True
		actionIdFunctionName[713]="action_draw_life"
		actionIdArgumentKinds[713]=[0,0,1]
		actionIdMayBeRelative[713]=True
		actionIdFunctionName[714]="action_draw_life_images"
		actionIdArgumentKinds[714]=[0,0,5]
		actionIdMayBeRelative[714]=True
		actionIdFunctionName[721]="action_set_health"
		actionIdArgumentKinds[721]=[0]
		actionIdMayBeRelative[721]=True
		actionIdFunctionName[722]="action_if_health"
		actionIdArgumentKinds[722]=[0,4]
		actionIdQuestion[722]=True
		actionIdFunctionName[723]="action_draw_health"
		actionIdArgumentKinds[723]=[0,0,0,0,4,4]
		actionIdMayBeRelative[723]=True
		actionIdFunctionName[731]="action_set_caption"
		actionIdArgumentKinds[731]=[4,1,4,1,4,1]
		actionIdFunctionName[801]="action_set_cursor"
		actionIdArgumentKinds[801]=[5,4]
		actionIdFunctionName[802]="action_snapshot"
		actionIdArgumentKinds[802]=[2]
		actionIdFunctionName[803]="action_replace_sprite"
		actionIdArgumentKinds[803]=[5,2,0]
		actionIdFunctionName[804]="action_replace_sound"
		actionIdArgumentKinds[804]=[6,2]
		actionIdFunctionName[805]="action_replace_background"
		actionIdArgumentKinds[805]=[7,2]
		actionIdFunctionName[807]="action_webpage"
		actionIdArgumentKinds[807]=[2]
		actionIdFunctionName[808]="action_cd_play"#not in gmx
		actionIdArgumentKinds[808]=[0,0]
		actionIdFunctionName[809]="action_cd_stop"#not in gmx
		actionIdArgumentKinds[809]=[]
		actionIdFunctionName[810]="action_cd_pause"#not in gmx
		actionIdArgumentKinds[810]=[]
		actionIdFunctionName[811]="action_cd_resume"#not in gmx
		actionIdArgumentKinds[811]=[]
		actionIdFunctionName[812]="action_cd_present"#not in gmx
		actionIdArgumentKinds[812]=[]
		actionIdQuestion[812]=True
		actionIdFunctionName[813]="action_cd_playing"#not in gmx
		actionIdArgumentKinds[813]=[]
		actionIdQuestion[813]=True
		actionIdFunctionName[820]="action_partsyst_create"
		actionIdArgumentKinds[820]=[0]
		actionIdFunctionName[821]="action_partsyst_destroy"
		actionIdArgumentKinds[821]=[]
		actionIdFunctionName[822]="action_partsyst_clear"
		actionIdArgumentKinds[822]=[]
		actionIdFunctionName[823]="action_parttype_create"
		actionIdArgumentKinds[823]=[4,4,5,0,0,0]
		actionIdFunctionName[824]="action_parttype_color"
		actionIdArgumentKinds[824]=[4,4,13,13,0,0]
		actionIdFunctionName[826]="action_parttype_life"
		actionIdArgumentKinds[826]=[4,0,0]
		actionIdFunctionName[827]="action_parttype_speed"
		actionIdArgumentKinds[827]=[4,0,0,0,0,0]
		actionIdFunctionName[828]="action_parttype_gravity"
		actionIdArgumentKinds[828]=[4,0,0]
		actionIdFunctionName[829]="action_parttype_secondary"
		actionIdArgumentKinds[829]=[4,4,0,4,0]
		actionIdFunctionName[831]="action_partemit_create"
		actionIdArgumentKinds[831]=[4,4,0,0,0,0]
		actionIdFunctionName[832]="action_partemit_destroy"
		actionIdArgumentKinds[832]=[4]
		actionIdFunctionName[833]="action_partemit_burst"
		actionIdArgumentKinds[833]=[4,4,0]
		actionIdFunctionName[834]="action_partemit_stream"
		actionIdArgumentKinds[834]=[4,4,0]

	defaults={"functionName":"","functionCode":"","libraryId":0,"actionId":0,"kind":0,"type":0,
		  "argumentsUsed":0,"appliesToObject":ApSelf,"relative":False,"appliesToSomething":False,
		  "question":False,"mayBeRelative":False,"notFlag":False}

	def __init__(self, gameFile):
		GameResource.__init__(self, gameFile, -1)
		self.argumentLink=[None,None,None,None,None,None,None,None]
		self.argumentValue=["","","","","","","",""]
		self.argumentKind=[0,0,0,0,0,0,0,0]
		self.appliesObject=None

	def WriteGGG(self, nactions):
		ml=False
		singleaction=False
		for a in self.argumentValue:
			if "\n" in a:
				ml=True
		v=[]
		for a,k in zip(self.argumentValue,self.argumentKind):
			if a.isdigit():
				v.append(a)
			elif ifWordArgumentValue(a):
				v.append(a)
			elif "\n" in a:
				v.append(a+"\n")
			else:
				v.append(a)
		v=v[:self.getMember("argumentsUsed")]
		stri="@action "+str(self.getMember("libraryId"))+" "+str(self.getMember("actionId"))+"{\n"
		if self.getMember("libraryId")==1:
			if self.actionIdFunctionName.has_key(self.getMember("actionId")):
				f=self.actionIdFunctionName[self.getMember("actionId")]
				if self.getMember("functionName")==f:
					if f=="" and self.getMember("libraryId")==1:
						if self.getMember("actionId")==421:
							stri="@else "+",".join(v)+"\n"
							return stri
						elif self.getMember("actionId")==422:
							stri="@start "+",".join(v)+"\n"
							return stri
						elif self.getMember("actionId")==423:
							stri="@repeat "+",".join(v)+"\n"
							return stri
						elif self.getMember("actionId")==424:
							stri="@end "+",".join(v)+"\n"
							return stri
						elif self.getMember("actionId")==425:
							stri="@exitevent "+",".join(v)+"\n"
							return stri
						elif self.getMember("actionId")==611:
							stri="@set "+",".join(v)+"\n"
							return stri
						if self.getMember("actionId")==603:
							if nactions==1:
								stri=""
								singleaction=True
							else:
								stri="@code {\n"
						elif self.getMember("actionId")==605:
							if ml:
								stri="@comment {\n"
							else:
								stri="@comment "+",".join(v)+"\n"
								return stri
					if f!="":
						if f.startswith("action"):
							stri="@"+f
						else:
							print_error("unsupported action "+f)
							stri="@action "+f
						if ml:
							stri+="\n"
						else:
							stri+="("+",".join(v)+")\n"
							#for key in self.members:
							#	if not self.ifDefault(key):
							#		stri+="\t"+key+"="+str(self.getMember(key))+"\n"
							return stri
		else:
			print_error("unsupported libraryId "+str(self.getMember("libraryId")))
		if self.getMember("actionId")==603:
			if len(v)>1:
				print_error("603 more than 1 argument")
			stri+=tabStringLines(v[0],tab="\t")
		else:
			stri+=",".join(v)+"\n"
			if ml:
				print_error("unsupported newline in action arguments "+f)
		if not singleaction:
			stri+="}\n"
		return stri

	@staticmethod
	def actionNameId(name):
		for a in GameAction.actionIdFunctionName.keys():
			if GameAction.actionIdFunctionName[a]==name:
				return a

	def ReadGmk(self, stream):
		# Skip version
		stream.ReadDword()
		self.setMember("libraryId",stream.ReadDword())
		self.setMember("actionId",stream.ReadDword())
		self.setMember("kind",stream.ReadDword())
		#if self.kind == ACT_CODE:
		self.setMember("mayBeRelative",stream.ReadBoolean())
		self.setMember("question",stream.ReadBoolean())
		self.setMember("appliesToSomething",stream.ReadBoolean())
		self.setMember("type",stream.ReadDword())
		#if (la.execType == Action.EXEC_FUNCTION) la.execInfo=
		self.setMember("functionName",stream.ReadString())
		#if (la.execType == Action.EXEC_CODE) la.execInfo=
		self.setMember("functionCode",stream.ReadString())
		self.setMember("argumentsUsed",stream.ReadDword())
		count = stream.ReadDword()
		for i in xrange(count):
			self.argumentKind[i]=stream.ReadDword()
		self.setMember("appliesToObject",stream.readInt32())
		self.setMember("relative",stream.ReadBoolean())
		count = stream.ReadDword()
		for i in xrange(count):
			self.argumentValue[i]=stream.ReadString()
		self.setMember("notFlag",stream.ReadBoolean())

	def WriteGmk(self, stream):
		stream.WriteDword(440)
		stream.WriteDword(self.getMember("libraryId"))
		stream.WriteDword(self.getMember("actionId"))
		stream.WriteDword(self.getMember("kind"))
		stream.WriteBoolean(self.getMember("mayBeRelative"))
		stream.WriteBoolean(self.getMember("question"))
		stream.WriteBoolean(self.getMember("appliesToSomething"))
		stream.WriteDword(self.getMember("type"))
		stream.WriteString(self.getMember("functionName"))
		stream.WriteString(self.getMember("functionCode"))
		stream.WriteDword(self.getMember("argumentsUsed"))
		stream.WriteDword(GameAction.ARGUMENT_COUNT)
		for i in xrange(GameAction.ARGUMENT_COUNT):
			stream.WriteDword(self.argumentKind[i])
		if self.appliesObject == None:
			stream.WriteDword(self.getMember("appliesToObject"))
		else:
			stream.WriteDword(self.appliesObject.getMember("id"))
		stream.WriteBoolean(self.getMember("relative"))
		stream.WriteDword(GameAction.ARGUMENT_COUNT)
		for i in xrange(GameAction.ARGUMENT_COUNT):
			if self.argumentLink[i]:
				stream.WriteString(str(self.argumentLink[i].getMember("id")))
			else:
				stream.WriteString(self.argumentValue[i])
		stream.WriteBoolean(self.getMember("notFlag"))

	def GetArgumentReference(self, index):
		akKinds = [GameFile.RtUnknown,
			GameFile.RtUnknown,
			GameFile.RtUnknown,
			GameFile.RtUnknown,
			GameFile.RtUnknown,
			GameFile.RtSprite,
			GameFile.RtSound,
			GameFile.RtBackground,
			GameFile.RtPath,
			GameFile.RtScript,
			GameFile.RtObject,
			GameFile.RtRoom,
			GameFile.RtFont,
			GameFile.RtUnknown,
			GameFile.RtTimeline]
		if index < GameAction.ARGUMENT_COUNT:
			#self.argumentValue[index] and 
			#if akKinds[self.argumentKind[index]] != GameFile.RtUnknown:
			if self.argumentValue[index].isdigit():
				return self.gameFile.GetResource(akKinds[self.argumentKind[index]], int(self.argumentValue[index]))
			return None
		else:
			return None

	def GetArgumentReferenceName(self, index):
		akKinds = [GameFile.RtUnknown,
			GameFile.RtUnknown,
			GameFile.RtUnknown,
			GameFile.RtUnknown,
			GameFile.RtUnknown,
			GameFile.RtSprite,
			GameFile.RtSound,
			GameFile.RtBackground,
			GameFile.RtPath,
			GameFile.RtScript,
			GameFile.RtObject,
			GameFile.RtRoom,
			GameFile.RtFont,
			GameFile.RtUnknown,
			GameFile.RtTimeline]
		if index < GameAction.ARGUMENT_COUNT:
			#if akKinds[self.argumentKind[index]] != GameFile.RtUnknown:
			if self.argumentValue[index]:
				return self.gameFile.GetResourceName(akKinds[self.argumentKind[index]], self.argumentValue[index])
			return None
		else:
			return None

	def Finalize(self):
		if self.getMember("appliesToObject") >= GameAction.ApObject:
			self.appliesObject = self.gameFile.GetResource(GameFile.RtObject, self.getMember("appliesToObject"))
		else:
			self.appliesObject = None

		for i in xrange(GameAction.ARGUMENT_COUNT):
			self.argumentLink[i] = self.GetArgumentReference(i)

class GameRoomBackground(GameResource):
	defaults={"visible":False,"foreground":False,"imageIndex":-1,"image":None,"x":0,"y":0,"tileHorizontal":True,
		  "tileVertical":True,"speedHorizontal":0,"speedVertical":0,"stretch":False}

	def __init__(self, gameFile):
		GameResource.__init__(self, gameFile, -1)

	def setMember(self, member, value):
		GameResource.setMember(self, member, value)
		if not self.gameFile.readingFile:
			if member=="imageIndex":
				if value != -1:
					self.setMember("image", self.gameFile.GetResource(GameFile.RtBackground, value))

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
			stream.WriteDword(self.self.getMember("image").getMember("id"))
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
			self.setMember("image", self.gameFile.GetResource(GameFile.RtBackground, self.getMember("imageIndex")))

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
		if not self.gameFile.readingFile:
			if member=="objectFollowingIndex":
				if value != -1:
					self.setMember("objectFollowing", self.gameFile.GetResource(GameFile.RtObject, value))

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
			self.setMember("objectFollowing", self.gameFile.GetResource(GameFile.RtObject, self.getMember("objectFollowingIndex")))

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
		if not self.gameFile.readingFile:
			if member=="objectIndex":
				if value != -1:
					self.setMember("object", self.gameFile.GetResource(GameFile.RtObject, value))

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
			stream.WriteDword(self.self.getMember("object").getMember("id"))
		else:
			stream.WriteDword(-1)
		stream.WriteDword(self.getMember("id"))
		stream.WriteString(self.getMember("creationCode"))
		stream.WriteBoolean(self.getMember("locked"))

	def Finalize(self):
		if self.getMember("objectIndex") != -1:
			self.setMember("object", self.gameFile.GetResource(GameFile.RtObject, self.getMember("objectIndex")))

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
		obj.creationCode=self.getMember("creationCode")
		obj.locked=self.getMember("locked")
		return obj

class GameRoomTile(GameResource):
	defaults={"x":0,"y":0,"backgroundIndex":-1,"background":None,"tileX":0,"tileY":0,"width":0,"height":0,"layer":1000000,"id":0,"locked":False}

	def __init__(self, gameFile):
		GameResource.__init__(self, gameFile, -1)

	def setMember(self, member, value):
		GameResource.setMember(self, member, value)
		if not self.gameFile.readingFile:
			if member=="backgroundIndex":
				if value != -1:
					self.setMember("background", self.gameFile.GetResource(GameFile.RtObject, value))

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
			self.setMember("background", self.gameFile.GetResource(GameFile.RtBackground, self.getMember("backgroundIndex")))

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
		stream = BinaryStream(data)
		stream.ReadString()
		nobackgrounds=stream.ReadDword()
		for count in xrange(nobackgrounds):
			background = self.newBackground()
			background.setMember("visible",stream.ReadBoolean())
			background.setMember("foreground",stream.ReadBoolean())
			imageName=stream.ReadString()
			if imageName!="":
				background.setMember("imageIndex",gmkfile.egmNameId[imageName])
			background.setMember("x",stream.ReadDword())
			background.setMember("y",stream.ReadDword())
			background.setMember("tileHorizontal",stream.ReadBoolean())
			background.setMember("tileVertical",stream.ReadBoolean())
			background.setMember("speedHorizontal",stream.ReadDword())
			background.setMember("speedVertical",stream.ReadDword())
			background.setMember("stretch",stream.ReadBoolean())
		noviews=stream.ReadDword()
		for count in xrange(noviews):
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
			view.setMember("objectFollowingIndex",stream.readInt32())
			view.setMember("horizontalSpeed",stream.ReadDword())
			view.setMember("verticalSpeed",stream.ReadDword())
		noinstances=stream.ReadDword()
		for count in xrange(noinstances):
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
		for count in xrange(notiles):
			tile=self.newTile()
			background.setMember("x",stream.ReadDword())
			background.setMember("y",stream.ReadDword())
			background.setMember("backgroundName",stream.ReadString())
			background.setMember("tileX",stream.ReadDword())
			background.setMember("tileY",stream.ReadDword())
			background.setMember("width",stream.ReadDword())
			background.setMember("height",stream.ReadDword())
			background.setMember("layer",stream.ReadDword())
			background.setMember("id",stream.readInt32())
			background.setMember("locked",stream.ReadBoolean())
			print_error("egm tiles unsupported")
			tile = GmkTile()
			tile.ReadGmk(roomStream)

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
					print_error("gmx tiles unsupported")
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
			for i in xrange(len(self.backgrounds)):
				self.backgrounds[i].WriteGmk(roomStream)
			roomStream.WriteBoolean(self.getMember("enableViews"))
			roomStream.WriteDword(len(self.views))
			for i in xrange(len(self.views)):
				self.views[i].WriteGmk(roomStream)
			roomStream.WriteDword(len(self.instances))
			for i in xrange(len(self.instances)):
				self.instances[i].WriteGmk(roomStream)
			roomStream.WriteDword(len(self.tiles))
			for i in xrange(len(self.tiles)):
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
		for i in xrange(len(self.backgrounds)):
			self.backgrounds[i].Finalize()
		for i in xrange(len(self.views)):
			self.views[i].Finalize()
		for i in xrange(len(self.instances)):
			self.instances[i].Finalize()
		for i in xrange(len(self.tiles)):
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
		obj.name=self.getMember("name")
		obj.id=self.getMember("id")
		obj.caption=self.getMember("caption")
		obj.width=self.getMember("width")
		obj.height=self.getMember("height")
		obj.snapX=self.getMember("hsnap")
		obj.snapY=self.getMember("vsnap")
		obj.isometric=self.getMember("isometric")
		obj.speed=self.getMember("speed")
		obj.persistent=self.getMember("persistent")
		obj.backgroundColor=0xff|ARGBtoRGBA(self.getMember("color"))
		obj.drawBackgroundColor=self.getMember("showcolor")
		obj.creationCode=self.getMember("code")
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
		for count in xrange(obj.backgroundDefCount):
			me=self.backgrounds[count].WriteESRoomBackground()
			ot[count]=me
		obj.backgroundDefs=cast(ot,POINTER(ESRoomBackground))
		obj.viewCount=len(self.views)
		ot=(ESRoomView*obj.viewCount)()
		for count in xrange(obj.viewCount):
			me=self.views[count].WriteESRoomView()
			ot[count]=me
		obj.views=cast(ot,POINTER(ESRoomView))
		obj.instanceCount=len(self.instances)
		ot=(ESRoomInstance*obj.instanceCount)()
		for count in xrange(obj.instanceCount):
			me=self.instances[count].WriteESRoomInstance()
			ot[count]=me
		obj.instances=cast(ot,POINTER(ESRoomInstance))
		obj.tileCount=len(self.tiles)
		ot=(ESRoomTile*obj.tileCount)()
		for count in xrange(obj.tileCount):
			me=self.tiles[count].WriteESRoomTile()
			ot[count]=me
		obj.tiles=cast(ot,POINTER(ESRoomTile))
		return obj

class GameTrigger(GameResource):
	if Class:
		MomentMiddle=0
		MomentBegin=1
		MomentEnd=2

	defaults={"id":-1,"name":"noname","condition":"","momentOfChecking":MomentBegin,"constantName":""}

	def __init__(self, gameFile, id):
		GameResource.__init__(self, gameFile, id)

	def ReadGmk(self, stream):
		triggerStream = stream.Deserialize()

		if not triggerStream.ReadBoolean():
			self.exists = False
			return

		triggerStream.ReadDword()
		self.setMember("name", triggerStream.ReadString())
		self.setMember("condition", triggerStream.ReadString())
		self.setMember("momentOfChecking", triggerStream.ReadDword())
		self.setMember("constantName", triggerStream.ReadString())

class GameSettings(GameResource):
	if Class:
		ScalingKeepAspectRatio = -1
		ScalingFullScale=0
		
		#ColorDepth
		CdNoChange=0
		Cd16Bit=1
		Cd32Bit=2
		
		ResolutionNoChange=0
		Resolution320x240=1
		Resolution640x480=2
		Resolution800x600=3
		Resolution1024x768=4
		Resolution1280x1024=5
		Resolution1600x1200=6
		
		FrequencyNoChange=0
		Frequency60=1
		Frequency70=2
		Frequency85=3
		Frequency100=4
		Frequency120=5
		
		PriorityNormal=0
		PriorityHigh=1
		PriorityHighest=2
		
		#LoadingProgressBarType
		LpbtNone=0
		LpbtDefault=1
		LpbtCustom=2
	
	defaults={"id":-1,"fullscreen":False,"interpolate":False,"noborder":False,"showcursor":True,
	"scale":ScalingKeepAspectRatio,"sizeable":False,"stayontop":False,"windowcolor":0,
	"changeresolution":False,"colordepth":CdNoChange,"resolution":ResolutionNoChange,"frequency":FrequencyNoChange,
	"nobuttons":False,"vsync":False,"noscreensaver":True,"fullscreenkey":True,"helpkey":True,"quitkey":True,"savekey":True,#clifix gmx default
	"screenshotkey":True,"closesecondary":True,"priority":PriorityNormal,
	"freeze":False,"showprogress":LpbtDefault,
	"frontImage":None,"backImage":None,"loadImage":None,"loadtransparent":False,"loadalpha":255,"scaleprogress":True,"iconImage":None,
	"displayerrors":True,"writeerrors":False,"aborterrors":False,"treatUninitializedVariablesAsZero":False,"argumenterrors":True,
	"author":"","version":"100","version_information":"","version_major":1,"version_minor":0,"version_release":0,"version_build":0,
	"version_company":"","version_product":"","version_copyright":"","version_description":"",
	"errorFlags":0}

	def __init__(self, gameFile):
		GameResource.__init__(self, gameFile, -1)

	def ReadEgm(self, gmkfile, entry, z):
		stream=z.open(entry+".ey",'r')
		y=YamlParser()
		r=y.parseStream(stream)
		self.setMember("fullscreen",r.getMbool('START_FULLSCREEN'))
		self.setMember("interpolate",r.getMbool('INTERPOLATE'))
		self.setMember("noborder",r.getMbool('DONT_DRAW_BORDER'))
		self.setMember("showcursor",r.getMbool('DISPLAY_CURSOR'))
		self.setMember("scale",r.getMint('SCALING'))
		self.setMember("sizeable",r.getMbool('ALLOW_WINDOW_RESIZE'))
		self.setMember("stayontop",r.getMbool('ALWAYS_ON_TOP'))
		self.setMember("windowcolor",r.getMhex('COLOR_OUTSIDE_ROOM'))
		self.setMember("changeresolution",r.getMbool('SET_RESOLUTION'))
		self.setMember("colordepth",r.getMchange('COLOR_DEPTH'))
		self.setMember("resolution",r.getMchange('RESOLUTION'))
		self.setMember("frequency",r.getMchange('FREQUENCY'))
		self.setMember("nobuttons",r.getMbool('DONT_SHOW_BUTTONS'))
		self.setMember("vsync",r.getMbool('USE_SYNCHRONIZATION'))
		self.setMember("noscreensaver",r.getMbool('DISABLE_SCREENSAVERS'))
		self.setMember("fullscreenkey",r.getMbool('LET_F4_SWITCH_FULLSCREEN'))
		self.setMember("helpkey",r.getMbool('LET_F1_SHOW_GAME_INFO'))
		self.setMember("quitkey",r.getMbool('LET_ESC_END_GAME'))
		self.setMember("savekey",r.getMbool('LET_F5_SAVE_F6_LOAD'))
		self.setMember("screenshotkey",r.getMbool('LET_F9_SCREENSHOT'))
		self.setMember("closesecondary",r.getMbool('TREAT_CLOSE_AS_ESCAPE'))
		self.setMember("priority",r.getMpriority('GAME_PRIORITY'))
		self.setMember("freeze",r.getMbool('FREEZE_ON_LOSE_FOCUS'))
		self.setMember("showprogress",r.getMmode('LOAD_BAR_MODE'))
		#SHOW_CUSTOM_LOAD_IMAGE
		self.setMember("loadtransparent",r.getMbool('IMAGE_PARTIALLY_TRANSPARENTY'))
		self.setMember("loadalpha",r.getMint('LOAD_IMAGE_ALPHA'))
		self.setMember("scaleprogress",r.getMbool('SCALE_PROGRESS_BAR'))
		icon=r.getMstr('Icon')
		iconStream=z.open(icon,"r")
		icon=iconStream.read()
		self.iconImage				= BinaryStream(cStringIO.StringIO(icon))
		self.setMember("displayerrors",r.getMbool('DISPLAY_ERRORS'))
		self.setMember("writeerrors",r.getMbool('WRITE_TO_LOG'))
		self.setMember("aborterrors",r.getMbool('ABORT_ON_ERROR'))
		#self.setMember("errorFlags"
		self.setMember("treatUninitializedVariablesAsZero",r.getMbool('TREAT_UNINIT_AS_0'))
		self.setMember("argumenterrors",r.getMbool('ERROR_ON_ARGS'))
		#LAST_CHANGED
		self.setMember("author",r.getMstr('AUTHOR'))
		self.setMember("version",r.getMstr('VERSION'))
		self.setMember("version_information",r.getMstr('INFORMATION'))
		#INCLUDE_FOLDER
		#OVERWRITE_EXISTING
		#REMOVE_AT_GAME_END
		self.setMember("version_major",r.getMint('VERSION_MAJOR'))
		self.setMember("version_minor",r.getMint('VERSION_MINOR'))
		self.setMember("version_release",r.getMint('VERSION_RELEASE'))
		self.setMember("version_build",r.getMint('VERSION_BUILD'))
		self.setMember("version_company",r.getMstr('COMPANY'))
		self.setMember("version_product",r.getMstr('PRODUCT'))
		self.setMember("version_copyright",r.getMstr('COPYRIGHT'))
		self.setMember("version_description",r.getMstr('DESCRIPTION'))

	def ReadGmk(self, stream):
		settingsStream = stream.Deserialize()
		self.setMember("fullscreen",settingsStream.ReadBoolean())
		self.setMember("interpolate",settingsStream.ReadBoolean())
		self.setMember("noborder",settingsStream.ReadBoolean())
		self.setMember("showcursor",settingsStream.ReadBoolean())
		self.setMember("scale",settingsStream.readInt32())
		self.setMember("sizeable",settingsStream.ReadBoolean())
		self.setMember("stayontop",settingsStream.ReadBoolean())
		self.setMember("windowcolor",settingsStream.ReadDword())
		self.setMember("changeresolution",settingsStream.ReadBoolean())
		self.setMember("colordepth",settingsStream.ReadDword())
		self.setMember("resolution",settingsStream.ReadDword())
		self.setMember("frequency",settingsStream.ReadDword())
		self.setMember("nobuttons",settingsStream.ReadBoolean())
		self.setMember("vsync",settingsStream.ReadBoolean())
		self.setMember("noscreensaver",settingsStream.ReadBoolean())
		self.setMember("fullscreenkey",settingsStream.ReadBoolean())
		self.setMember("helpkey",settingsStream.ReadBoolean())
		self.setMember("quitkey",settingsStream.ReadBoolean())
		self.setMember("savekey",settingsStream.ReadBoolean())
		self.setMember("screenshotkey",settingsStream.ReadBoolean())
		self.setMember("closesecondary",settingsStream.ReadBoolean())
		self.setMember("priority",settingsStream.ReadDword())
		self.setMember("freeze",settingsStream.ReadBoolean())
		self.setMember("showprogress",settingsStream.ReadDword())
		if self.getMember("showprogress") == GameSettings.LpbtCustom:
			self.backImage = 1#settingsStream.ReadBitmap();
			#frontImage = settingsStream.ReadBitmap();
			exists=settingsStream.ReadDword()
			if exists:
				print_warning("settings Back Image")
				data = settingsStream.Deserialize()
			exists=settingsStream.ReadDword()
			if exists:
				print_warning("settings Front Image")
				data = settingsStream.Deserialize()
		if settingsStream.ReadBoolean():
			exists = settingsStream.ReadDword()
			settingsStream.Deserialize()
			#loadImage = settingsStream.ReadBitmap();
		self.setMember("loadtransparent",settingsStream.ReadBoolean())
		self.setMember("loadalpha",settingsStream.ReadDword())
		self.setMember("scaleprogress",settingsStream.ReadBoolean())
		self.iconImage=settingsStream.Deserialize(0)
		self.setMember("displayerrors",settingsStream.ReadBoolean())
		self.setMember("writeerrors",settingsStream.ReadBoolean())
		self.setMember("aborterrors",settingsStream.ReadBoolean())
		self.setMember("errorFlags",settingsStream.ReadDword())
		self.setMember("treatUninitializedVariablesAsZero",(self.getMember("errorFlags") & 0x01) == 0x01)
		self.setMember("argumenterrors",(self.getMember("errorFlags") & 0x02) == 0x02)
		self.setMember("author",settingsStream.ReadString())
		self.setMember("version",settingsStream.ReadString())
		#Last Changed date and time
		settingsStream.ReadTimestamp()
		self.setMember("version_information",settingsStream.ReadString())
		self.setMember("version_major",settingsStream.ReadDword())
		self.setMember("version_minor",settingsStream.ReadDword())
		self.setMember("version_release",settingsStream.ReadDword())
		self.setMember("version_build",settingsStream.ReadDword())
		self.setMember("version_company",settingsStream.ReadString())
		self.setMember("version_product",settingsStream.ReadString())
		self.setMember("version_copyright",settingsStream.ReadString())
		self.setMember("version_description",settingsStream.ReadString())
		#Last time Global Game Settings were changed
		settingsStream.ReadTimestamp()

	def ReadGmx(self, root):
		seen={}
		if root.tag=="options":
			option=""
		elif root.tag=="Config":
			option="option_"
		else:
			print_error("unsupported options root "+root.tag)
		for child in root:
			if seen.get(child.tag,0)>0:
				print_error("duplicated tag "+child.tag)
			seen[child.tag]=seen.get(child.tag,0)+1
			if child.tag==option+"aborterrors":
				self.setMember("aborterrors",child.text=="true")
			elif child.tag==option+"argumenterrors":
				self.setMember("argumenterrors",child.text=="true")
			elif child.tag==option+"author":
				self.setMember("author",emptyTextToString(child.text))
			elif child.tag==option+"backimage":
				pass#self.backImage=
			elif child.tag==option+"changed":pass
			elif child.tag==option+"changeresolution":
				self.setMember("changeresolution",child.text=="true")
			elif child.tag==option+"closeesc":
				self.setMember("closesecondary",child.text=="true")
			elif child.tag==option+"colordepth":
				self.setMember("colordepth",int(child.text))
			elif child.tag==option+"display_name":
				pass#self.gameInformation.setMember("caption",emptyTextToString(child.text))
			elif child.tag==option+"displayerrors":
				self.setMember("displayerrors",child.text=="true")
			elif child.tag==option+"facebook_appid":pass
			elif child.tag==option+"facebook_enable":pass
			elif child.tag==option+"freeze":
				#self.gameInformation.setMember("freeze",child.text=="true")
				self.setMember("freeze",child.text=="true")
			elif child.tag==option+"frequency":
				self.setMember("frequency",int(child.text))
			elif child.tag==option+"frontimage":
				pass#self.frontImage=
			elif child.tag==option+"fullscreen":
				self.setMember("fullscreen",child.text=="true")
			elif child.tag==option+"gameguid":pass
			elif child.tag==option+"gameid":pass
			elif child.tag==option+"GameID":pass
			elif child.tag==option+"GUID":pass
			elif child.tag==option+"haptic_effects":pass
			elif child.tag==option+"hasloadimage":pass
			elif child.tag==option+"helpkey":
				self.setMember("helpkey",child.text=="true")
			elif child.tag==option+"icon":
				pass#self.iconImage=
			elif child.tag==option+"in_app_purchase_enable":pass
			elif child.tag==option+"in_app_purchase_sandbox_mode":pass
			elif child.tag==option+"in_app_purchase_server_url":pass
			elif child.tag==option+"information":
				pass#self.gameInformation.setMember("information",emptyTextToString(child.text))
			elif child.tag==option+"interpolate":
				self.setMember("interpolate",child.text=="true")
			elif child.tag==option+"lastchanged":pass
			elif child.tag==option+"loadalpha":
				self.setMember("loadalpha",int(child.text))
			elif child.tag==option+"loadimage":
				pass#self.loadImage=
			elif child.tag==option+"loadtransparent":
				self.setMember("loadtransparent",child.text=="true")
			elif child.tag==option+"noborder":
				#self.gameInformation.setMember("showborder"
				self.setMember("noborder",child.text=="true")
			elif child.tag==option+"nobuttons":
				self.setMember("nobuttons",child.text=="true")
			elif child.tag==option+"noscreensaver":
				self.setMember("noscreensaver",child.text=="true")
			elif child.tag==option+"priority":
				self.setMember("priority",int(child.text))
			elif child.tag==option+"quitkey":
				self.setMember("quitkey",child.text=="true")
			elif child.tag==option+"resolution":
				self.setMember("resolution",int(child.text))
			elif child.tag==option+"savekey":pass
			elif child.tag==option+"scale":
				self.setMember("scale",int(child.text))
			elif child.tag==option+"scaleprogress":
				self.setMember("scaleprogress",child.text=="true")
			elif child.tag==option+"sci_Password":pass
			elif child.tag==option+"sci_RememberPassword":pass
			elif child.tag==option+"sci_UseSCI":pass
			elif child.tag==option+"sci_UserName":pass
			elif child.tag==option+"sci_serverlocation":pass
			elif child.tag==option+"screenkey":pass
			elif child.tag==option+"screenshotkey":
				self.setMember("screenshotkey",child.text=="true")
			elif child.tag==option+"showcursor":
				self.setMember("showcursor",child.text=="true")
			elif child.tag==option+"showprogress":
				self.setMember("showprogress",int(child.text))
			elif child.tag==option+"sizeable":
				#self.gameInformation.setMember("sizeable",child.text=="true")
				self.setMember("sizeable",child.text=="true")
			elif child.tag==option+"stayontop":
				#self.gameInformation.setMember("alwaysontop",child.text=="true")
				self.setMember("stayontop",child.text=="true")
			elif child.tag==option+"sync_vertex":#clifix
				pass#self.vsync
			elif child.tag==option+"sync":#options
				pass#self.vsync
			elif child.tag==option+"textureGroup_count":pass
			elif child.tag==option+"use_new_audio":pass
			elif child.tag==option+"variableerrors":pass
			elif child.tag==option+"version":
				self.setMember("version",emptyTextToString(child.text))
			elif child.tag==option+"version_build":
				self.setMember("version_build",int(child.text))
			elif child.tag==option+"version_company":
				self.setMember("version_company",emptyTextToString(child.text))
			elif child.tag==option+"version_copyright":
				self.setMember("version_copyright",emptyTextToString(child.text))
			elif child.tag==option+"version_description":
				self.setMember("version_description",emptyTextToString(child.text))
			elif child.tag==option+"version_major":
				self.setMember("version_major",int(child.text))
			elif child.tag==option+"version_minor":
				self.setMember("version_minor",int(child.text))
			elif child.tag==option+"version_product":
				self.setMember("version_product",emptyTextToString(child.text))
			elif child.tag==option+"version_release":
				self.setMember("version_release",int(child.text))
			elif child.tag==option+"windowcolor":#clBlack
				pass#self.windowcolor=
			elif child.tag==option+"writeerrors":
				self.setMember("writeerrors",child.text=="true")
			else:
				if child.tag.startswith(option+"android_"):pass
					#self.setMember("child.tag",child.text)
				elif child.tag.startswith(option+"html5_"):pass
				elif child.tag.startswith(option+"ios_"):pass
				elif child.tag.startswith(option+"linux_"):pass
				elif child.tag.startswith(option+"mac_"):pass
				elif child.tag.startswith(option+"tizen_"):pass
				elif child.tag.startswith(option+"win8_"):pass
				elif child.tag.startswith(option+"windows_"):pass
				elif child.tag.startswith(option+"winphone_"):pass
				elif child.tag.startswith(option+"textureGroup"):pass
				else:
					print_error("unsupported tag "+child.tag)

	def WriteGmk(self, stream):
		settingsStream = BinaryStream()
		settingsStream.WriteBoolean(self.getMember("fullscreen"))
		settingsStream.WriteBoolean(self.getMember("interpolate"))
		settingsStream.WriteBoolean(self.getMember("noborder"))
		settingsStream.WriteBoolean(self.getMember("showcursor"))
		settingsStream.WriteDword(self.getMember("scale"))
		settingsStream.WriteBoolean(self.getMember("sizeable"))
		settingsStream.WriteBoolean(self.getMember("stayontop"))
		settingsStream.writeUInt32(self.getMember("windowcolor"))
		settingsStream.WriteBoolean(self.getMember("changeresolution"))
		settingsStream.WriteDword(self.getMember("colordepth"))
		settingsStream.WriteDword(self.getMember("resolution"))
		settingsStream.WriteDword(self.getMember("frequency"))
		settingsStream.WriteBoolean(self.getMember("nobuttons"))
		settingsStream.WriteBoolean(self.getMember("vsync"))
		settingsStream.WriteBoolean(self.getMember("noscreensaver"))
		settingsStream.WriteBoolean(self.getMember("fullscreenkey"))
		settingsStream.WriteBoolean(self.getMember("helpkey"))
		settingsStream.WriteBoolean(self.getMember("quitkey"))
		settingsStream.WriteBoolean(self.getMember("savekey"))
		settingsStream.WriteBoolean(self.getMember("screenshotkey"))
		settingsStream.WriteBoolean(self.getMember("closesecondary"))
		settingsStream.WriteDword(self.getMember("priority"))
		settingsStream.WriteBoolean(self.getMember("freeze"))
		settingsStream.WriteDword(self.getMember("showprogress"))
		if self.getMember("showprogress") == GameSettings.LpbtCustom:
			print_error("showprogress not none")
			settingsStream.WriteBitmap(self.backImage)
			settingsStream.WriteBitmap(self.frontImage)
		if self.getMember("loadImage") != None:
			print_error("loadimage not none")
			settingsStream.WriteBoolean(True)
			settingsStream.WriteBitmap(self.getMember("loadImage"))
		else:
			settingsStream.WriteBoolean(False)
		settingsStream.WriteBoolean(self.getMember("loadtransparent"))
		settingsStream.WriteDword(self.getMember("loadalpha"))
		settingsStream.WriteBoolean(self.getMember("scaleprogress"))
		settingsStream.Serialize(self.iconImage, False)
		settingsStream.WriteBoolean(self.getMember("displayerrors"))
		settingsStream.WriteBoolean(self.getMember("writeerrors"))
		settingsStream.WriteBoolean(self.getMember("aborterrors"))
		settingsStream.WriteDword(((self.getMember("argumenterrors") & 0x01) << 1) | (self.getMember("treatUninitializedVariablesAsZero") & 0x01))
		settingsStream.WriteString(self.getMember("author"))
		settingsStream.WriteString(self.getMember("version"))
		settingsStream.WriteTimestamp()
		settingsStream.WriteString(self.getMember("version_information"))
		settingsStream.WriteDword(self.getMember("version_major"))
		settingsStream.WriteDword(self.getMember("version_minor"))
		settingsStream.WriteDword(self.getMember("version_release"))
		settingsStream.WriteDword(self.getMember("version_build"))
		settingsStream.WriteString(self.getMember("version_company"))
		settingsStream.WriteString(self.getMember("version_product"))
		settingsStream.WriteString(self.getMember("version_copyright"))
		settingsStream.WriteString(self.getMember("version_description"))
		settingsStream.WriteTimestamp()
		stream.Serialize(settingsStream)

	def WriteGGG(self):
		stri="@settings {\n"
		for key in self.members:
			if not self.ifDefault(key):
				stri+="\t"+key+"="+str(self.getMember(key))+"\n"
		stri+="}\n"
		return stri

	def WriteESGameSettings(self,es):
		og=es.gameSettings
		og.startFullscreen = self.getMember("fullscreen")
		og.interpolate = self.getMember("interpolate")
		og.dontDrawBorder = self.getMember("noborder")
		og.displayCursor = self.getMember("showcursor")
		og.scaling = self.getMember("scale")
		og.allowWindowResize = self.getMember("sizeable")
		og.alwaysOnTop = self.getMember("stayontop")
		og.colorOutsideRoom = ARGBtoRGBA(self.getMember("windowcolor"))
		og.setResolution = self.getMember("changeresolution")
		og.colorDepth = self.getMember("colordepth")
		og.resolution = self.getMember("resolution")
		og.frequency = self.getMember("frequency")
		og.dontShowButtons = self.getMember("nobuttons")
		og.useSynchronization = self.getMember("vsync")
		og.disableScreensavers = self.getMember("noscreensaver")
		og.letF4SwitchFullscreen = self.getMember("fullscreenkey")
		og.letF1ShowGameInfo = self.getMember("helpkey")
		og.letEscEndGame = self.getMember("quitkey")
		og.letF9Screenshot = self.getMember("screenshotkey")
		og.treatCloseAsEscape = self.getMember("closesecondary")#clifix
		og.gamePriority = self.getMember("priority")
		og.freezeOnLoseFocus = self.getMember("freeze")
		og.loadBarMode = self.getMember("showprogress")
		og.imagePartiallyTransparent = self.getMember("loadtransparent")
		og.loadImageAlpha = self.getMember("loadalpha")
		og.scaleProgressBar = self.getMember("scaleprogress")
		og.displayErrors = self.getMember("displayerrors")
		og.writeToLog = self.getMember("writeerrors")
		og.abortOnError = self.getMember("aborterrors")
		og.treatUninitializedAs0 = self.getMember("treatUninitializedVariablesAsZero")
		og.author = self.getMember("author")
		og.version = self.getMember("version")
		og.information = self.getMember("version_information")
		#og.includeFolder = GmFile.GS_INCFOLDER_CODE.get(ig.get(PGameSettings.INCLUDE_FOLDER));
		#og.overwriteExisting = ig.get(PGameSettings.OVERWRITE_EXISTING);
		#og.removeAtGameEnd = ig.get(PGameSettings.REMOVE_AT_GAME_END);
		og.versionMajor = self.getMember("version_major")
		og.versionMinor = self.getMember("version_minor")
		og.versionRelease = self.getMember("version_release")
		og.versionBuild = self.getMember("version_build")
		og.company = self.getMember("version_company")
		og.product = self.getMember("version_product")
		og.copyright = self.getMember("version_copyright")
		og.description = self.getMember("version_description")
		#All this shit is just to write the icon to a temp file and provide the filename...
		"""ICOFile ico = ig.get(PGameSettings.GAME_ICON);
		OutputStream os = null;
		String fn = null;
		if (ico != null) try
			{
			File f = File.createTempFile("gms_ico",".ico");
			ico.write(os = new FileOutputStream(f));
			fn = f.getAbsolutePath();
			}
		catch (IOException e)
			{
			e.printStackTrace();
			}
		finally
			{
			if (os != null) try
				{
				os.close();
				}
			catch (IOException e)
				{
				e.printStackTrace();
				}
			}"""
		og.gameIcon = 0#fn;

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
		if len(self.getMember("information"))>400:
			print_warning("information too big")
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

	def WriteGGG(self):
		stri="@gameinformation {\n"
		for key in self.members:
			if not self.ifDefault(key):
				stri+="\t"+key+"="+str(self.getMember(key))+"\n"
		stri+="}\n"
		return stri

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

	def WriteGmk(stream):
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

class GameTreeNode(object):
	def __init__(self,_status, _group, _index, _name):
		self.index=_index
		self.name=_name
		self.status=_status
		self.group=_group
		self.resource=None
		self.contents=[]

	def Finalize(self,parent):
		groupKind = [
			GameFile.RtUnknown,
			GameFile.RtObject,
			GameFile.RtSprite,
			GameFile.RtSound,
			GameFile.RtRoom,
			GameFile.RtUnknown,
			GameFile.RtBackground,
			GameFile.RtScript,
			GameFile.RtPath,
			GameFile.RtFont,
			GameFile.RtUnknown,
			GameFile.RtUnknown,
			GameFile.RtTimeline,
			GameFile.RtUnknown,
			GameFile.RtShader]
		self.resource = parent.gameFile.GetResource(groupKind[self.group], self.index)
		for i in xrange(len(self.contents)):
			self.contents[i].Finalize(parent)

	def AddResource(self,resource):
		self.index = 0
		self.index = resource.GetId()
		node = GameTreeNode(StatusSecondary, self.group, self.index, self.resource.name)
		node.resource = self.resource
		self.contents.append(node)

	def AddFilter(self,value):
		node = GameTreeNode(StatusGroup, self.group, -1, value)
		self.contents.push_back(node)
		return node

class GameTree(GameResource):
	if Class:
		StatusPrimary = 1
		StatusGroup = 2
		StatusSecondary = 3

		GroupObjects = 1
		GroupSprites = 2
		GroupSounds = 3
		GroupRooms = 4
		GroupBackgrounds = 6
		GroupScripts = 7
		GroupShaders=14
		GroupPaths = 8
		GroupDataFiles = 9
		GroupFonts = GroupDataFiles
		GroupGameInformation = 10
		GroupGameOptions = 11
		GroupGlobalGameOptions = GroupGameOptions
		GroupTimelines = 12
		GroupExtensionPackages = 13
		GroupCount = 15

	def __init__(self, gameFile):
		GameResource.__init__(self, gameFile, -1)
		self.contents=[]

	def ReadGmk(self, stream):
		for i in xrange(12):
			status = stream.ReadDword()
			group = stream.ReadDword()
			stream.ReadDword()
			name = stream.ReadString()
			node = GameTreeNode(status, group, -1, name)
			self.ReadRecursiveTree(stream, node, stream.ReadDword())
			self.contents.append(node)

	def ReadRecursiveTree(self, stream, parent, count):
		for c in xrange(count):
			status = stream.ReadDword()
			group = stream.ReadDword()
			index = stream.ReadDword()
			name = stream.ReadString()
			node = GameTreeNode(status, group, index, name)
			self.ReadRecursiveTree(stream, node, stream.ReadDword())
			parent.contents.append(node)

	def WriteGmk(self, stream):
		for i in xrange(12):
			stream.WriteDword(self.contents[i].status)
			stream.WriteDword(self.contents[i].group)
			stream.WriteDword(0)
			stream.WriteString(self.contents[i].name)
			stream.WriteDword(len(self.contents[i].contents))
			self.WriteRecursiveTree(stream, self.contents[i], len(self.contents[i].contents))

	def WriteRecursiveTree(self, stream, parent, count):
		for i in xrange(count):
			if parent.contents[i].resource == None and parent.contents[i].status != GameTree.StatusGroup:
				if parent.contents[i].status == GameTree.StatusPrimary:
					print_warning("StatusPrimary")
				else:
					print_error("NULL resource \"" + parent.contents[i].name + "\" in resource tree")
			stream.WriteDword(parent.contents[i].status)
			stream.WriteDword(parent.contents[i].group)
			if parent.contents[i].status == GameTree.StatusGroup or parent.contents[i].status == GameTree.StatusPrimary:#fucking StatusPrimary
				stream.WriteDword(0)
				stream.WriteString(parent.contents[i].name)
			else:
				stream.WriteDword(parent.contents[i].resource.getMember("id"))
				stream.WriteString(parent.contents[i].resource.getMember("name"))
			stream.WriteDword(len(parent.contents[i].contents))
			self.WriteRecursiveTree(stream, parent.contents[i], len(parent.contents[i].contents))

	def Finalize(self):
		for i in xrange(len(self.contents)):
			self.contents[i].Finalize(self)

	def PrimaryGroupName(self, name):
		status=GameTree.StatusPrimary
		name=name.lower()
		if name=="objects":
			group=GameTree.GroupObjects
		elif name=="sprites":
			group=GameTree.GroupSprites
		elif name=="sounds":
			group=GameTree.GroupSounds
		elif name=="rooms":
			group=GameTree.GroupRooms
		elif name=="backgrounds" or name=="background":
			group=GameTree.GroupBackgrounds
		elif name=="scripts":
			group=GameTree.GroupScripts
		elif name=="shaders":
			group=GameTree.GroupShaders
		elif name=="paths":
			group=GameTree.GroupPaths
		elif name=="fonts":
			group=GameTree.GroupFonts
		elif name=="game information":
			group=GameTree.GroupGameInformation
			status=GameTree.StatusSecondary
		elif name=="global game settings":
			group=GameTree.GroupGameOptions
			status=GameTree.StatusSecondary
		elif name=="timelines":
			group=GameTree.GroupTimelines
		elif name=="extensions":
			group=GameTree.GroupExtensionPackages
			status=GameTree.StatusSecondary
		else:
			print_error("unsupported group name "+name)
		return group,status

	def AddGroupName(self, name):
		group,status = self.PrimaryGroupName(name)
		node = GameTreeNode(status, group, -1, name)
		self.contents.append(node)
		return node

	def AddResourcePath(self, path, resource):
		p=path.split("/")
		r=self
		status=GameTree.StatusPrimary
		group=0
		for name in p:
			node=None
			for x in r.contents:
				if x.name.lower()==name.lower():
					node=x
					group=node.group
			if node==None:
				if r==self:
					group,status = self.PrimaryGroupName(name)
					if status!=GameTree.StatusPrimary:
						print_error("status isn't StatusPrimary")
				node = GameTreeNode(status, group, -1, name)
				r.contents.append(node)
			r=node
		r.status=GameTree.StatusSecondary
		r.resource=resource
		r.index=resource.getMember("id")

class GameFile(GameResource):
	defaults={"version":0,"gameId":0,"settings":None,"triggers":[]}

	if Class:
		GMK_MAGIC					= 1234321
		GMK_GUID_LENGTH			= 16
		GMK_MAX_ID				= 100000000
		GMK_MIN_INSTANCE_LAST_ID	= 100000
		GMK_MIN_TILE_LAST_ID		= 1000000

		#ResourceType
		RtSprite=0
		RtSound=1
		RtBackground=2
		RtPath=3
		RtScript=4
		RtShader=11
		RtFont=5
		RtTimeline=6
		RtObject=7
		RtRoom=8
		RtUnknown=9
		RtCount=10

		try:
			EnigmaSettingsEy=open(cliDir+"gamesettings.ey","r").read()
		except:
			try:
				EnigmaSettingsEy=open("gamesettings.ey","r").read()
			except:
				print_error("can't find gamesettings.ey")
		#extensions: Universal_System/Extensions/Alarms,Universal_System/Extensions/Timelines,Universal_System/Extensions/Paths,Universal_System/Extensions/MotionPlanning,Universal_System/Extensions/DateTime,Universal_System/Extensions/ParticleSystems,Universal_System/Extensions/DataStructures

	def __init__(self):
		GameResource.__init__(self, self, -1)
		self.version=0
		self.gameId=0
		self.settings=None
		self.triggers=[]
		self.constants=[]
		self.sounds=[]
		self.sprites=[]
		self.backgrounds=[]
		self.paths=[]
		self.scripts=[]
		self.shaders=[]
		self.fonts=[]
		self.timelines=[]
		self.objects=[]
		self.rooms=[]
		self.lastInstancePlacedId=self.GMK_MIN_INSTANCE_LAST_ID
		self.lastTilePlacedId=self.GMK_MIN_TILE_LAST_ID
		self.includeFiles=[]
		self.packages=[]
		self.gameInformation=None
		self.resourceTree=None
		#self.settings = Settings()
		#self.gameInformation = GameInformation()
		#self.resourceTree = Tree()
		self.gameId = random.randint(0,2147483647) % self.GMK_MAX_ID;
		self.readingFile=False

	def addSprite(self, point):
		if point in self.sprites:
			print_error("add duplicate")
		self.sprites.append(point)
		for callBack in self.listeners:
			callBack("subresource","sprites",None,None)

	def addObject(self, point):
		if point in self.objects:
			print_error("add duplicate")
		self.objects.append(point)
		for callBack in self.listeners:
			callBack("subresource","objects",None,None)

	def addRoom(self, point):
		if point in self.sprites:
			print_error("add duplicate")
		self.rooms.append(point)
		for callBack in self.listeners:
			callBack("subresource","rooms",None,None)

	def newSprite(self):
		instance = GameSprite(self, self.GetResourceHighestId(GameFile.RtSprite)+1)
		self.addSprite(instance)
		return instance

	def newObject(self):
		instance = GameObject(self, self.GetResourceHighestId(GameFile.RtObject)+1)
		self.addObject(instance)
		return instance

	def newRoom(self):
		instance = GameRoom(self, self.GetResourceHighestId(GameFile.RtRoom)+1)
		self.addRoom(instance)
		return instance

	def newSettings(self):
		self.settings = GameSettings(self)
		return self.settings

	def newGameInformation(self):
		self.gameInformation = GameInformation(self)
		return self.gameInformation

	def compileRunEnigma(self, exePath, emode):
		es=self.WriteES()
		GameFile.compileRunES(es, exePath, emode)
		
	@staticmethod
	def compileRunES(es, exePath, emode):
		result=definitionsModified("", GameFile.EnigmaSettingsEy)
		print_notice("definitions "+str(result[0].err_str))
		if Class:#trick compileEGMf into using fixed make
			gcliDir=os.path.join(os.getcwd(),cliDir)
			if gcliDir not in os.environ["PATH"]:
				path=gcliDir+":"+os.environ["PATH"]
				os.environ["PATH"]=path
				if os.getenv("PATH")!=path:
					print_error("can't set PATH "+path)
		cError = compileEGMf(es, exePath, emode)
		if cError>0:
			print_error("compileEGMf error "+str(cError))
		else:
			print_notice("compileEGMf done "+str(cError))

	def ReadEgm(self, f):
		z=zipfile.ZipFile(f,'r')
		self.egmNames=z.namelist()
		self.guid=[1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 0, 0, 0, 0, 0, 0]
		self.resourceTree = GameTree(self)
		self.resourceTree.AddGroupName("Sprites")
		self.resourceTree.AddGroupName("Sounds")
		self.resourceTree.AddGroupName("Backgrounds")
		self.resourceTree.AddGroupName("Paths")
		self.resourceTree.AddGroupName("Scripts")
		self.resourceTree.AddGroupName("Fonts")
		self.resourceTree.AddGroupName("Timelines")
		self.resourceTree.AddGroupName("Objects")
		self.resourceTree.AddGroupName("Rooms")
		self.resourceTree.AddGroupName("Game Information")
		self.resourceTree.AddGroupName("Global Game Settings")
		self.resourceTree.AddGroupName("Extensions")
		self.egmId={}
		self.egmNameId={}
		res={}
		self.egmEntries=[]
		self.egmReadNodeChildren(z,res,"notype","")
		for e in self.egmEntries:
			self.egmProcesEntry(*e)
		self.Finalize()

	def egmReadNodeChildren(self, z, parent, kind, dir):
		if dir=="":
			f=z.open("toc.txt",'r')
		else:
			f=z.open(dir+"/toc.txt",'r')
		toc=[]
		for t in f.readlines():
			entry = t.strip()
			if len(entry) > 4 and entry[3] == ' ':
				kind,entry = entry[0:3],entry[4:]
			toc.append((kind,entry))
		self.egmProcessEntries(z,parent,toc,dir);

	def egmProcessEntries(self, z, parent, entries, dir):
		for kind,entry in entries:
			if dir!="":
				entry = dir + '/' + entry
			if entry+"/toc.txt" in self.egmNames:
				parent[entry]={}
				self.egmReadNodeChildren(z,parent[entry],kind,entry);
			else:
				if entry+".ey" in self.egmNames:#if (f.exists())
					parent[entry]={}
					self.egmId[kind]=self.egmId.get(kind,-1)+1
					self.egmNameId[os.path.split(entry)[1]]=self.egmId[kind]
					self.egmEntries.append((z,kind,entry,self.egmId[kind]))
				else:
					print_error("Extraneous TOC entry: "+entry)

	def egmProcesEntry(self, z, kind, entry, id):
		if kind=="EGS":
			pass
		elif kind=="GMS":
			self.settings = GameSettings(self)
			self.settings.ReadEgm(self,entry,z)
		# Load triggers
		# Load constants
		elif kind=="SND":
			s = GameSound(self,id)
			s.ReadEgm(self,entry,z)
			self.sounds.append(s)
			self.resourceTree.AddResourcePath(entry,s)
		elif kind=="SPR":
			s = GameSprite(self,id)
			s.ReadEgm(self,entry,z)
			self.sprites.append(s)
			self.resourceTree.AddResourcePath(entry,s)
		elif kind=="BKG":
			s = GameBackground(self,id)
			s.ReadEgm(self,entry,z)
			self.backgrounds.append(s)
			self.resourceTree.AddResourcePath(entry,s)
		elif kind=="PTH":
			s = GamePath(self,id)
			s.ReadEgm(self,entry,z)
			self.paths.append(s)
			self.resourceTree.AddResourcePath(entry,s)
		elif kind=="SCR":
			s = GameScript(self,id)
			s.ReadEgm(self,entry,z)
			self.scripts.append(s)
			self.resourceTree.AddResourcePath(entry,s)
		elif kind=="SHR":
			s = GameShader(self,id)
			s.ReadEgm(self,entry,z)
			self.shaders.append(s)
			self.resourceTree.AddResourcePath(entry,s)
		elif kind=="FNT":
			s = GameFont(self,id)
			s.ReadEgm(self,entry,z)
			self.fonts.append(s)
			self.resourceTree.AddResourcePath(entry,s)
		elif kind=="TML":
			s = GameTimeline(self,id)
			s.ReadEgm(self,entry,z)
			self.timelines.append(s)
			self.resourceTree.AddResourcePath(entry,s)
		elif kind=="OBJ":
			s = GameObject(self,id)
			s.ReadEgm(self,entry,z)
			self.objects.append(s)
			self.resourceTree.AddResourcePath(entry,s)
		elif kind=="RMM":
			s = GameRoom(self,id)
			s.ReadEgm(self,entry,z)
			self.rooms.append(s)
			self.resourceTree.AddResourcePath(entry,s)
		# Load last ids
		# Load include files
		# Load packages
		elif kind=="GMI":
			self.gameInformation = GameInformation(self)
			self.gameInformation.ReadEgm(self,entry,z)
		# Read library creation code -- we should be able to safely ignore this
		# Read room execution order -- this too
		# Read resource tree
		elif kind=="EXT":
			pass
		else:
			print_error("unsupported toc.txt kind "+kind)

	def ReadGmz(self, filename):
		tempDir=tempfile.mkdtemp()
		print_notice("temp dir "+tempDir)
		print_notice(subprocess.check_output(["7zr", "x","-o"+tempDir,filename]))
		x=subprocess.check_output("ls "+os.path.join(tempDir,"*.project.gmx"),shell=True).strip()
		self.ReadGmx(x)
		#if tempDir.startswith("/tmp/tmp"):
		#	shutil.rmtree(tempDir)
		#else:
		#	print_error("wrong dir"+tempDir)

	def ReadGmxConfig(self, gmkfile, gmxdir, name):
		tree=xml.etree.ElementTree.parse(os.path.join(gmxdir,name)+".config.gmx")
		root=tree.getroot()
		if root.tag!="Config":
			print_error("tag isn't Config "+root.tag)
		self.settings = GameSettings(self)
		self.gameInformation = GameInformation(self)
		self.settings.ReadGmx(root)

	def ReadGmxResourceNames(self, names, name, child, path, nameId):
		c=0
		for chil in child:
			if chil.tag==name:
				filep=chil.text.replace("\\","/")
				iname=os.path.split(filep)[1]
				iname=os.path.splitext(iname)[0]
				nameId[iname]=c
				c+=1
			elif chil.tag==names:
				self.ReadGmxResourceNames(names, name, chil, path+"/"+chil.attrib["name"],nameId)
			else:
				print_error("tag is "+chil.tag+" "+name)

	def ReadGmxResources(self, names, name, child, path, gmxdir):
		c=0
		for chil in child:
			if chil.tag==name:
				filep=chil.text.replace("\\","/")
				p,iname=os.path.split(filep)
				p=os.path.join(gmxdir,p)
				if name=="sound":
					s = GameSound(self,c)
					self.sounds.append(s)
				elif name=="sprite":
					s = GameSprite(self,c)
					self.sprites.append(s)
				elif name=="background":
					s = GameBackground(self,c)
					self.backgrounds.append(s)
				elif name=="path":
					s = GamePath(self,c)
					self.paths.append(s)
				elif name=="script":
					s = GameScript(self,c)
					self.scripts.append(s)
				elif name=="font":
					s = GameFont(self,c)
					self.fonts.append(s)
				elif name=="object":
					s = GameObject(self,c)
					self.objects.append(s)
				elif name=="timeline":
					s = GameTimeline(self,c)
					self.timelines.append(s)
				elif name=="room":
					s = GameRoom(self,c)
					self.rooms.append(s)
				else:
					print_error("unsupported resource "+name)
				s.setMember("name",iname)
				s.ReadGmx(self,p,iname)
				if filep.startswith("sound/"):
					filep="Sounds/"+filep[6:]
				self.resourceTree.AddResourcePath(filep,s)
				c+=1
			elif chil.tag==names:
				self.ReadGmxResources(names, name, chil, path+"/"+chil.attrib["name"], gmxdir)
			else:
				print_error("tag is "+chil.tag+" "+name)

	def GmxSplitPath(self, filename):
		if os.path.isdir(filename):
			if filename[-1] in ["/","\\"]:
				filename=filename[:-1]
			gmxdir=filename
			gmxdirname=os.path.split(gmxdir)[1]
			gmxdirnamesp=os.path.splitext(gmxdirname)[0]
			gmxfile=gmxdirnamesp+".project.gmx"
		else:
			gmxdir,gmxfile=os.path.split(filename)
		return gmxdir,gmxfile

	def ReadGmx(self, filename):
		gmxdir,gmxfile=self.GmxSplitPath(filename)
		self.resourceTree = GameTree(self)
		self.resourceTree.AddGroupName("Sprites")
		self.resourceTree.AddGroupName("Sounds")
		self.resourceTree.AddGroupName("Backgrounds")
		self.resourceTree.AddGroupName("Paths")
		self.resourceTree.AddGroupName("Scripts")
		self.resourceTree.AddGroupName("Fonts")
		self.resourceTree.AddGroupName("Timelines")
		self.resourceTree.AddGroupName("Objects")
		self.resourceTree.AddGroupName("Rooms")
		self.resourceTree.AddGroupName("Game Information")
		self.resourceTree.AddGroupName("Global Game Settings")
		self.resourceTree.AddGroupName("Extensions")
		gmxPath=os.path.join(gmxdir,gmxfile)
		tree=xml.etree.ElementTree.parse(gmxPath)
		root=tree.getroot()
		self.gmxRoot=root
		if root.tag!="assets":
			print_error("tag isn't assets "+root.tag)
		seen={}
		self.egmNameId={}
		self.egmNameId["<undefined>"] = -1
		for child in root:
			if seen.get(child.tag,0)>0:
				print_error("duplicated tag "+child.tag)
			seen[child.tag]=seen.get(child.tag,0)+1
			if child.tag=="Configs":
				pass
			elif child.tag=="datafiles":
				pass
			elif child.tag=="options":
				pass
			elif child.tag=="help":
				pass
			elif child.tag=="NewExtensions":
				pass
			elif child.tag=="sounds":
				self.ReadGmxResourceNames("sounds","sound",child,child.attrib["name"],self.egmNameId)
			elif child.tag=="sprites":
				self.ReadGmxResourceNames("sprites","sprite",child,child.attrib["name"],self.egmNameId)
			elif child.tag=="backgrounds":
				self.ReadGmxResourceNames("backgrounds","background",child,child.attrib["name"],self.egmNameId)
			elif child.tag=="paths":
				self.ReadGmxResourceNames("paths","path",child,child.attrib["name"],self.egmNameId)
			elif child.tag=="scripts":
				self.ReadGmxResourceNames("scripts","script",child,child.attrib["name"],self.egmNameId)
			elif child.tag=="fonts":
				self.ReadGmxResourceNames("fonts","font",child,child.attrib["name"],self.egmNameId)
			elif child.tag=="objects":
				self.ReadGmxResourceNames("objects","object",child,child.attrib["name"],self.egmNameId)
			elif child.tag=="timelines":
				self.ReadGmxResourceNames("timelines","timeline",child,child.attrib["name"],self.egmNameId)
			elif child.tag=="rooms":
				self.ReadGmxResourceNames("rooms","room",child,child.attrib["name"],self.egmNameId)
			elif child.tag=="help":
				pass
			elif child.tag=="TutorialState":
				pass
			elif child.tag=="constants":
				pass
			else:
				print_error("unsupported tag "+child.tag)
		for child in root:
			if child.tag=="Configs":#<Configs name="configs"><Config>Configs\Default</Config></Configs>
				if len(child)>1:
					print_error("more than 1 Config")
				for chil in child:
					if chil.tag=="Config":
						filep=chil.text.replace("\\","/")
						p,name=os.path.split(filep)
						p=os.path.join(gmxdir,p)
						self.ReadGmxConfig(self,p,name)
					else:
						print_error("tag isn't Config "+chil.tag)
			elif child.tag=="datafiles":
				pass
			elif child.tag=="options":#Config
				self.settings = GameSettings(self)
				self.gameInformation = GameInformation(self)
				self.settings.ReadGmx(child)
			elif child.tag=="help":#Game Information
				pass
			elif child.tag=="NewExtensions":#<NewExtensions><extension index="0">extensions\Extension1</extension></NewExtensions>
				pass
			elif child.tag=="sounds":#<sounds name="sound"><sound>sound\sound0</sound></sounds>
				self.ReadGmxResources("sounds","sound",child,child.attrib["name"],gmxdir)
			elif child.tag=="sprites":#<sprites name="sprites"><sprite>sprites\sprite0</sprite></sprites>
				self.ReadGmxResources("sprites","sprite",child,child.attrib["name"],gmxdir)
			elif child.tag=="backgrounds":#<backgrounds name="background"><background>background\background0</background></backgrounds>
				self.ReadGmxResources("backgrounds","background",child,child.attrib["name"],gmxdir)
			elif child.tag=="paths":#<paths name="paths"><path>paths\path0</path></paths>
				self.ReadGmxResources("paths","path",child,child.attrib["name"],gmxdir)
			elif child.tag=="scripts":#<scripts name="scripts"><script>scripts\script0.gml</script></scripts>
				self.ReadGmxResources("scripts","script",child,child.attrib["name"],gmxdir)
			elif child.tag=="fonts":#<fonts name="fonts"><font>fonts\font0</font></fonts>
				self.ReadGmxResources("fonts","font",child,child.attrib["name"],gmxdir)
			elif child.tag=="objects":#<objects name="objects"><object>objects\object0</object></objects>
				self.ReadGmxResources("objects","object",child,child.attrib["name"],gmxdir)
			elif child.tag=="timelines":#<timelines name="timelines"><timeline>timelines\timeline0</timeline></timelines>
				self.ReadGmxResources("timelines","timeline",child,child.attrib["name"],gmxdir)
			elif child.tag=="rooms":#<rooms name="rooms"><room>rooms\room0</room></rooms>
				self.ReadGmxResources("rooms","room",child,child.attrib["name"],gmxdir)
			elif child.tag=="help":#<help><rtf>help.rtf</rtf></help>
				pass
			elif child.tag=="TutorialState":#<TutorialState><IsTutorial>0</IsTutorial><TutorialName></TutorialName><TutorialPage>0</TutorialPage></TutorialState>
				pass
			elif child.tag=="constants":#<constants number="23"><constant name="VersionMajor">1</constant>
				pass
			else:
				print_error("unsupported tag "+child.tag)
		self.Finalize()

	def ReadGmk(self, stream):
		# Read header
		if stream.ReadDword() != self.GMK_MAGIC:
			print_error("Invalid magic")
		self.version=stream.ReadDword()
		#if self.version==530:
		#elif self.version==600:
		#elif self.version==701:
		if self.version not in [800,810]:
			print_error("Unknown or unsupported version "+str(self.version))
		# Read header
		self.gameId = stream.ReadDword()
		self.guid=[]
		for i in xrange(self.GMK_GUID_LENGTH):
			self.guid.append(stream.readUChar())
		# Load settings
		gmVersionGameSettings=stream.ReadDword()
		if gmVersionGameSettings not in [800,820]:print_error("unsupported gmk version "+str(gmVersionGameSettings))
		self.settings = GameSettings(self)
		self.settings.ReadGmk(stream)
		# Load triggers
		gmVersionTriggers=stream.ReadDword()
		if gmVersionTriggers != 800:print_error("unsupported gmk version "+str(gmVersionTriggers))
		count = stream.ReadDword()
		for c in xrange(count):
			trigger = GmkTrigger(self,c)
			trigger.ReadGmk(stream)
			self.triggers.append(trigger)
		#Last time Triggers were changed'
		stream.ReadTimestamp()
		# Load constants
		#GM version needed for Resource
		stream.ReadDword()
		count = stream.ReadDword()
		for c in xrange(count):
			name = stream.ReadString()
			value = stream.ReadString()
			self.constants.append((name, value))
		#Last time Constants were changed
		stream.ReadTimestamp()
		# Load sounds
		#GM version needed for Resource
		stream.ReadDword()
		count = stream.ReadDword()
		for c in xrange(count):
			sound = GameSound(self,c)
			sound.ReadGmk(stream)
			if sound.exists:
				self.sounds.append(sound)
		# Load sprites
		#GM version needed for Resource
		stream.ReadDword()
		count = stream.ReadDword()
		for c in xrange(count):
			sprite = GameSprite(self,c)
			sprite.ReadGmk(stream)
			if sprite.exists:
				self.sprites.append(sprite)
		# Load backgrounds
		#GM version needed for Resource
		stream.ReadDword()
		count = stream.ReadDword()
		for c in xrange(count):
			background = GameBackground(self,c)
			background.ReadGmk(stream)
			if background.exists:
				self.backgrounds.append(background)
		# Load paths
		#GM version needed for Resource
		stream.ReadDword()
		count = stream.ReadDword()
		for c in xrange(count):
			path = GamePath(self,c)
			path.ReadGmk(stream)
			self.paths.append(path)
		# Load scripts
		#GM version needed for Resource
		stream.ReadDword()
		count = stream.ReadDword()
		for c in xrange(count):
			script = GameScript(self,c)
			script.ReadGmk(stream)
			self.scripts.append(script)
		# Load fonts
		#GM version needed for Resource
		stream.ReadDword()
		count = stream.ReadDword()
		for c in xrange(count):
			font = GameFont(self,c)
			font.ReadGmk(stream)
			self.fonts.append(font)
		# Load timelines
		#GM version needed for Resource
		stream.ReadDword()
		count = stream.ReadDword()
		for c in xrange(count):
			timeline = GameTimeline(self,c)
			timeline.ReadGmk(stream)
			if timeline.exists:
				print_error("timeline unsupported")
				self.timelines.append(timeline)
		# Load objects
		#GM version needed for Resource
		stream.ReadDword()
		count = stream.ReadDword()
		for c in xrange(count):
			gmObject = GameObject(self,c)
			gmObject.ReadGmk(stream)
			if gmObject.exists:
				self.objects.append(gmObject)
		# Load rooms
		#GM version needed for Resource
		stream.ReadDword()
		count = stream.ReadDword()
		for c in xrange(count):
			room = GameRoom(self,c)
			room.ReadGmk(stream)
			if room.exists:
				self.rooms.append(room)
		# Load last ids
		self.lastInstancePlacedId = stream.ReadDword()
		self.lastTilePlacedId = stream.ReadDword()
		# Load include files
		#GM version needed for Resource
		stream.ReadDword()
		count = stream.ReadDword()
		for c in xrange(count):
			includeFile = GameIncludeFile(self,c)
			includeFile.ReadGmk(stream)
			self.includeFiles.append(includeFile)
		# Load packages
		#GM version needed for Resource
		stream.ReadDword()
		count = stream.ReadDword()
		for c in xrange(count):
			self.packages.append(stream.ReadString())
		# Read game information
		#GM version needed for Resource
		stream.ReadDword()
		self.gameInformation = GameInformation(self)
		self.gameInformation.ReadGmk(stream)
		# Read library creation code -- we should be able to safely ignore this
		#GM version needed for Resource
		stream.ReadDword()
		count = stream.ReadDword()
		for c in xrange(count):
			print_warning("library creation code "+stream.ReadString())
		# Read room execution order -- this too
		#GM version needed for Resource
		stream.ReadDword()
		count = stream.ReadDword()
		for c in xrange(count):
			print_warning("room execution order "+str(stream.ReadDword()))
		# Read resource tree
		self.resourceTree = GameTree(self)
		self.resourceTree.ReadGmk(stream)
		self.Finalize()

	def Read(self, filename):
		self.readingFile=True
		self.readPath=filename
		ext=os.path.splitext(filename)[1]
		if ext in [".gmk",".gm81",".gm6"]:
			data = open(filename, "rb")
			stream = BinaryStream(data)
			self.ReadGmk(stream)
		elif ext==".egm":
			self.ReadEgm(filename)
		elif ext==".gmx":
			self.ReadGmx(filename)
		elif ext==".gmz":
			self.ReadGmz(filename)
		else:
			print_error("unsupported load format")
		self.readingFile=False

	def SaveGmx(self, filename):
		if filename==self.readPath:
			print_error("unsupported update gmx")
		if not os.path.exists(filename):
			if filename.endswith(".project.gmx"):
				print_error("unsupported save to .project.gmx file")
			else:
				os.mkdir(filename)
		gmxdir,gmxfile=self.GmxSplitPath(filename)
		gmxPath=os.path.join(gmxdir,gmxfile)
		if os.path.exists(gmxPath):
			print_error("gmx already exists "+gmxPath)
			return
		writeFile=open(gmxPath,"w")
		writeFile.write("<!--This Document is generated by GameMaker, if you edit it by hand then you do so at your own risk!-->\n")
		writeFile.write(xml.etree.ElementTree.tostring(self.gmxRoot))
		writeFile.close()

	def SaveGmk(self, stream):
		stream = BinaryStream(stream)
		# Write header
		stream.WriteDword(GameFile.GMK_MAGIC)
		stream.WriteDword(810)
		# Write header
		stream.WriteDword(self.gameId)
		for i in xrange(self.GMK_GUID_LENGTH):
			guidByte = self.gameId >> i / 4
			guidByte %= ((i >> 6) + guidByte & 0x7F) + 0xFF
			guidByte ^= (i * guidByte >> 3) & 0xAB
			if guidByte>256:#clifix
				guidByte=0
			stream.WriteByte(chr(guidByte))
		# Write settings
		stream.WriteDword(800)
		if self.settings == None:
			raise "Settings are not declared"
		self.settings.WriteGmk(stream)
		# Write triggers
		stream.WriteDword(800)
		stream.WriteDword(len(self.triggers))
		for i in xrange(len(self.triggers)):
			self.triggers[i].WriteGmk(stream)
		stream.WriteTimestamp()
		# Write constants
		stream.WriteDword(800)
		stream.WriteDword(len(self.constants))
		for i in xrange(len(self.constants)):
			stream.WriteString(self.constants[i][0])
			stream.WriteString(self.constants[i][1])
		stream.WriteTimestamp()
		# Write sounds
		stream.WriteDword(800)
		stream.WriteDword(len(self.sounds))
		for i in xrange(len(self.sounds)):
			self.sounds[i].WriteGmk(stream)
		# Write sprites
		stream.WriteDword(800)
		stream.WriteDword(len(self.sprites))
		for i in xrange(len(self.sprites)):
			self.sprites[i].WriteGmk(stream)
		# Write backgrounds
		stream.WriteDword(800)
		stream.WriteDword(len(self.backgrounds))
		for i in xrange(len(self.backgrounds)):
			self.backgrounds[i].WriteGmk(stream)
		# Write paths
		stream.WriteDword(800)
		stream.WriteDword(len(self.paths))
		for i in xrange(len(self.paths)):
			self.paths[i].WriteGmk(stream)
		# Write scripts
		stream.WriteDword(800)
		stream.WriteDword(len(self.scripts))
		for i in xrange(len(self.scripts)):
			self.scripts[i].WriteGmk(stream)
		# Write fonts
		stream.WriteDword(800)
		stream.WriteDword(len(self.fonts))
		for i in xrange(len(self.fonts)):
			self.fonts[i].WriteGmk(stream)
		# Write timelines
		stream.WriteDword(800)
		stream.WriteDword(len(self.timelines))
		for i in xrange(len(self.timelines)):
			self.timelines[i].WriteGmk(stream)
		# Write objects
		stream.WriteDword(800)
		stream.WriteDword(len(self.objects))
		for i in xrange(len(self.objects)):
			self.objects[i].WriteGmk(stream)
		# Write rooms
		stream.WriteDword(800)
		stream.WriteDword(len(self.rooms))
		for i in xrange(len(self.rooms)):
			self.rooms[i].WriteGmk(stream)
		# Write last ids
		stream.WriteDword(self.lastInstancePlacedId)
		stream.WriteDword(self.lastTilePlacedId)
		# Write include files
		stream.WriteDword(800)
		stream.WriteDword(len(self.includeFiles))
		for i in xrange(len(self.includeFiles)):
			self.includeFiles[i].WriteGmk(stream)
		# Write packages
		stream.WriteDword(700)
		stream.WriteDword(len(self.packages))
		for i in xrange(len(self.packages)):
			stream.WriteString(self.packages[i])
		# Write game information
		stream.WriteDword(800)
		self.gameInformation.WriteGmk(stream)
		# Ignore library creation code (safe)
		stream.WriteDword(500)
		stream.WriteDword(0)
		# Ignore room execution order (safe)
		stream.WriteDword(700)
		stream.WriteDword(0)
		# Write resource tree
		self.resourceTree.WriteGmk(stream)

	def Save(self, ext, filename, wfile=None):
		if ext in [".gmk",".gm81"]:
			stream=open(filename,"wb")
			self.SaveGmk(stream)
		elif ext == ".egm":
			stream=open(filename,"wb")
			self.SaveEgm(stream)
		elif ext == ".gmx":
			self.SaveGmx(filename)
		elif ext == ".gmz":
			self.SaveGmz(stream)
		elif ext == ".ggg":
			ggg=self.WriteGGG()
			if not wfile:
				wfile=open(filename,"wb")
			wfile.write(ggg)
		else:
			print_error("unsupported save format")

	def Finalize(self):
		# Finalize paths
		for i in xrange(len(self.paths)):
			self.paths[i].Finalize()
		# Finalize timelines
		for i in xrange(len(self.timelines)):
			self.timelines[i].Finalize()
		# Finalize objects
		for i in xrange(len(self.objects)):
			self.objects[i].Finalize()
		# Finalize rooms
		for i in xrange(len(self.rooms)):
			self.rooms[i].Finalize()
		# Finalize resource tree
		if self.resourceTree:
			self.resourceTree.Finalize()

	def GetResourceHighestId(self, type):
		highest=-1
		if type==GameFile.RtSprite:
			for s in self.sprites:
				id = s.getMember("id")
				if id>highest:
					highest=id
		elif type==GameFile.RtSound:
			for s in self.sounds:
				id = s.getMember("id")
				if id>highest:
					highest=id
		elif type==GameFile.RtBackground:
			for s in self.backgrounds:
				id = s.getMember("id")
				if id>highest:
					highest=id
		elif type==GameFile.RtPath:
			for s in self.paths:
				id = s.getMember("id")
				if id>highest:
					highest=id
		elif type==GameFile.RtScript:
			for s in self.scripts:
				id = s.getMember("id")
				if id>highest:
					highest=id
		elif type==GameFile.RtFont:
			for s in self.fonts:
				id = s.getMember("id")
				if id>highest:
					highest=id
		elif type==GameFile.RtTimeline:
			for s in self.timelines:
				id = s.getMember("id")
				if id>highest:
					highest=id
		elif type==GameFile.RtObject:
			for s in self.objects:
				id = s.getMember("id")
				if id>highest:
					highest=id
		elif type==GameFile.RtRoom:
			for s in self.rooms:
				id = s.getMember("id")
				if id>highest:
					highest=id
		return highest

	def GetResource(self, type, index):
		if type==GameFile.RtSprite:
			for s in self.sprites:
				if s.getMember("id")==index:
					return s
		elif type==GameFile.RtSound:
			for s in self.sounds:
				if s.getMember("id")==index: return s
		elif type==GameFile.RtBackground:
			for s in self.backgrounds:
				if s.getMember("id")==index: return s
		elif type==GameFile.RtPath:
			for s in self.paths:
				if s.getMember("id")==index: return s
		elif type==GameFile.RtScript:
			for s in self.scripts:
				if s.getMember("id")==index: return s
		elif type==GameFile.RtFont:
			for s in self.fonts:
				if s.getMember("id")==index: return s
		elif type==GameFile.RtTimeline:
			for s in self.timelines:
				if s.getMember("id")==index: return s
		elif type==GameFile.RtObject:
			for s in self.objects:
				if s.getMember("id")==index: return s
		elif type==GameFile.RtRoom:
			for s in self.rooms:
				if s.getMember("id")==index: return s
		return None

	def GetResourceName(self, type, name):
		if type==GameFile.RtSprite:
			for s in self.sprites:
				if s.getMember("name")==name:
					return s
		elif type==GameFile.RtSound:
			for s in self.sounds:
				if s.getMember("name")==name: return s
		elif type==GameFile.RtBackground:
			for s in self.backgrounds:
				if s.getMember("name")==name: return s
		elif type==GameFile.RtPath:
			for s in self.paths:
				if s.getMember("name")==name: return s
		elif type==GameFile.RtScript:
			for s in self.scripts:
				if s.getMember("name")==name: return s
		elif type==GameFile.RtShader:
			for s in self.shaders:
				if s.getMember("name")==name: return s
		elif type==GameFile.RtFont:
			for s in self.fonts:
				if s.getMember("name")==name: return s
		elif type==GameFile.RtTimeline:
			for s in self.timelines:
				if s.getMember("name")==name: return s
		elif type==GameFile.RtObject:
			for s in self.objects:
				if s.getMember("name")==name: return s
		elif type==GameFile.RtRoom:
			for s in self.rooms:
				if s.getMember("name")==name: return s
		return None

	def DeleteResource(self, res):
		if type(res)==GameSprite:
			self.sprites.remove(res)
		elif type(res)==GameSound:
			self.sounds.remove(res)
		elif type(res)==GameBackground:
			self.backgrounds.remove(res)
		elif type(res)==GamePath:
			self.paths.remove(res)
		elif type(res)==GameScript:
			self.scripts.remove(res)
		elif type(res)==GameShader:
			self.shaders.remove(res)
		elif type(res)==GameFont:
			self.fonts.remove(res)
		elif type(res)==GameTimeline:
			self.timelines.remove(res)
		elif type(res)==GameObject:
			self.objects.remove(res)
		elif type(res)==GameRoom:
			self.rooms.remove(res)
		for callBack in self.listeners:
			callBack("delete")

	def WriteGGG(self):
		stri=""
		stri+="lastInstancePlacedId="+str(self.lastInstancePlacedId)+"\n"
		stri+="lastTilePlacedId="+str(self.lastTilePlacedId)+"\n"
		stri+=self.settings.WriteGGG()
		stri+=self.gameInformation.WriteGGG()
		#stri+=self.resourceTree.WriteGGG()
		for o in self.triggers:			stri+=o.WriteGGG()
		for o in self.constants:			stri+=o.WriteGGG()
		for o in self.sounds:			stri+=o.WriteGGG()
		for o in self.sprites:			stri+=o.WriteGGG()
		for o in self.backgrounds:			stri+=o.WriteGGG()
		for o in self.paths:			stri+=o.WriteGGG()
		for o in self.scripts:			stri+=o.WriteGGG()
		for o in self.fonts:			stri+=o.WriteGGG()
		for o in self.timelines:			stri+=o.WriteGGG()
		for o in self.objects:			stri+=o.WriteGGG()
		for o in self.rooms:			stri+=o.WriteGGG()
		for o in self.includeFiles:			stri+=o.WriteGGG()
		return stri

	def WriteES(self):
		self.es=EnigmaStruct()
		self.es.fileVersion = -1#i.format.getVersion();
		self.es.filename = None#i.uri
		self.populateSettings()
		print_notice("writing Sprites")
		self.populateSprites()
		self.populateSounds()
		print_notice("writing Backgrounds")
		self.populateBackgrounds()
		self.populatePaths()
		self.populateScripts()
		self.populateShaders()
		print_notice("writing Fonts")
		self.populateFonts()
		print_notice("writing Timelines")
		self.populateTimelines()
		self.populateObjects()
		self.populateRooms()
		self.es.triggerCount = 0;
		self.es.constantCount = 0#i.constants.size();
		#if (o.constantCount != 0)
		#	{
		#	o.constants = new Constant.ByReference();
		#	Constant[] ocl = (Constant[]) o.constants.toArray(o.constantCount);
		#	for (int c = 0; c < o.constantCount; c++)
		#		{
		#		ocl[c].name = i.constants.get(c).name;
		#		ocl[c].value = i.constants.get(c).value;
		#		}
		#	}
		self.es.includeCount = 0#i.includes.size();
		#if (o.includeCount != 0)
		#	{
		#	o.includes = new Include.ByReference();
		#	Include[] oil = (Include[]) o.includes.toArray(o.includeCount);
		#	for (int inc = 0; inc < o.includeCount; inc++)
		#		{
		#		oil[inc].filepath = i.includes.get(inc).filepath;
		#		}
		#	}
		self.es.packageCount = 0
		# o.packageCount = packages.length;
		# o.packages = new StringArray(packages);
		self.es.extensionCount = 0
		self.es.lastInstanceId = self.lastInstancePlacedId
		self.es.lastTileId = self.lastTilePlacedId
		return self.es

	def populateSettings(self):
		if not self.settings:
			print_error("no settings")
		self.settings.WriteESGameSettings(self.es)
		self.es.gameSettings.gameId = self.gameId

	def populateSprites(self):
		self.es.spriteCount=len(self.sprites)
		if self.es.spriteCount>0:
			ot=(ESSprite*self.es.spriteCount)()
			for count in xrange(self.es.spriteCount):
				tobj=self.sprites[count]
				eobj=tobj.WriteESSprite()
				ot[count]=eobj
			self.es.sprites=cast(ot,POINTER(ESSprite))

	def populateSounds(self):
		self.es.soundCount=len(self.sounds)
		if self.es.spriteCount>0:
			ot=(ESSound*self.es.soundCount)()
			for count in xrange(self.es.soundCount):
				tobj=self.sounds[count]
				eobj=tobj.WriteESSound()
				ot[count]=eobj
			self.es.sounds=cast(ot,POINTER(ESSound))

	def populateBackgrounds(self):
		self.es.backgroundCount=len(self.backgrounds)
		if self.es.backgroundCount>0:
			ot=(ESBackground*self.es.backgroundCount)()
			for count in xrange(self.es.backgroundCount):
				tobj=self.backgrounds[count]
				eobj=tobj.WriteESBackground()
				ot[count]=eobj
			self.es.backgrounds=cast(ot,POINTER(ESBackground))

	def populatePaths(self):
		self.es.pathCount=len(self.paths)
		if self.es.pathCount>0:
			ot=(ESPath*self.es.pathCount)()
			for count in xrange(self.es.pathCount):
				tobj=self.paths[count]
				eobj=tobj.WriteESPath()
				ot[count]=eobj
			self.es.paths=cast(ot,POINTER(ESPath))

	def populateScripts(self):
		self.es.scriptCount=len(self.scripts)
		if self.es.scriptCount>0:
			ot=(ESScript*self.es.scriptCount)()
			for count in xrange(self.es.scriptCount):
				tobj=self.scripts[count]
				eobj=tobj.WriteESScript()
				ot[count]=eobj
			self.es.scripts=cast(ot,POINTER(ESScript))

	def populateShaders(self):
		self.es.shaderCount=len(self.shaders)
		if self.es.shaderCount>0:
			ot=(ESShader*self.es.shaderCount)()
			for count in xrange(self.es.shaderCount):
				tobj=self.shaders[count]
				eobj=tobj.WriteESShader()
				ot[count]=eobj
			self.es.shaders=cast(ot,POINTER(ESShader))

	def populateFonts(self):
		if not self.app:
			print_error("initialize Qt")
		oF = ESFont()
		oF.name = "EnigmaDefault"
		oF.id = -1
		oF.fontName = "Arial"
		oF.size = 12
		oF.bold = False
		oF.italic = False
		oF.rangeMin = 32
		oF.rangeMax = 127
		og = self.populateGlyphs(oF,oF.rangeMin,oF.rangeMax,0);
		oF.glyphs = cast(og,POINTER(ESGlyph))
		self.es.fontCount=len(self.fonts)+1
		ot=(ESFont*self.es.fontCount)()
		ot[0]=oF
		if self.es.fontCount>1:
			for count in xrange(1,self.es.fontCount):
				ifont=self.fonts[count-1]
				oF = ESFont()
				oF.name = ifont.getMember("name")
				oF.id = ifont.getMember("id")
				oF.fontName = ifont.getMember("fontName")
				oF.size = ifont.getMember("size")
				oF.bold = ifont.getMember("bold")
				oF.italic = ifont.getMember("italic")
				oF.rangeMin = ifont.getMember("characterRangeBegin")
				oF.rangeMax = ifont.getMember("characterRangeEnd")
				og = self.populateGlyphs(oF,oF.rangeMin,oF.rangeMax,0);
				oF.glyphs = cast(og,POINTER(ESGlyph))
				ot[count]=oF
		self.es.fonts=cast(ot,POINTER(ESFont))

	def populateGlyphs(self, fnt, rangeMin, rangeMax, aa):
		glyphs = (ESGlyph*(rangeMax - rangeMin + 1))()
		for c in xrange(rangeMin,rangeMax):
			self.populateGlyph(glyphs[c - rangeMin],fnt,chr(c),aa)
		return glyphs

	def populateGlyph(self, og, fnt, c, aa):
		font = QtGui.QFont(fnt.fontName,fnt.size)
		metrics = QtGui.QFontMetrics(font)
		r=metrics.boundingRect(c)
		if r.width()==0:
			r.setWidth(metrics.width(c))
		r.setWidth(metrics.width(c))#clifix
		# Generate a raster of the glyph vector
		i=QtGui.QImage(r.width(),r.height(),QtGui.QImage.Format_ARGB32)
		g=QtGui.QPainter(i)
		g.setFont(font)
		g.setPen(QtGui.QColor(255,255,255))
		g.fillRect(0,0,r.width(),r.height(),QtGui.QColor(0,0,0))
		g.drawText(0,abs(r.y()),c)
		g.end()
		# Produce the relevant stats
		og.origin = r.x() # bump image right X pixels
		og.baseline = r.y() # bump image down X pixels (usually negative, since baseline is at bottom)
		og.advance = r.width() # advance X pixels from origin
		# Copy over the raster
		raster = ""
		for y in xrange(r.height()):
			for x in xrange(r.width()):
				raster+=chr(i.pixel(x,y)&0xff)
		og.width = r.width()
		og.height = r.height()
		og.data = raster

	def populateTimelines(self):
		self.es.timelineCount=len(self.timelines)
		if self.es.scriptCount>0:
			ot=(ESTimeline*self.es.timelineCount)()
			for count in xrange(self.es.timelineCount):
				tobj=self.timelines[count]
				eobj=tobj.WriteESTimeline()
				ot[count]=eobj
			self.es.timelines=cast(ot,POINTER(ESTimeline))

	def populateObjects(self):
		self.es.gmObjectCount=len(self.objects)
		if self.es.gmObjectCount>0:
			ot=(ESObject*self.es.gmObjectCount)()
			for count in xrange(self.es.gmObjectCount):
				tobj=self.objects[count]
				eobj=tobj.WriteESObject()
				ot[count]=eobj
			self.es.gmObjects=cast(ot,POINTER(ESObject))

	def populateRooms(self):
		self.es.roomCount=len(self.rooms)
		if self.es.roomCount>0:
			ot=(ESRoom*self.es.roomCount)()
			for count in xrange(self.es.roomCount):
				tobj=self.rooms[count]
				eobj=tobj.WriteESRoom()
				ot[count]=eobj
			self.es.rooms=cast(ot,POINTER(ESRoom))

def LoadPluginLib():
	egmf=cdll.LoadLibrary("./libcompileEGMf.so")
	global ecb,compileEGMf,next_available_resource,first_available_resource,resource_isFunction,resource_argCountMin,resource_argCountMax,resource_overloadCount,resource_parameters,resource_isTypeName,resource_isGlobal,resources_atEnd,libInit,libFree,definitionsModified,syntaxCheck
	#extern int (*compileEGMf)(EnigmaStruct *es, const char* exe_filename, int mode);
	compileEGMf=egmf.compileEGMf
	compileEGMf.restype = c_int
	compileEGMf.argtypes = [POINTER(EnigmaStruct), c_char_p, c_int]
	#extern const char* (*next_available_resource)();
	next_available_resource=egmf.next_available_resource
	next_available_resource.restype = c_char_p
	next_available_resource.argtypes = []
	#extern const char* (*first_available_resource)();
	first_available_resource=egmf.first_available_resource
	first_available_resource.restype = c_char_p
	first_available_resource.argtypes = []
	#extern bool (*resource_isFunction)();
	resource_isFunction=egmf.resource_isFunction
	resource_isFunction.restype = c_intbool
	resource_isFunction.argtypes = []
	#extern int (*resource_argCountMin)();
	resource_argCountMin=egmf.resource_argCountMin
	resource_argCountMin.restype = c_int
	resource_argCountMin.argtypes = []
	#extern int (*resource_argCountMax)(); //Returns the maximum number of arguments to the function
	resource_argCountMax=egmf.resource_argCountMax
	resource_argCountMax.restype = c_int
	resource_argCountMax.argtypes = []
	#extern int (*resource_overloadCount)(); //Returns the number of times the function was declared in the parsed sources
	resource_overloadCount=egmf.resource_overloadCount
	resource_overloadCount.restype = c_int
	resource_overloadCount.argtypes = []
	#extern const char* (*resource_parameters)(int i); //Returns a simple string of parameters and defaults that would serve as the prototype of this function
	resource_parameters=egmf.resource_parameters
	resource_parameters.restype = c_char_p
	resource_parameters.argtypes = [c_int]
	#extern int (*resource_isTypeName)(); //Returns whether the resource can be used as a typename.
	resource_isTypeName=egmf.resource_isTypeName
	resource_isTypeName.restype = c_int
	resource_isTypeName.argtypes = []
	#extern int (*resource_isGlobal)(); //Returns whether the resource is nothing but a global variable.
	resource_isGlobal=egmf.resource_isGlobal
	resource_isGlobal.restype = c_int
	resource_isGlobal.argtypes = []
	#extern bool (*resources_atEnd)(); //Returns whether we're really done iterating the list
	resources_atEnd=egmf.resources_atEnd
	resources_atEnd.restype = c_intbool
	resources_atEnd.argtypes = []
	#extern const char* (*libInit)(EnigmaCallbacks* ecs);
	libInit=egmf.libInit
	libInit.restype = c_char_p
	libInit.argtypes = [POINTER(EnigmaCallbacks)]
	#extern void (*libFree)();
	libFree=egmf.libFree
	libFree.restype = c_voidp
	libFree.argtypes = []
	#extern syntax_error* (*definitionsModified)(const char* wscode, const char* targetYaml);
	definitionsModified=egmf.definitionsModified
	definitionsModified.restype = POINTER(syntax_error)
	definitionsModified.argtypes = [c_char_p, c_char_p]
	#extern syntax_error* (*syntaxCheck)(int script_count, const char* *script_names, const char* code);
	syntaxCheck=egmf.syntaxCheck
	syntaxCheck.restype = POINTER(syntax_error)
	syntaxCheck.argtypes = [c_int, c_char_p, c_char_p]#array
	ecb=EnigmaCallbacks()
	ecb.dia_open = CFUNCTYPE(c_voidp)(ede_dia_open)
	ecb.dia_add = CFUNCTYPE(c_voidp, c_char_p)(ede_dia_add)
	ecb.dia_clear = CFUNCTYPE(c_voidp)(ede_dia_clear)
	ecb.dia_progress = CFUNCTYPE(c_voidp, c_int)(ede_dia_progress)
	ecb.dia_progress_text = CFUNCTYPE(c_voidp, c_char_p)(ede_dia_progress_text)
	ecb.output_redirect_file = CFUNCTYPE(c_voidp, c_char_p)(ede_output_redirect_file)
	ecb.output_redirect_reset = CFUNCTYPE(c_voidp)(ede_output_redirect_reset)
	libInit(ecb)



