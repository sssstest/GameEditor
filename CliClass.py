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
import tempfile#gmz
import shutil#gmz
import tempfile
from PyQt4 import QtGui, QtCore#font
from CliApng import *
from CliEefReader import *
from CliPrintColors import *
from CliBinaryStream import *
from CliEnigmaStruct import *
from GameResource import *
from GameSprite import *
from GameSound import *
from GameBackground import *
from GamePath import *
from GameScript import *
from GameShader import *
from GameFont import *
from GameTimeline import *
from GameObject import *
from GameRoom import *
from GameTrigger import *
from GameSettings import *
from GameInformation import *
from GameIncludeFile import *
from GameTree import *

def we_are_frozen():
    return hasattr(sys, "frozen")

def module_path():
	if sys.version_info[0]<3:
		if we_are_frozen():
			return os.path.dirname(unicode(sys.executable, sys.getfilesystemencoding( )))

		return os.path.dirname(unicode(__file__, sys.getfilesystemencoding( )))
	else:
		if we_are_frozen():
			return os.path.dirname(sys.executable)

		return os.path.dirname(__file__)

cliDir = module_path()+"/"
tmpDir=tempfile.gettempdir()+"/"

def redirectStdout():
	global realStdout,realStderr
	realStdout = open(tmpDir+"enigmastdout2.txt","w")
	os.dup2(sys.stdout.fileno(), realStdout.fileno())
	realStderr = open(tmpDir+"enigmacrap2.txt","w")
	os.dup2(sys.stderr.fileno(), realStderr.fileno())
	oldf = open(tmpDir+"enigmastdout.txt","w")
	os.dup2(oldf.fileno(), sys.stdout.fileno())
	oldf2 = open(tmpDir+"enigmacrap.txt","w")
	os.dup2(oldf2.fileno(), sys.stderr.fileno())

def restoreStdout():
	global realStdout,realStderr
	os.dup2(realStdout.fileno(), sys.stdout.fileno())
	os.dup2(realStderr.fileno(), sys.stderr.fileno())

realStdout=sys.stdout
realStderr=sys.stderr
setRealStdout(realStdout)

def ede_dia_open():
	pass

def ede_dia_add(text):
	pass
	#print_notice("ede_dia_add "+text)

def ede_dia_clear():
	pass

def ede_dia_progress(progress):
	print_notice(str(progress)+"%")

def ede_dia_progress_text(caption):
	print_notice("ENIGMA "+str(caption))

def ede_output_redirect_file(filepath):
	print_notice("ede_output_redirect_file "+str(filepath))

def ede_output_redirect_reset():
	print_notice("ede_output_redirect_reset")

def ede_ide_execute(command,a,b):
	print_error("ide_execute")
	return 0
	
def ede_ide_compress_data(d,i):
	print_error("ide_compress_data")
	return 0

def ifCleanArgumentValue(chil):
	for child in "(),\n":
		if child in chil:
			return False
	return True

