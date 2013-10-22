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

#* getActionsCode converted to python from https://github.com/enigma-dev/enigma-dev/blob/master/pluginsource/org/enigma/EnigmaWriter.java

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
import tempfile
from PyQt4 import QtGui, QtCore#font
from CliApng import *
from CliEefReader import *
from CliPrintColors import *
from CliBinaryStream import *
from CliEnigmaStruct import *
from CliLexer import *
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

#redirectStdout()
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

def emptyTextToString(chil):
	if not chil:
		return ""
	return chil

def ifCleanArgumentValue(chil):
	for child in "(),\n":
		if child in chil:
			return False
	return True




def gmxFloat(string):
	return float(string.replace(",","."))

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
		self.iconImage = BinaryStream(io.BytesIO(icon))
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
		og.author = self.getMember("author").encode()
		og.version = self.getMember("version").encode()
		og.information = self.getMember("version_information").encode()
		#og.includeFolder = GmFile.GS_INCFOLDER_CODE.get(ig.get(PGameSettings.INCLUDE_FOLDER));
		#og.overwriteExisting = ig.get(PGameSettings.OVERWRITE_EXISTING);
		#og.removeAtGameEnd = ig.get(PGameSettings.REMOVE_AT_GAME_END);
		og.versionMajor = self.getMember("version_major")
		og.versionMinor = self.getMember("version_minor")
		og.versionRelease = self.getMember("version_release")
		og.versionBuild = self.getMember("version_build")
		og.company = self.getMember("version_company").encode()
		og.product = self.getMember("version_product").encode()
		og.copyright = self.getMember("version_copyright").encode()
		og.description = self.getMember("version_description").encode()
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
		og.gameIcon = "../../CompilerSource/stupidity-buffer/enigma.ico"

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

	def WriteGGG(self):
		stri="@gameinformation {\n"
		for key in self.members:
			if not self.ifDefault(key):
				if key != "information":
					stri+="\t"+key+"="+str(self.getMember(key))+"\n"
		stri+="\t@information {\n"+str(self.getMember("information"))+"}\n"
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
			GameObject,
			GameSprite,
			GameSound,
			GameRoom,
			GameFile.RtUnknown,
			GameBackground,
			GameScript,
			GamePath,
			GameFont,
			GameFile.RtUnknown,
			GameFile.RtUnknown,
			GameTimeline,
			GameFile.RtUnknown,
			GameShader]
		self.resource = parent.gameFile.GetResource(groupKind[self.group], self.index)
		for i in range(len(self.contents)):
			self.contents[i].Finalize(parent)

	def AddResource(self,resource):
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
		for i in range(12):
			status = stream.ReadDword()
			group = stream.ReadDword()
			stream.ReadDword()
			name = stream.ReadString()
			node = GameTreeNode(status, group, -1, name)
			self.ReadRecursiveTree(stream, node, stream.ReadDword())
			self.contents.append(node)

	def ReadRecursiveTree(self, stream, parent, count):
		for c in range(count):
			status = stream.ReadDword()
			group = stream.ReadDword()
			index = stream.ReadDword()
			name = stream.ReadString()
			node = GameTreeNode(status, group, index, name)
			self.ReadRecursiveTree(stream, node, stream.ReadDword())
			parent.contents.append(node)

	def WriteGmk(self, stream):
		for i in range(12):
			stream.WriteDword(self.contents[i].status)
			stream.WriteDword(self.contents[i].group)
			stream.WriteDword(0)
			stream.WriteString(self.contents[i].name)
			stream.WriteDword(len(self.contents[i].contents))
			self.WriteRecursiveTree(stream, self.contents[i], len(self.contents[i].contents))

	def WriteRecursiveTree(self, stream, parent, count):
		for i in range(count):
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
		for i in range(len(self.contents)):
			self.contents[i].Finalize(self)
		names=[]
		for node in self.contents:
			names.append(node.name)
		if "Shaders" not in names:
			for count in range(len(self.contents)):
				if self.contents[count].name=="Scripts":
					group,status = self.PrimaryGroupName("Shaders")
					node = GameTreeNode(status, group, -1, "Shaders")
					self.contents.insert(count+1,node)

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

	def FindNodeName(self, name):
		return self.FindRecursiveNodeName(name, self)

	def FindRecursiveNodeName(self, name, r):
		for x in r.contents:
			if x.name==name:
				return x,r
			node,tree=self.FindRecursiveNodeName(name, x)
			if node:
				return node,tree
		return None,None

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
		RtUnknown=9
		RtCount=10

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
		self.EnigmaSettingsEef=None
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
		self.settings = GameSettings(self)
		return self.settings

	def newGameInformation(self):
		self.gameInformation = GameInformation(self)
		return self.gameInformation

	def compileRunEnigma(self, exePath, emode):
		es=self.WriteES()
		GameFile.compileRunES(es, exePath, emode, self.EnigmaSettingsEy())

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

	def ReadEgm(self, f):
		z=zipfile.ZipFile(f,'r')
		f=z.open("Enigma Settings.eef",'rU')
		global tempeef
		tempeef=tempfile.NamedTemporaryFile()
		tempeef=open(tempeef.name+".eef","wb")
		tempeef.write(f.read())
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
			f=z.open("toc.txt",'rU')
		else:
			f=z.open(dir+"/toc.txt",'rU')
		toc=[]
		for t in f.readlines():
			entry = t.decode().strip()
			if len(entry) > 4 and entry[3] == ' ' and entry[:3].isupper():
				#oldKind=kind
				kind,entry = entry[0:3],entry[4:]
				#if oldKind!=kind:
				#	print_warning("kind changed "+kind+" "+oldKind)
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
			print_error("unsupported toc.txt kind "+kind+" "+entry)

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
		for i in range(self.GMK_GUID_LENGTH):
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
		for c in range(count):
			trigger = GmkTrigger(self,c)
			trigger.ReadGmk(stream)
			self.triggers.append(trigger)
		#Last time Triggers were changed'
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
			sound = GameSound(self,c)
			sound.ReadGmk(stream)
			if sound.exists:
				self.sounds.append(sound)
		# Load sprites
		#GM version needed for Resource
		stream.ReadDword()
		count = stream.ReadDword()
		for c in range(count):
			sprite = GameSprite(self,c)
			sprite.ReadGmk(stream)
			if sprite.exists:
				self.sprites.append(sprite)
		# Load backgrounds
		#GM version needed for Resource
		stream.ReadDword()
		count = stream.ReadDword()
		for c in range(count):
			background = GameBackground(self,c)
			background.ReadGmk(stream)
			if background.exists:
				self.backgrounds.append(background)
		# Load paths
		#GM version needed for Resource
		stream.ReadDword()
		count = stream.ReadDword()
		for c in range(count):
			path = GamePath(self,c)
			path.ReadGmk(stream)
			self.paths.append(path)
		# Load scripts
		#GM version needed for Resource
		stream.ReadDword()
		count = stream.ReadDword()
		for c in range(count):
			script = GameScript(self,c)
			script.ReadGmk(stream)
			self.scripts.append(script)
		# Load fonts
		#GM version needed for Resource
		stream.ReadDword()
		count = stream.ReadDword()
		for c in range(count):
			font = GameFont(self,c)
			font.ReadGmk(stream)
			self.fonts.append(font)
		# Load timelines
		#GM version needed for Resource
		stream.ReadDword()
		count = stream.ReadDword()
		for c in range(count):
			timeline = GameTimeline(self,c)
			timeline.ReadGmk(stream)
			if timeline.exists:
				print_error("timeline unsupported")
				self.timelines.append(timeline)
		# Load objects
		#GM version needed for Resource
		stream.ReadDword()
		count = stream.ReadDword()
		for c in range(count):
			gmObject = GameObject(self,c)
			gmObject.ReadGmk(stream)
			if gmObject.exists:
				self.objects.append(gmObject)
		# Load rooms
		#GM version needed for Resource
		stream.ReadDword()
		count = stream.ReadDword()
		for c in range(count):
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
		for c in range(count):
			includeFile = GameIncludeFile(self,c)
			includeFile.ReadGmk(stream)
			self.includeFiles.append(includeFile)
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

	def ReadGGGStream(self, stream):
		GGGLexer(stream)

	def ReadReadGGGFile(self, filename):
		data = open(filename, "rb")
		stream = BinaryStream(data)
		self.ReadGGGStream(stream)

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
		elif ext==".ggg":
			self.ReadGGGFile(filename)
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
		for i in range(self.GMK_GUID_LENGTH):
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
			wfile.write(ggg.encode())
		else:
			print_error("unsupported save format")

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

	def GetResourceHighestId(self, type):
		highest=-1
		if type==GameSprite:
			for s in self.sprites:
				id = s.getMember("id")
				if id>highest:
					highest=id
		elif type==GameSound:
			for s in self.sounds:
				id = s.getMember("id")
				if id>highest:
					highest=id
		elif type==GameBackground:
			for s in self.backgrounds:
				id = s.getMember("id")
				if id>highest:
					highest=id
		elif type==GamePath:
			for s in self.paths:
				id = s.getMember("id")
				if id>highest:
					highest=id
		elif type==GameScript:
			for s in self.scripts:
				id = s.getMember("id")
				if id>highest:
					highest=id
		elif type==GameShader:
			for s in self.shaders:
				id = s.getMember("id")
				if id>highest:
					highest=id
		elif type==GameFont:
			for s in self.fonts:
				id = s.getMember("id")
				if id>highest:
					highest=id
		elif type==GameTimeline:
			for s in self.timelines:
				id = s.getMember("id")
				if id>highest:
					highest=id
		elif type==GameObject:
			for s in self.objects:
				id = s.getMember("id")
				if id>highest:
					highest=id
		elif type==GameRoom:
			for s in self.rooms:
				id = s.getMember("id")
				if id>highest:
					highest=id
		return highest

	def GetResource(self, type, index):
		if type==str:
			type=eval(str)
		if type==GameSprite:
			for s in self.sprites:
				if s.getMember("id")==index:
					return s
		elif type==GameSound:
			for s in self.sounds:
				if s.getMember("id")==index: return s
		elif type==GameBackground:
			for s in self.backgrounds:
				if s.getMember("id")==index: return s
		elif type==GamePath:
			for s in self.paths:
				if s.getMember("id")==index: return s
		elif type==GameScript:
			for s in self.scripts:
				if s.getMember("id")==index: return s
		elif type==GameShader:
			for s in self.shaders:
				if s.getMember("id")==index: return s
		elif type==GameFont:
			for s in self.fonts:
				if s.getMember("id")==index: return s
		elif type==GameTimeline:
			for s in self.timelines:
				if s.getMember("id")==index: return s
		elif type==GameObject:
			for s in self.objects:
				if s.getMember("id")==index: return s
		elif type==GameRoom:
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
			for count in range(self.es.spriteCount):
				tobj=self.sprites[count]
				eobj=tobj.WriteESSprite()
				ot[count]=eobj
			self.es.sprites=cast(ot,POINTER(ESSprite))

	def populateSounds(self):
		self.es.soundCount=len(self.sounds)
		if self.es.spriteCount>0:
			ot=(ESSound*self.es.soundCount)()
			for count in range(self.es.soundCount):
				tobj=self.sounds[count]
				eobj=tobj.WriteESSound()
				ot[count]=eobj
			self.es.sounds=cast(ot,POINTER(ESSound))

	def populateBackgrounds(self):
		self.es.backgroundCount=len(self.backgrounds)
		if self.es.backgroundCount>0:
			ot=(ESBackground*self.es.backgroundCount)()
			for count in range(self.es.backgroundCount):
				tobj=self.backgrounds[count]
				eobj=tobj.WriteESBackground()
				ot[count]=eobj
			self.es.backgrounds=cast(ot,POINTER(ESBackground))

	def populatePaths(self):
		self.es.pathCount=len(self.paths)
		if self.es.pathCount>0:
			ot=(ESPath*self.es.pathCount)()
			for count in range(self.es.pathCount):
				tobj=self.paths[count]
				eobj=tobj.WriteESPath()
				ot[count]=eobj
			self.es.paths=cast(ot,POINTER(ESPath))

	def populateScripts(self):
		self.es.scriptCount=len(self.scripts)
		if self.es.scriptCount>0:
			ot=(ESScript*self.es.scriptCount)()
			for count in range(self.es.scriptCount):
				tobj=self.scripts[count]
				eobj=tobj.WriteESScript()
				ot[count]=eobj
			self.es.scripts=cast(ot,POINTER(ESScript))

	def populateShaders(self):
		self.es.shaderCount=len(self.shaders)
		if self.es.shaderCount>0:
			ot=(ESShader*self.es.shaderCount)()
			for count in range(self.es.shaderCount):
				tobj=self.shaders[count]
				eobj=tobj.WriteESShader()
				ot[count]=eobj
			self.es.shaders=cast(ot,POINTER(ESShader))

	def populateFonts(self):
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
		og = self.populateGlyphs(oF,oF.rangeMin,oF.rangeMax,0);
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
				og = self.populateGlyphs(oF,oF.rangeMin,oF.rangeMax,0);
				oF.glyphs = cast(og,POINTER(ESGlyph))
				ot[count]=oF
		self.es.fonts=cast(ot,POINTER(ESFont))

	def populateGlyphs(self, fnt, rangeMin, rangeMax, aa):
		glyphs = (ESGlyph*(rangeMax - rangeMin + 1))()
		for c in range(rangeMin,rangeMax):
			self.populateGlyph(glyphs[c - rangeMin],fnt,chr(c),aa)
		return glyphs

	def populateGlyph(self, og, fnt, c, aa):
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

	def populateTimelines(self):
		self.es.timelineCount=len(self.timelines)
		if self.es.scriptCount>0:
			ot=(ESTimeline*self.es.timelineCount)()
			for count in range(self.es.timelineCount):
				tobj=self.timelines[count]
				eobj=tobj.WriteESTimeline()
				ot[count]=eobj
			self.es.timelines=cast(ot,POINTER(ESTimeline))

	def populateObjects(self):
		self.es.gmObjectCount=len(self.objects)
		if self.es.gmObjectCount>0:
			ot=(ESObject*self.es.gmObjectCount)()
			for count in range(self.es.gmObjectCount):
				tobj=self.objects[count]
				eobj=tobj.WriteESObject()
				ot[count]=eobj
			self.es.gmObjects=cast(ot,POINTER(ESObject))

	def populateRooms(self):
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