class GameFile(GameResource):
	defaults={}

	if Class:
		GMK_MAGIC					= 1234321
		GMK_GUID_LENGTH			= 16
		GMK_MAX_ID				= 100000000
		GMK_MIN_INSTANCE_LAST_ID	= 100000
		GMK_MIN_TILE_LAST_ID		= 1000000

	def __init__(self):
		GameResource.__init__(self, self, -1)
		self.configs=[]
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
		self.includeFiles=[]
		self.packages=[]
		self.lastInstancePlacedId=self.GMK_MIN_INSTANCE_LAST_ID
		self.lastTilePlacedId=self.GMK_MIN_TILE_LAST_ID
		self.gameInformation=None
		self.resourceTree=None
		self.gameId = random.randint(0,2147483647) % self.GMK_MAX_ID;
		self.ifReadingFile=False
		self.gmxRoot=None
		self.EnigmaSettingsEef=None
		self.EnigmaSettingsEefData=None
		if os.name=="nt":
			self.EnigmaTargetAudio="OpenAL"
			self.EnigmaTargetWindowing="Win32"
			self.EnigmaTargetCompiler="gcc"
			self.EnigmaTargetGraphics="OpenGL3"
			self.EnigmaTargetWidget="Win32"
			self.EnigmaTargetCollision="Precise"
		else:
			self.EnigmaTargetAudio="OpenAL"
			self.EnigmaTargetWindowing="xlib"
			self.EnigmaTargetCompiler="gcc"
			self.EnigmaTargetGraphics="OpenGL3"
			self.EnigmaTargetWidget="None"
			self.EnigmaTargetCollision="BBox"
		self.EnigmaTargetNetworking="None"

	def Finalize(self):
		# Finalize paths
		for i in range(len(self.paths)):
			self.paths[i].Finalize()
		# Finalize timelines
		for i in range(len(self.timelines)):
			self.timelines[i].Finalize()
		# Finalize objects
		for i in range(len(self.objects)):
			self.objects[i].Finalize()
		# Finalize rooms
		for i in range(len(self.rooms)):
			self.rooms[i].Finalize()
		# Finalize resource tree
		if self.resourceTree:
			self.resourceTree.Finalize()

	def printBasicStats(self):
		numberScripts=len(self.scripts)
		print_notice("number of scripts:\t\t"+str(numberScripts))
		numberScriptLines=0
		for x in self.scripts:
			if x.getMember("value") != "":
				numberScriptLines+=x.getMember("value").count("\n")+1
		print_notice("script lines:\t\t\t"+str(numberScriptLines))
		numberNonCodeActions=0
		numberCodeActions=0
		numberCodeActionLines=0
		for object in self.objects:
			for event in object.events:
				for action in event.actions:
					if action.ifActionCode():
						numberCodeActions+=1
						if action.argumentValue[0]!="":
							numberCodeActionLines+=action.argumentValue[0].count("\n")+1
					else:
						numberNonCodeActions+=1
		print_notice("number of non code actions:\t"+str(numberNonCodeActions))
		print_notice("number of code (603) actions:\t"+str(numberCodeActions))
		print_notice("code action (603) lines:\t"+str(numberCodeActionLines))
		print_notice("script and code action lines:\t"+str(numberScriptLines+numberCodeActionLines))

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
		instance = GameSprite(self, self.GetResourceHighestId(GameSprite)+1)
		self.addSprite(instance)
		return instance

	def newObject(self):
		instance = GameObject(self, self.GetResourceHighestId(GameObject)+1)
		self.addObject(instance)
		return instance

	def newRoom(self):
		instance = GameRoom(self, self.GetResourceHighestId(GameRoom)+1)
		self.addRoom(instance)
		return instance

	def newSettings(self):
		self.configs=[]
		self.configs.append(GameSettings(self))
		return self.configs[0]

	def newGameInformation(self):
		self.gameInformation = GameInformation(self)
		return self.gameInformation

	def AddResourceTree(self):
		self.resourceTree=GameTree(self)
		self.resourceTree.NewTree()

		for s in self.sounds:
			self.resourceTree.AddResourcePath("Sounds/"+s.getMember("name"),s)
		for s in self.sprites:
			self.resourceTree.AddResourcePath("Sprites/"+s.getMember("name"),s)
		for s in self.backgrounds:
			self.resourceTree.AddResourcePath("Backgrounds/"+s.getMember("name"),s)
		for s in self.paths:
			self.resourceTree.AddResourcePath("Paths/"+s.getMember("name"),s)
		for s in self.scripts:
			self.resourceTree.AddResourcePath("Scripts/"+s.getMember("name"),s)
		for s in self.shaders:
			self.resourceTree.AddResourcePath("Shaders/"+s.getMember("name"),s)
		for s in self.fonts:
			self.resourceTree.AddResourcePath("Fonts/"+s.getMember("name"),s)
		for s in self.timelines:
			self.resourceTree.AddResourcePath("Timelines/"+s.getMember("name"),s)
		for s in self.objects:
			self.resourceTree.AddResourcePath("Objects/"+s.getMember("name"),s)
		for s in self.rooms:
			self.resourceTree.AddResourcePath("Rooms/"+s.getMember("name"),s)

	def GetResourceHighestId(self, typec):
		highest=-1
		if type(typec)==str:
			typec=eval(typec)
		if typec==GameSprite:
			for s in self.sprites:
				id = s.getMember("id")
				if id>highest:
					highest=id
		elif typec==GameSound:
			for s in self.sounds:
				id = s.getMember("id")
				if id>highest:
					highest=id
		elif typec==GameBackground:
			for s in self.backgrounds:
				id = s.getMember("id")
				if id>highest:
					highest=id
		elif typec==GamePath:
			for s in self.paths:
				id = s.getMember("id")
				if id>highest:
					highest=id
		elif typec==GameScript:
			for s in self.scripts:
				id = s.getMember("id")
				if id>highest:
					highest=id
		elif typec==GameShader:
			for s in self.shaders:
				id = s.getMember("id")
				if id>highest:
					highest=id
		elif typec==GameFont:
			for s in self.fonts:
				id = s.getMember("id")
				if id>highest:
					highest=id
		elif typec==GameTimeline:
			for s in self.timelines:
				id = s.getMember("id")
				if id>highest:
					highest=id
		elif typec==GameObject:
			for s in self.objects:
				id = s.getMember("id")
				if id>highest:
					highest=id
		elif typec==GameRoom:
			for s in self.rooms:
				id = s.getMember("id")
				if id>highest:
					highest=id
		return highest

	def GetResource(self, typec, index):
		if type(typec)==str:
			typec=eval(typec)
		if typec==GameSprite:
			for s in self.sprites:
				if s.getMember("id")==index:
					return s
		elif typec==GameSound:
			for s in self.sounds:
				if s.getMember("id")==index: return s
		elif typec==GameBackground:
			for s in self.backgrounds:
				if s.getMember("id")==index: return s
		elif typec==GamePath:
			for s in self.paths:
				if s.getMember("id")==index: return s
		elif typec==GameScript:
			for s in self.scripts:
				if s.getMember("id")==index: return s
		elif typec==GameShader:
			for s in self.shaders:
				if s.getMember("id")==index: return s
		elif typec==GameFont:
			for s in self.fonts:
				if s.getMember("id")==index: return s
		elif typec==GameTimeline:
			for s in self.timelines:
				if s.getMember("id")==index: return s
		elif typec==GameObject:
			for s in self.objects:
				if s.getMember("id")==index: return s
		elif typec==GameRoom:
			for s in self.rooms:
				if s.getMember("id")==index: return s
		return None

	def GetResourceName(self, type, name):
		if type==GameSprite:
			for s in self.sprites:
				if s.getMember("name")==name:
					return s
		elif type==GameSound:
			for s in self.sounds:
				if s.getMember("name")==name: return s
		elif type==GameBackground:
			for s in self.backgrounds:
				if s.getMember("name")==name: return s
		elif type==GamePath:
			for s in self.paths:
				if s.getMember("name")==name: return s
		elif type==GameScript:
			for s in self.scripts:
				if s.getMember("name")==name: return s
		elif type==GameShader:
			for s in self.shaders:
				if s.getMember("name")==name: return s
		elif type==GameFont:
			for s in self.fonts:
				if s.getMember("name")==name: return s
		elif type==GameTimeline:
			for s in self.timelines:
				if s.getMember("name")==name: return s
		elif type==GameObject:
			for s in self.objects:
				if s.getMember("name")==name: return s
		elif type==GameRoom:
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

	def ReadEgm(self, filename):
		z=zipfile.ZipFile(filename, "r")
		f=z.open("Enigma Settings.eef", "rU")
		global tempeef
		tempeef=tempfile.NamedTemporaryFile()
		tempeef=open(tempeef.name+".eef", "wb")
		self.EnigmaSettingsEefData=f.read()
		tempeef.write(self.EnigmaSettingsEefData)
		f.close()
		tempeef.seek(0)
		self.EnigmaSettingsEef=tempeef.name

		self.egmNames=z.namelist()
		self.guid=[1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 0, 0, 0, 0, 0, 0]
		self.resourceTree = GameTree(self)
		self.resourceTree.AddGroupName("Sprites")
		self.resourceTree.AddGroupName("Sounds")
		self.resourceTree.AddGroupName("Backgrounds")
		self.resourceTree.AddGroupName("Paths")
		self.resourceTree.AddGroupName("Scripts")
		self.resourceTree.AddGroupName("Shaders")
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
		self.egmReadNodeChildren(z, res, "notype", "")
		for e in self.egmEntries:
			self.egmProcesEntry(*e)
		self.Finalize()

	def egmReadNodeChildren(self, z, parent, kind, dir):
		if dir=="":
			f=z.open("toc.txt", "rU")
		else:
			f=z.open(dir+"/toc.txt", "rU")
		toc=[]
		for t in f.readlines():
			entry = t.decode().strip()
			if len(entry) > 4 and entry[3] == " " and entry[:3].isupper():
				#oldKind=kind
				kind,entry = entry[0:3],entry[4:]
				#if oldKind!=kind:
				#	print_warning("kind changed "+kind+" "+oldKind)
			toc.append((kind,entry))
		self.egmProcessEntries(z,parent,toc,dir);

	def egmProcessEntries(self, z, parent, entries, dir):
		for kind,entry in entries:
			if dir!="":
				entry = dir + "/" + entry
			if entry+"/toc.txt" in self.egmNames:
				parent[entry]={}
				self.egmReadNodeChildren(z,parent[entry],kind,entry);
			else:
				if entry+".ey" in self.egmNames:#if (f.exists())
					parent[entry]={}
					self.egmId[kind]=self.egmId.get(kind,-1)+1
					self.egmNameId[os.path.split(entry)[1]]=self.egmId[kind]
					self.egmEntries.append((z,kind,entry,self.egmId[kind]))
				elif entry=="null":
					1
				else:
					print_warning("Extraneous TOC entry: "+entry)

	def egmProcesEntry(self, z, kind, entry, id):
		if kind=="EGS":
			pass
		elif kind=="GMS":
			self.configs=[]
			self.configs.append(GameSettings(self))
			self.configs[0].ReadEgm(entry, z)
		# Load triggers
		# Load constants
		elif kind=="SND":
			s = GameSound(self, id)
			s.ReadEgm(entry, z)
			self.sounds.append(s)
			self.resourceTree.AddResourcePath(entry, s)
		elif kind=="SPR":
			s = GameSprite(self, id)
			s.ReadEgm(entry, z)
			self.sprites.append(s)
			self.resourceTree.AddResourcePath(entry, s)
		elif kind=="BKG":
			s = GameBackground(self, id)
			s.ReadEgm(entry, z)
			self.backgrounds.append(s)
			self.resourceTree.AddResourcePath(entry, s)
		elif kind=="PTH":
			s = GamePath(self, id)
			s.ReadEgm(entry, z)
			self.paths.append(s)
			self.resourceTree.AddResourcePath(entry, s)
		elif kind=="SCR":
			s = GameScript(self, id)
			s.ReadEgm(entry, z)
			self.scripts.append(s)
			self.resourceTree.AddResourcePath(entry, s)
		elif kind=="SHR":
			s = GameShader(self, id)
			s.ReadEgm(entry, z)
			self.shaders.append(s)
			self.resourceTree.AddResourcePath(entry, s)
		elif kind=="FNT":
			s = GameFont(self, id)
			s.ReadEgm(entry, z)
			self.fonts.append(s)
			self.resourceTree.AddResourcePath(entry, s)
		elif kind=="TML":
			s = GameTimeline(self, id)
			s.ReadEgm(entry, z)
			self.timelines.append(s)
			self.resourceTree.AddResourcePath(entry, s)
		elif kind=="OBJ":
			s = GameObject(self, id)
			s.ReadEgm(entry, z)
			self.objects.append(s)
			self.resourceTree.AddResourcePath(entry, s)
		elif kind=="RMM":
			s = GameRoom(self, id)
			s.ReadEgm(entry, z)
			self.rooms.append(s)
			self.resourceTree.AddResourcePath(entry, s)
		# Load last ids
		# Load include files
		# Load packages
		elif kind=="GMI":
			self.gameInformation = GameInformation(self)
			self.gameInformation.ReadEgm(entry, z)
		# Read library creation code -- we should be able to safely ignore this
		# Read room execution order -- this too
		# Read resource tree
		elif kind=="EXT":
			pass
		else:
			print_error("unsupported toc.txt kind "+kind+" "+entry)

	def ReadGmz(self, filename):
		tempDir=tempfile.mkdtemp()
		print_notice("temp dir "+tempDir)
		print_notice(subprocess.check_output(["7zr", "x","-o"+tempDir,filename]))
		x=subprocess.check_output("ls "+os.path.join(tempDir,"*.project.gmx"),shell=True).strip()
		self.ReadGmx(x)
		if tempDir.startswith("/tmp/tmp"):
			shutil.rmtree(tempDir)
		else:
			print_error("error dir"+tempDir)

	def ReadGmx(self, filename):
		rootDir, gmxProjectFile=self.GmxSplitPath(filename)
		self.resourceTree = GameTree(self)
		self.resourceTree.NewTree()
		gmxPath=os.path.join(rootDir, gmxProjectFile)
		tree=xml.etree.ElementTree.parse(gmxPath)
		root=tree.getroot()
		self.gmxRoot=root
		if root.tag!="assets":
			print_error("tag isn't assets "+root.tag)
		seen={}
		self.egmNameId={}
		self.egmNameId["<undefined>"] = -1
		self.configs=[]
		self.gameInformation = GameInformation(self)
		for child in root:
			if seen.get(child.tag,0)>0:
				print_error("duplicated tag "+child.tag)
			seen[child.tag]=seen.get(child.tag, 0)+1
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
				self.ReadGmxResourceNames("sounds", "sound", child, self.egmNameId)
			elif child.tag=="sprites":
				self.ReadGmxResourceNames("sprites", "sprite", child, self.egmNameId)
			elif child.tag=="backgrounds":
				self.ReadGmxResourceNames("backgrounds", "background", child, self.egmNameId)
			elif child.tag=="paths":
				self.ReadGmxResourceNames("paths", "path", child, self.egmNameId)
			elif child.tag=="scripts":
				self.ReadGmxResourceNames("scripts", "script", child, self.egmNameId)
			elif child.tag=="shaders":
				self.ReadGmxResourceNames("shaders", "shader", child, self.egmNameId)
			elif child.tag=="fonts":
				self.ReadGmxResourceNames("fonts", "font", child, self.egmNameId)
			elif child.tag=="objects":
				self.ReadGmxResourceNames("objects", "object", child, self.egmNameId)
			elif child.tag=="timelines":
				self.ReadGmxResourceNames("timelines", "timeline", child, self.egmNameId)
			elif child.tag=="rooms":
				self.ReadGmxResourceNames("rooms", "room", child, self.egmNameId)
			elif child.tag=="TutorialState":
				pass
			elif child.tag=="constants":
				pass
			else:
				print_error("unsupported tag "+child.tag)
		for child in root:
			if child.tag=="Configs":
				#<Configs name="configs"><Config>Configs\Default</Config></Configs>
				if len(child)>1:
					print_notice("more than 1 Config")
				for chil in child:
					if chil.tag=="Config":
						configPathText=chil.text.replace("\\","/")
						configPath,configName=os.path.split(configPathText)
						absConfigPath=os.path.join(rootDir, configPath)
						self.ReadGmxConfig(absConfigPath, configName)
					else:
						print_error("tag isn't Config "+chil.tag)
			elif child.tag=="datafiles":
				pass
			elif child.tag=="options":
				if len(self.configs)>0:
					print_warning("gmx Configs and options")
				settings = GameSettings(self)
				self.gameInformation = GameInformation(self)
				settings.ReadGmx(child)
				self.configs.append(settings)
			elif child.tag=="help":
				#<help><rtf>help.rtf</rtf></help>
				pass
				#self.gameInformation=
			elif child.tag=="NewExtensions":
				#<NewExtensions><extension index="0">extensions\Extension1</extension></NewExtensions>
				pass
			elif child.tag=="sounds":
				#<sounds name="sound"><sound>sound\sound0</sound></sounds>
				self.ReadGmxResources("sounds", "sound", child, child.attrib["name"], rootDir)
			elif child.tag=="sprites":
				#<sprites name="sprites"><sprite>sprites\sprite0</sprite></sprites>
				self.ReadGmxResources("sprites", "sprite", child, child.attrib["name"], rootDir)
			elif child.tag=="backgrounds":
				#<backgrounds name="background"><background>background\background0</background></backgrounds>
				self.ReadGmxResources("backgrounds", "background", child, child.attrib["name"], rootDir)
			elif child.tag=="paths":
				#<paths name="paths"><path>paths\path0</path></paths>
				self.ReadGmxResources("paths", "path", child, child.attrib["name"], rootDir)
			elif child.tag=="scripts":
				#<scripts name="scripts"><script>scripts\script0.gml</script></scripts>
				self.ReadGmxResources("scripts", "script", child, child.attrib["name"], rootDir)
			elif child.tag=="shaders":
				self.ReadGmxResources("shaders", "shader", child, child.attrib["name"], rootDir)
			elif child.tag=="fonts":
				#<fonts name="fonts"><font>fonts\font0</font></fonts>
				self.ReadGmxResources("fonts", "font", child, child.attrib["name"], rootDir)
			elif child.tag=="objects":
				#<objects name="objects"><object>objects\object0</object></objects>
				self.ReadGmxResources("objects", "object", child, child.attrib["name"], rootDir)
			elif child.tag=="timelines":
				#<timelines name="timelines"><timeline>timelines\timeline0</timeline></timelines>
				self.ReadGmxResources("timelines", "timeline", child, child.attrib["name"], rootDir)
			elif child.tag=="rooms":
				#<rooms name="rooms"><room>rooms\room0</room></rooms>
				self.ReadGmxResources("rooms", "room", child, child.attrib["name"], rootDir)
			elif child.tag=="TutorialState":
				#<TutorialState><IsTutorial>0</IsTutorial><TutorialName></TutorialName><TutorialPage>0</TutorialPage></TutorialState>
				pass
			elif child.tag=="constants":
				#<constants number="23"><constant name="VersionMajor">1</constant>
				pass
			else:
				print_error("unsupported tag "+child.tag)
		self.Finalize()

	def ReadGmxConfig(self, gmxDir, gmxName):
		gmxPath=os.path.join(gmxDir, gmxName)+".config.gmx"
		tree=xml.etree.ElementTree.parse(gmxPath)
		root=tree.getroot()
		if root.tag!="Config":
			print_error("tag isn't Config "+root.tag)
		settings = GameSettings(self)
		settings.ReadGmx(root)
		self.configs.append(settings)

	def WriteGmxResource(self, gmxDir, name, res, gmxExtension, rootTagName):
		if not os.path.exists(gmxDir):
			os.mkdir(gmxDir)
		gmxPath=os.path.join(gmxDir, name)+"."+gmxExtension+".gmx"
		writeFile=open(gmxPath, "w")
		root=xml.etree.ElementTree.Element(rootTagName)
		root.tail="\n"
		if rootTagName in ["sprite","background"]:
			res.WriteGmx(root, gmxDir)
		else:
			res.WriteGmx(root)
		writeFile.write(xml.etree.ElementTree.tostring(root).decode())
		writeFile.close()

	def ReadGmxResourceNames(self, groupTagName, resourceTagName, groupTag, nameId, startId=0):
		c=startId
		for chil in groupTag:
			if chil.tag==resourceTagName:
				pathText=chil.text.replace("\\","/")
				resourceNameExt=os.path.split(pathText)[1]
				resourceName=os.path.splitext(resourceNameExt)[0]
				nameId[resourceName]=c
				c+=1
			elif chil.tag==groupTagName:
				self.ReadGmxResourceNames(groupTagName, resourceTagName, chil, nameId, c)
			else:
				print_error("tag is "+chil.tag+" "+resourceTagName)

	def ReadGmxResources(self, groupTagName, resourceTagName, groupTag, path, rootDir, startId=0):
		c=startId
		for chil in groupTag:
			if chil.tag==resourceTagName:
				filep=chil.text.replace("\\","/")
				groupPath=path+"/"+filep.split("/")[1]
				p,iname=os.path.split(filep)
				p=os.path.join(rootDir, p)
				if resourceTagName=="sound":
					s = GameSound(self,c)
					self.sounds.append(s)
				elif resourceTagName=="sprite":
					s = GameSprite(self,c)
					self.sprites.append(s)
				elif resourceTagName=="background":
					s = GameBackground(self,c)
					self.backgrounds.append(s)
				elif resourceTagName=="path":
					s = GamePath(self,c)
					self.paths.append(s)
				elif resourceTagName=="script":
					s = GameScript(self,c)
					self.scripts.append(s)
					groupPath=os.path.splitext(groupPath)[0]
				elif resourceTagName=="shader":
					s = GameShader(self,c)
					s.setMember("type",chil.get("type"))
					self.shaders.append(s)
					groupPath=os.path.splitext(groupPath)[0]
				elif resourceTagName=="font":
					s = GameFont(self,c)
					self.fonts.append(s)
				elif resourceTagName=="object":
					s = GameObject(self,c)
					self.objects.append(s)
				elif resourceTagName=="timeline":
					s = GameTimeline(self,c)
					self.timelines.append(s)
				elif resourceTagName=="room":
					s = GameRoom(self,c)
					self.rooms.append(s)
				else:
					print_error("unsupported resource "+resourceTagName)
				s.setMember("name",iname)
				s.ReadGmx(self,p,iname)
				if groupPath.startswith("sound/"):
					groupPath="Sounds/"+groupPath[len("sound/"):]
				if groupPath.startswith("background/"):
					groupPath="Backgrounds/"+groupPath[len("background/"):]
				if groupPath.startswith("shaders/"):
					groupPath="Shaders/"+groupPath[len("shaders/"):]
				self.resourceTree.AddResourcePath(groupPath,s)
				c+=1
			elif chil.tag==groupTagName:
				self.ReadGmxResources(groupTagName, resourceTagName, chil, path+"/"+chil.attrib["name"], rootDir, c)
			else:
				print_error("tag is "+chil.tag+" "+resourceTagName)

	def GmxSplitPath(self, filename):
		if os.path.isdir(filename):
			if filename[-1] in ["/","\\"]:
				filename=filename[:-1]
			baseDir=filename
			baseDirNameExt=os.path.split(baseDir)[1]
			baseDirName=os.path.splitext(baseDirNameExt)[0]
			gmxProjectFile=baseDirName+".project.gmx"
		else:
			baseDir, gmxProjectFile=os.path.split(filename)
		return baseDir, gmxProjectFile

	def ReadGmk(self, stream):
		if stream.ReadDword() != self.GMK_MAGIC:
			print_error("Invalid magic")
		self.gmkVersion=stream.ReadDword()
		#if self.gmkVersion==530:
		#elif self.gmkVersion==600:
		#elif self.gmkVersion==701:
		if self.gmkVersion not in [800,810]:
			print_warning("Unknown or unsupported version "+str(self.gmkVersion))
		if self.gmkVersion>=700 and self.gmkVersion<800:
			#Gmkrypt gmkrypt(Gmkrypt::ReadSeedFromJunkyard(stream));
			stream = stream.Decrypt()
		self.gameId = stream.ReadDword()
		self.guid=[]
		for i in range(self.GMK_GUID_LENGTH):
			self.guid.append(stream.readUChar())
		gmVersionGameSettings=stream.ReadDword()
		if gmVersionGameSettings not in [800,820]:
			print_warning("unsupported gmk version "+str(gmVersionGameSettings))
		self.configs = []
		self.configs.append(GameSettings(self))
		self.configs[0].ReadGmk(stream)
		if self.gmkVersion>=800:
			gmVersionTriggers=stream.ReadDword()
			if gmVersionTriggers != 800:
				print_error("unsupported gmk version "+str(gmVersionTriggers))
			count = stream.ReadDword()
			for c in range(count):
				trigger = GameTrigger(self,c)
				trigger.ReadGmk(stream)
				self.triggers.append(trigger)
			#Last time Triggers were changed
			stream.ReadTimestamp()
			# Load constants
			#GM version needed for Resource
			stream.ReadDword()
			count = stream.ReadDword()
			for c in range(count):
				name = stream.ReadString()
				value = stream.ReadString()
				self.constants.append((name, value))
			#Last time Constants were changed
			stream.ReadTimestamp()
		# Load sounds
		#GM version needed for Resource
		stream.ReadDword()
		count = stream.ReadDword()
		for c in range(count):
			sound = GameSound(self, c)
			sound.ReadGmk(stream)
			if sound.exists:
				self.sounds.append(sound)
		# Load sprites
		#GM version needed for Resource
		stream.ReadDword()
		count = stream.ReadDword()
		for c in range(count):
			sprite = GameSprite(self, c)
			sprite.ReadGmk(stream)
			if sprite.exists:
				self.sprites.append(sprite)
		# Load backgrounds
		#GM version needed for Resource
		stream.ReadDword()
		count = stream.ReadDword()
		for c in range(count):
			background = GameBackground(self, c)
			background.ReadGmk(stream)
			if background.exists:
				self.backgrounds.append(background)
		# Load paths
		#GM version needed for Resource
		stream.ReadDword()
		count = stream.ReadDword()
		for c in range(count):
			path = GamePath(self, c)
			path.ReadGmk(stream)
			self.paths.append(path)
		# Load scripts
		#GM version needed for Resource
		stream.ReadDword()
		count = stream.ReadDword()
		for c in range(count):
			script = GameScript(self, c)
			script.ReadGmk(stream)
			self.scripts.append(script)
		# Load fonts
		#GM version needed for Resource
		stream.ReadDword()
		count = stream.ReadDword()
		for c in range(count):
			font = GameFont(self, c)
			font.ReadGmk(stream)
			self.fonts.append(font)
		# Load timelines
		#GM version needed for Resource
		stream.ReadDword()
		count = stream.ReadDword()
		for c in range(count):
			timeline = GameTimeline(self, c)
			timeline.ReadGmk(stream)
			if timeline.exists:
				print_error("timeline unsupported")
				self.timelines.append(timeline)
		# Load objects
		#GM version needed for Resource
		stream.ReadDword()
		count = stream.ReadDword()
		for c in range(count):
			gmObject = GameObject(self, c)
			gmObject.ReadGmk(stream)
			if gmObject.exists:
				self.objects.append(gmObject)
		# Load rooms
		#GM version needed for Resource
		stream.ReadDword()
		count = stream.ReadDword()
		for c in range(count):
			room = GameRoom(self, c)
			room.ReadGmk(stream)
			if room.exists:
				self.rooms.append(room)
		# Load last ids
		self.lastInstancePlacedId = stream.ReadDword()
		self.lastTilePlacedId = stream.ReadDword()
		if self.gmkVersion>=700:
			# Load include files
			#GM version needed for Resource
			stream.ReadDword()
		if self.gmkVersion>=620:
			count = stream.ReadDword()
			for c in range(count):
				includeFile = GameIncludeFile(self, c)
				includeFile.ReadGmk(stream)
				self.includeFiles.append(includeFile)
		if self.gmkVersion>=700:
			# Load packages
			#GM version needed for Resource
			stream.ReadDword()
			count = stream.ReadDword()
			for c in range(count):
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
		for c in range(count):
			print_warning("library creation code "+stream.ReadString())
		# Read room execution order -- this too
		#GM version needed for Resource
		stream.ReadDword()
		count = stream.ReadDword()
		for c in range(count):
			print_warning("room execution order "+str(stream.ReadDword()))
		# Read resource tree
		self.resourceTree = GameTree(self)
		self.resourceTree.ReadGmk(stream)
		self.Finalize()

	def ReadEGP(self, filename):
		pass

	def ReadGGGStream(self, stream):
		GGGLexer(stream)

	def ReadGGGFile(self, filename):
		data = open(filename, "rb")
		stream = BinaryStream(data)
		self.ReadGGGStream(stream)

	def Read(self, filename):
		if os.path.isdir(filename):
			if filename[-1] in ["/","\\"]:
				filename=filename[:-1]
		self.ifReadingFile=True
		ext=os.path.splitext(filename)[1]
		if ext in [".gmd",".gm6",".gmk",".gm81"] or ext.startswith(".gb"):
			data = open(filename, "rb")
			stream = BinaryStream(data)
			self.ReadGmk(stream)
		elif ext==".egm":
			self.ReadEgm(filename)
		elif ext==".gmx":
			self.ReadGmx(filename)
		elif ext==".gmz":
			self.ReadGmz(filename)
		elif ext==".egp":
			self.ReadEGP(filename)
		elif ext==".ggg":
			self.ReadGGGFile(filename)
		else:
			print_error("unsupported load format")
		self.ifReadingFile=False

	def SaveEGP(self, filename):
		if not os.path.exists(filename):
			os.mkdir(filename)
		if not os.path.isdir(filename):
			filename=os.path.split(filename)[0]
			if not os.path.splitext(filename)[1]==".egp":
				print_error("egp has to be a directory ending in .egp")
				return
		baseDir=filename
		constantsFile=open(os.path.join(baseDir, "constants.ini"), "w")
		constantsFile.write("")
		constantsFile.close()
		egpFile=open(os.path.join(baseDir, "game.egp"), "w")
		egpFile.close()
		#constantsFile=open(os.path.join(baseDir, "information.rtf"), "w")
		#constantsFile=open(os.path.join(baseDir, "enigma.ey"), "w")
		for s in self.resourceTree.contents:
			if s.group=="Sounds":
				self.SaveRecursiveEgpTree(baseDir, s, "sound", et, "sound", "sounds")
			elif s.group=="Sprites":
				self.SaveRecursiveEgpTree(baseDir, s, "sprites", et, "sprite", "sprites")
			elif s.group=="Backgrounds":
				self.SaveRecursiveEgpTree(baseDir, s, "background", et, "background", "backgrounds")
			elif s.group=="Paths":
				self.SaveRecursiveEgpTree(baseDir, s, "paths", et, "path", "paths")
			elif s.group=="Scripts":
				self.SaveRecursiveEgpTree(baseDir, s, "scripts", et, "script", "scripts")
			elif s.group=="Shaders":
				self.SaveRecursiveEgpTree(baseDir, s, "shaders", et, "shader", "shaders")
			elif s.group=="Fonts":
				self.SaveRecursiveEgpTree(baseDir, s, "fonts", et, "font", "fonts")
			elif s.group=="Objects":
				self.SaveRecursiveEgpTree(baseDir, s, "objects", et, "object", "objects")
			elif s.group=="Timelines":
				self.SaveRecursiveEgpTree(baseDir, s, "timelines", et, "timeline", "timelines")
			elif s.group=="Rooms":
				self.SaveRecursiveEgpTree(baseDir, s, "rooms", et, "room", "rooms")
			else:
				print_warning("unsupported group type "+s.group)

	def SaveRecursiveEgpTree(self, baseDir, node, path):
		pass

	def SaveGmx(self, filename):
		if not os.path.exists(filename):
			if filename.endswith(".project.gmx"):
				print_error("unsupported save to .project.gmx file")
			else:
				os.mkdir(filename)
		baseDir, gmxProjectFile=self.GmxSplitPath(filename)
		gmxPath=os.path.join(baseDir, gmxProjectFile)
		writeFile=open(gmxPath, "w")
		#writeFile.write("<!--This Document is generated by GameMaker, if you edit it by hand then you do so at your own risk!-->\n")
		self.gmxRoot=None
		if not self.gmxRoot:
			self.gmxRoot=xml.etree.ElementTree.Element("assets")
			self.gmxRoot.tail="\n"
			Configs=xml.etree.ElementTree.Element("Configs")
			Configs.tail="\n"
			Configs.set("name","configs")
			self.gmxRoot.append(Configs)
			for config in self.configs:
				Config=xml.etree.ElementTree.Element("Config")
				Config.tail="\n"
				Configs.append(Config)
				Config.text="Configs\\"+config.name
				self.WriteGmxResource(os.path.join(baseDir,"Configs"), config.name, config, "config", "Config")
			NewExtensions=xml.etree.ElementTree.Element("NewExtensions")
			NewExtensions.tail="\n"
			self.gmxRoot.append(NewExtensions)
			for s in self.resourceTree.contents:
				if s.group=="Sounds":
					et=xml.etree.ElementTree.Element("sounds")
					et.set("name","sound")
					self.gmxRoot.append(et)
					self.SaveRecursiveGmxTree(baseDir, s, "sound", et, "sound", "sounds")
				elif s.group=="Sprites":
					et=xml.etree.ElementTree.Element("sprites")
					et.set("name","sprites")
					self.gmxRoot.append(et)
					self.SaveRecursiveGmxTree(baseDir, s, "sprites", et, "sprite", "sprites")
				elif s.group=="Backgrounds":
					et=xml.etree.ElementTree.Element("backgrounds")
					et.set("name","background")
					self.gmxRoot.append(et)
					self.SaveRecursiveGmxTree(baseDir, s, "background", et, "background", "backgrounds")
				elif s.group=="Paths":
					et=xml.etree.ElementTree.Element("paths")
					et.set("name","paths")
					self.gmxRoot.append(et)
					self.SaveRecursiveGmxTree(baseDir, s, "paths", et, "path", "paths")
				elif s.group=="Scripts":
					et=xml.etree.ElementTree.Element("scripts")
					et.set("name","scripts")
					self.gmxRoot.append(et)
					self.SaveRecursiveGmxTree(baseDir, s, "scripts", et, "script", "scripts")
				elif s.group=="Shaders":
					et=xml.etree.ElementTree.Element("shaders")
					et.set("name","shaders")
					self.gmxRoot.append(et)
					self.SaveRecursiveGmxTree(baseDir, s, "shaders", et, "shader", "shaders")
				elif s.group=="Fonts":
					et=xml.etree.ElementTree.Element("fonts")
					et.set("name","fonts")
					self.gmxRoot.append(et)
					self.SaveRecursiveGmxTree(baseDir, s, "fonts", et, "font", "fonts")
				elif s.group=="Objects":
					et=xml.etree.ElementTree.Element("objects")
					et.set("name","objects")
					self.gmxRoot.append(et)
					self.SaveRecursiveGmxTree(baseDir, s, "objects", et, "object", "objects")
				elif s.group=="Timelines":
					et=xml.etree.ElementTree.Element("timelines")
					et.set("name","timelines")
					self.gmxRoot.append(et)
					self.SaveRecursiveGmxTree(baseDir, s, "timelines", et, "timeline", "timelines")
				elif s.group=="Rooms":
					et=xml.etree.ElementTree.Element("rooms")
					et.set("name","rooms")
					self.gmxRoot.append(et)
					self.SaveRecursiveGmxTree(baseDir, s, "rooms", et, "room", "rooms")
				else:
					print_warning("unsupported group type "+s.group)
			help=xml.etree.ElementTree.Element("help")
			help.tail="\n"
			self.gmxRoot.append(help)
			rtf=xml.etree.ElementTree.Element("rtf")
			rtf.tail="\n"
			rtf.text="help.rtf"
			help.append(rtf)
			#clifix GameInformation
			TutorialState=xml.etree.ElementTree.Element("TutorialState")
			TutorialState.tail="\n"
			self.gmxRoot.append(TutorialState)
			IsTutorial=xml.etree.ElementTree.Element("IsTutorial")
			IsTutorial.tail="\n"
			IsTutorial.text="0"
			TutorialState.append(IsTutorial)
			TutorialName=xml.etree.ElementTree.Element("TutorialName")
			TutorialName.tail="\n"
			TutorialName.text=""
			TutorialState.append(TutorialName)
			TutorialPage=xml.etree.ElementTree.Element("TutorialPage")
			TutorialPage.tail="\n"
			TutorialPage.text="0"
			TutorialState.append(TutorialPage)
		writeFile.write(xml.etree.ElementTree.tostring(self.gmxRoot).decode())
		writeFile.close()

	def SaveRecursiveGmxTree(self, baseDir, resourceTreeNode, path, et, resourceTagName, groupTagName):
		for sc in resourceTreeNode.contents:
			if sc.status==GameTree.StatusPrimary:
				sounds=xml.etree.ElementTree.Element(groupTagName)
				sounds.tail="\n"
				sounds.set("name",sc.name)
				et.append(sounds)
				self.SaveRecursiveGmxTree(baseDir, sc, path, sounds, resourceTagName, groupTagName)
			else:
				sound=xml.etree.ElementTree.Element(resourceTagName)
				sound.text=path+"\\"+sc.resource.getMember("name")
				sound.tail="\n"
				if resourceTagName in ["sound", "sprite", "background", "path", "font", "object", "timeline", "room"]:
					self.WriteGmxResource(os.path.join(baseDir, path), sc.resource.getMember("name"), sc.resource, resourceTagName, resourceTagName)
				elif resourceTagName=="script":
					if not os.path.exists(os.path.join(baseDir, path)):
						os.mkdir(os.path.join(baseDir, path))
					gmxPath=os.path.join(baseDir, path, sc.resource.getMember("name"))+".gml"
					writeFile=open(gmxPath,"w")
					writeFile.write(sc.resource.getMember("value"))#.decode())
					writeFile.close()
					sound.text=path+"\\"+sc.resource.getMember("name")+".gml"
				elif resourceTagName=="shader":
					if not os.path.exists(os.path.join(baseDir, path)):
						os.mkdir(os.path.join(baseDir, path))
					gmxPath=os.path.join(baseDir, path, sc.resource.getMember("name"))+".shader"
					sc.resource.WriteGmxShader(gmxPath)
					sound.text=path+"\\"+sc.resource.getMember("name")+".shader"
				else:
					print_error("what tag "+resourceTagName)
				et.append(sound)

	def SaveGmk(self, stream):
		stream = BinaryStream(stream)
		# Write header
		stream.WriteDword(GameFile.GMK_MAGIC)
		stream.WriteDword(810)
		# Write header
		stream.WriteDword(self.gameId)
		for i in range(self.GMK_GUID_LENGTH):
			guidByte = self.gameId >> int(i / 4)
			guidByte %= ((i >> 6) + guidByte & 0x7F) + 0xFF
			guidByte ^= (i * guidByte >> 3) & 0xAB
			if guidByte>256:#clifix
				guidByte=0
			stream.WriteByte(chr(guidByte))
		# Write settings
		stream.WriteDword(800)
		if len(self.configs) == 0:
			raise "Settings are not declared"
		self.configs[0].WriteGmk(stream)
		# Write triggers
		stream.WriteDword(800)
		stream.WriteDword(len(self.triggers))
		for i in range(len(self.triggers)):
			self.triggers[i].WriteGmk(stream)
		stream.WriteTimestamp()
		# Write constants
		stream.WriteDword(800)
		stream.WriteDword(len(self.constants))
		for i in range(len(self.constants)):
			stream.WriteString(self.constants[i][0])
			stream.WriteString(self.constants[i][1])
		stream.WriteTimestamp()
		# Write sounds
		stream.WriteDword(800)
		stream.WriteDword(len(self.sounds))
		for i in range(len(self.sounds)):
			self.sounds[i].WriteGmk(stream)
		# Write sprites
		stream.WriteDword(800)
		stream.WriteDword(len(self.sprites))
		for i in range(len(self.sprites)):
			self.sprites[i].WriteGmk(stream)
		# Write backgrounds
		stream.WriteDword(800)
		stream.WriteDword(len(self.backgrounds))
		for i in range(len(self.backgrounds)):
			self.backgrounds[i].WriteGmk(stream)
		# Write paths
		stream.WriteDword(800)
		stream.WriteDword(len(self.paths))
		for i in range(len(self.paths)):
			self.paths[i].WriteGmk(stream)
		# Write scripts
		stream.WriteDword(800)
		stream.WriteDword(len(self.scripts))
		for i in range(len(self.scripts)):
			self.scripts[i].WriteGmk(stream)
		# Write fonts
		stream.WriteDword(800)
		stream.WriteDword(len(self.fonts))
		for i in range(len(self.fonts)):
			self.fonts[i].WriteGmk(stream)
		# Write timelines
		stream.WriteDword(800)
		stream.WriteDword(len(self.timelines))
		for i in range(len(self.timelines)):
			self.timelines[i].WriteGmk(stream)
		# Write objects
		stream.WriteDword(800)
		stream.WriteDword(len(self.objects))
		for i in range(len(self.objects)):
			self.objects[i].WriteGmk(stream)
		# Write rooms
		stream.WriteDword(800)
		stream.WriteDword(len(self.rooms))
		for i in range(len(self.rooms)):
			self.rooms[i].WriteGmk(stream)
		# Write last ids
		stream.WriteDword(self.lastInstancePlacedId)
		stream.WriteDword(self.lastTilePlacedId)
		# Write include files
		stream.WriteDword(800)
		stream.WriteDword(len(self.includeFiles))
		for i in range(len(self.includeFiles)):
			self.includeFiles[i].WriteGmk(stream)
		# Write packages
		stream.WriteDword(700)
		stream.WriteDword(len(self.packages))
		for i in range(len(self.packages)):
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
		if not self.resourceTree:
			print_error("None resource tree")
			self.AddResourceTree()
		self.resourceTree.WriteGmk(stream)

	def SaveEgm(self, filename):
		z=zipfile.ZipFile(filename, "w")
		toc=""
		for s in self.resourceTree.contents:
			if s.group=="Sprites":
				toc += self.SaveEgmRecursiveTree("SPR", "Sprites", s)
			elif s.group=="Sounds":
				toc += self.SaveEgmRecursiveTree("SND", "Sounds", s)
			elif s.group=="Backgrounds":
				toc += self.SaveEgmRecursiveTree("BKG", "Backgrounds", s)
			elif s.group=="Paths":
				toc += self.SaveEgmRecursiveTree("PTH", "Paths", s)
			elif s.group=="Scripts":
				toc += self.SaveEgmRecursiveTree("SCR", "Scripts", s)
			elif s.group=="Shaders":
				toc += self.SaveEgmRecursiveTree("SHR", "Shaders", s)
			elif s.group=="Fonts":
				toc += self.SaveEgmRecursiveTree("FNT", "Fonts", s)
			elif s.group=="Timelines":
				toc += self.SaveEgmRecursiveTree("TML", "Time Lines", s)
			elif s.group=="Objects":
				toc += self.SaveEgmRecursiveTree("OBJ", "Objects", s)
			elif s.group=="Rooms":
				toc += self.SaveEgmRecursiveTree("RMM", "Rooms", s)
		toc += "GMI\tGame Information"
		self.gameInformation.SaveEgm(self, z)
		toc += "GMS\tGlobal Game Settings"
		self.configs[0].SaveEgm(self, z)
		toc += "EGS\tEnigma Settings"
		if self.EnigmaSettingsEefData:
			z.writestr("Enigma Settings.eef", self.EnigmaSettingsEefData)
		z.writestr("Enigma Settings.ey", self.EnigmaSettingsEy())
		z.writestr("toc.txt", toc)
		z.close()

	def SaveEgmRecursiveTree(self, type, path, node):
		for s in node.contents:
			print(s)
		return type+"\t"+path

	def Save(self, filename):
		if os.path.isdir(filename):
			if filename[-1] in ["/","\\"]:
				filename=filename[:-1]
		self.SaveExt(os.path.splitext(filename)[1], filename)

	def SaveExt(self, ext, filename, wfile=None):
		if ext in [".gmk",".gm81"]:
			stream=open(filename, "wb")
			self.SaveGmk(stream)
		elif ext == ".egm":
			self.SaveEgm(filename)
		elif ext == ".gmx":
			self.SaveGmx(filename)
		elif ext == ".gmz":
			self.SaveGmz(filename)
		elif ext == ".egp":
			self.SaveEGP(filename)
		elif ext == ".ggg":
			ggg=self.WriteGGG()
			if not wfile:
				wfile=open(filename,"wb")
			wfile.write(ggg.encode())
		else:
			print_error("unsupported save format")

	def Backup(self, filename):
		if os.path.exists(filename):
			x=1
			while 1:
				path=filename+".backup"+str(x)
				x=x+1
				if not os.path.exists(path):
					print_notice("backed up to "+path)
					if os.path.isdir(filename):
						print_warning("cant backup dir")
					else:
						shutil.copy(filename, path)
					return

	def WriteGGG(self):
		stri=""
		stri+="lastInstancePlacedId="+str(self.lastInstancePlacedId)+"\n"
		stri+="lastTilePlacedId="+str(self.lastTilePlacedId)+"\n"
		for c in self.configs:
			stri+=c.WriteGGG()
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

	@staticmethod
	def compileRunES(es, exePath, emode, EnigmaSettingsEy):
		#print_warning("modified "+EnigmaSettingsEy.encode())
		result=definitionsModified(b"", EnigmaSettingsEy.encode())
		print_notice("definitions "+str(result[0].err_str))
		if Class:#trick compileEGMf into using fixed make
			gcliDir=os.path.join(os.getcwd(),cliDir)
			if gcliDir not in os.environ["PATH"]:
				path=gcliDir+":"+os.environ["PATH"]
				os.environ["PATH"]=path
				if os.getenv("PATH")!=path:
					print_error("can't set PATH "+path)
		cError = compileEGMf(es, exePath.encode(), emode)
		if cError>0:
			print_error("compileEGMf error "+str(cError))
		else:
			print_notice("compileEGMf done "+str(cError))

	def compileRunEnigma(self, exePath, emode):
		es=self.WriteES()
		GameFile.compileRunES(es, exePath, emode, self.EnigmaSettingsEy())

	def EnigmaSettingsEy(self):
		ey="%e-yaml\n---\n"
		if self.EnigmaSettingsEef:
			ey+="Data: "+self.EnigmaSettingsEef+"\n"
			print_notice("Enigma Settings.eef "+self.EnigmaSettingsEef)
		ey+="treat-literals-as: 0\nsample-lots-of-radios: 0\ninherit-equivalence-from: 0\n"
		ey+="sample-checkbox: on\nsample-edit: DEADBEEF\nsample-combobox: 0\ninherit-strings-from: 0\n"
		ey+="inherit-escapes-from: 0\ninherit-increment-from: 0\n \n"
		ey+="target-audio: "+self.EnigmaTargetAudio+"\n"
		ey+="target-windowing: "+self.EnigmaTargetWindowing+"\n"
		ey+="target-compiler: "+self.EnigmaTargetCompiler+"\n"
		ey+="target-graphics: "+self.EnigmaTargetGraphics+"\n"
		ey+="target-widget: "+self.EnigmaTargetWidget+"\n"
		ey+="target-collision: "+self.EnigmaTargetCollision+"\n"
		ey+="target-networking: "+self.EnigmaTargetNetworking+"\n"
		ey+="extensions:Universal_System/Extensions/Alarms,Universal_System/Extensions/Timelines,Universal_System/Extensions/Paths,Universal_System/Extensions/MotionPlanning,Universal_System/Extensions/DateTime,Universal_System/Extensions/ParticleSystems,Universal_System/Extensions/DataStructures"
		return ey

	def WriteES(self):
		print_notice("writing ES")
		self.es=EnigmaStruct()
		self.es.fileVersion = -1#i.format.getVersion();
		self.es.filename = None#i.uri
		self.populateESSettings()
		self.populateESSprites()
		self.populateESSounds()
		self.populateESBackgrounds()
		self.populateESPaths()
		self.populateESScripts()
		self.populateESShaders()
		self.populateESFonts()
		self.populateESTimelines()
		self.populateESObjects()
		self.populateESRooms()
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
		print_notice("done ES")
		return self.es

	def populateESSettings(self):
		if len(self.configs) == 0:
			print_error("no settings")
		self.configs[0].WriteESGameSettings(self.es)
		self.es.gameSettings.gameId = self.gameId

	def populateESSprites(self):
		self.es.spriteCount=len(self.sprites)
		if self.es.spriteCount>0:
			ot=(ESSprite*self.es.spriteCount)()
			for count in range(self.es.spriteCount):
				tobj=self.sprites[count]
				eobj=tobj.WriteESSprite()
				ot[count]=eobj
			self.es.sprites=cast(ot,POINTER(ESSprite))

	def populateESSounds(self):
		self.es.soundCount=len(self.sounds)
		if self.es.spriteCount>0:
			ot=(ESSound*self.es.soundCount)()
			for count in range(self.es.soundCount):
				tobj=self.sounds[count]
				eobj=tobj.WriteESSound()
				ot[count]=eobj
			self.es.sounds=cast(ot,POINTER(ESSound))

	def populateESBackgrounds(self):
		self.es.backgroundCount=len(self.backgrounds)
		if self.es.backgroundCount>0:
			ot=(ESBackground*self.es.backgroundCount)()
			for count in range(self.es.backgroundCount):
				tobj=self.backgrounds[count]
				eobj=tobj.WriteESBackground()
				ot[count]=eobj
			self.es.backgrounds=cast(ot,POINTER(ESBackground))

	def populateESPaths(self):
		self.es.pathCount=len(self.paths)
		if self.es.pathCount>0:
			ot=(ESPath*self.es.pathCount)()
			for count in range(self.es.pathCount):
				tobj=self.paths[count]
				eobj=tobj.WriteESPath()
				ot[count]=eobj
			self.es.paths=cast(ot,POINTER(ESPath))

	def populateESScripts(self):
		self.es.scriptCount=len(self.scripts)
		if self.es.scriptCount>0:
			ot=(ESScript*self.es.scriptCount)()
			for count in range(self.es.scriptCount):
				tobj=self.scripts[count]
				eobj=tobj.WriteESScript()
				ot[count]=eobj
			self.es.scripts=cast(ot,POINTER(ESScript))

	def populateESShaders(self):
		self.es.shaderCount=len(self.shaders)
		if self.es.shaderCount>0:
			ot=(ESShader*self.es.shaderCount)()
			for count in range(self.es.shaderCount):
				tobj=self.shaders[count]
				eobj=tobj.WriteESShader()
				ot[count]=eobj
			self.es.shaders=cast(ot,POINTER(ESShader))

	def populateESFonts(self):
		if not self.app:
			print_error("initialize Qt")
		oF = ESFont()
		oF.name = "EnigmaDefault".encode()
		oF.id = -1
		oF.fontName = "Arial".encode()
		oF.size = 12
		oF.bold = False
		oF.italic = False
		oF.rangeMin = 32
		oF.rangeMax = 127
		og = self.populateESGlyphs(oF,oF.rangeMin,oF.rangeMax,0);
		oF.glyphs = cast(og,POINTER(ESGlyph))
		self.es.fontCount=len(self.fonts)+1
		ot=(ESFont*self.es.fontCount)()
		ot[0]=oF
		if self.es.fontCount>1:
			for count in range(1,self.es.fontCount):
				ifont=self.fonts[count-1]
				oF = ESFont()
				oF.name = ifont.getMember("name").encode()
				oF.id = ifont.getMember("id")
				oF.fontName = ifont.getMember("fontName").encode()
				oF.size = ifont.getMember("size")
				oF.bold = ifont.getMember("bold")
				oF.italic = ifont.getMember("italic")
				oF.rangeMin = ifont.getMember("characterRangeBegin")
				oF.rangeMax = ifont.getMember("characterRangeEnd")
				og = self.populateESGlyphs(oF,oF.rangeMin,oF.rangeMax,0);
				oF.glyphs = cast(og,POINTER(ESGlyph))
				ot[count]=oF
		self.es.fonts=cast(ot,POINTER(ESFont))

	def populateESGlyphs(self, fnt, rangeMin, rangeMax, aa):
		glyphs = (ESGlyph*(rangeMax - rangeMin + 1))()
		for c in range(rangeMin,rangeMax):
			self.populateESGlyph(glyphs[c - rangeMin],fnt,chr(c),aa)
		return glyphs

	def populateESGlyph(self, og, fnt, c, aa):
		font = QtGui.QFont(str(fnt.fontName.decode()),fnt.size)
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
		raster = b""
		for y in range(r.height()):
			for x in range(r.width()):
				raster+=bytes([i.pixel(x,y)&0xff])
		og.width = r.width()
		og.height = r.height()
		og.data = raster

	def populateESTimelines(self):
		self.es.timelineCount=len(self.timelines)
		if self.es.scriptCount>0:
			ot=(ESTimeline*self.es.timelineCount)()
			for count in range(self.es.timelineCount):
				tobj=self.timelines[count]
				eobj=tobj.WriteESTimeline()
				ot[count]=eobj
			self.es.timelines=cast(ot,POINTER(ESTimeline))

	def populateESObjects(self):
		self.es.gmObjectCount=len(self.objects)
		if self.es.gmObjectCount>0:
			ot=(ESObject*self.es.gmObjectCount)()
			for count in range(self.es.gmObjectCount):
				tobj=self.objects[count]
				eobj=tobj.WriteESObject()
				ot[count]=eobj
			self.es.gmObjects=cast(ot,POINTER(ESObject))

	def populateESRooms(self):
		self.es.roomCount=len(self.rooms)
		if self.es.roomCount>0:
			ot=(ESRoom*self.es.roomCount)()
			for count in range(self.es.roomCount):
				tobj=self.rooms[count]
				eobj=tobj.WriteESRoom()
				ot[count]=eobj
			self.es.rooms=cast(ot,POINTER(ESRoom))

def IfEnigmaDir():
	if os.name=="nt":
		if os.path.exists("compileEGMf.dll"):
			return True
	else:
		if os.path.exists("libcompileEGMf.so"):
			return True
	return False

def LoadPluginLib():
	if os.name=="nt":
		ss=cdll.LoadLibrary(os.path.split(os.getcwd())[0]+"\\mingw32\\bin\\libgcc_s_sjlj-1.dll")
		ss2=cdll.LoadLibrary(os.path.split(os.getcwd())[0]+"\\mingw32\\bin\\libstdc++-6.dll")
		egmf=cdll.LoadLibrary("compileEGMf.dll")
	else:
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
	ecb.ide_execute = CFUNCTYPE(c_int, c_char_p, POINTER(c_char_p), c_intbool)(ede_ide_execute)
	ecb.ide_compress_data = CFUNCTYPE(c_int, c_char_p, c_int)(ede_ide_compress_data)
	libInit(ecb)



