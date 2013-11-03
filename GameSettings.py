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
	"errorFlags":0, "OVERWRITE_EXISTING":False, "REMOVE_AT_GAME_END":False}

	def __init__(self, gameFile):
		GameResource.__init__(self, gameFile, -1)

	def ReadEgm(self, gmkfile, entry, z):
		stream=z.open(entry+".ey",'r')
		y=YamlParser()
		r=y.parseStream(stream)
		#gmkfile.guid=r.getMint('DPLAY_GUID')
		gmkfile.gameId=r.getMint('GAME_ID')
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
		self.setMember("closesecondary",r.getMbool('TREAT_CLOSE_AS_ESCAPE'))#clifix
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
		self.setMember("OVERWRITE_EXISTING",r.getMbool('OVERWRITE_EXISTING'))
		self.setMember("REMOVE_AT_GAME_END",r.getMbool('REMOVE_AT_GAME_END'))
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
		if root[0].tag=="Options":
			root=root[0]
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
				elif child.tag.startswith(option+"ouya_"):pass
				elif child.tag.startswith(option+"textureGroup"):pass
				else:
					print_error("unsupported tag "+child.tag)

	def SaveEgm(self, gmkfile, z):
		ey = "Icon: icon.ico\n"
		ey += "Splash: null\n"
		ey += "Filler: null\n"
		ey += "Progress: null\n"
		guid=''.join(map(lambda x:hex(x+0x100)[3:],gmkfile.guid))
		ey += "DPLAY_GUID: 0x"+guid+"\n"
		ey += "GAME_ID: "+str(gmkfile.gameId)+"\n"
		ey += "START_FULLSCREEN: "+boolToEgmBool(self.getMember("fullscreen"))+"\n"
		ey += "INTERPOLATE: "+boolToEgmBool(self.getMember("interpolate"))+"\n"
		ey += "DONT_DRAW_BORDER: "+boolToEgmBool(self.getMember("noborder"))+"\n"
		ey += "DISPLAY_CURSOR: "+boolToEgmBool(self.getMember("showcursor"))+"\n"
		ey += "SCALING: "+str(self.getMember("scale"))+"\n"
		ey += "ALLOW_WINDOW_RESIZE: "+boolToEgmBool(self.getMember("sizeable"))+"\n"
		ey += "ALWAYS_ON_TOP: "+boolToEgmBool(self.getMember("stayontop"))+"\n"
		ey += "COLOR_OUTSIDE_ROOM: "+hex(self.getMember("windowcolor"))+"\n"
		ey += "SET_RESOLUTION: "+boolToEgmBool(self.getMember("changeresolution"))+"\n"
		ey += "COLOR_DEPTH: "+intEgmChange(self.getMember("colordepth"))+"\n"#NO_CHANGE
		ey += "RESOLUTION: "+intEgmResolution(self.getMember("colordepth"))+"\n"#RES_640X480
		ey += "FREQUENCY: "+intEgmChange(self.getMember("colordepth"))+"\n"#NO_CHANGE
		ey += "DONT_SHOW_BUTTONS: "+boolToEgmBool(self.getMember("nobuttons"))+"\n"
		ey += "USE_SYNCHRONIZATION: "+boolToEgmBool(self.getMember("vsync"))+"\n"
		ey += "DISABLE_SCREENSAVERS: "+boolToEgmBool(self.getMember("noscreensaver"))+"\n"
		ey += "LET_F4_SWITCH_FULLSCREEN: "+boolToEgmBool(self.getMember("fullscreenkey"))+"\n"
		ey += "LET_F1_SHOW_GAME_INFO: "+boolToEgmBool(self.getMember("helpkey"))+"\n"
		ey += "LET_ESC_END_GAME: "+boolToEgmBool(self.getMember("quitkey"))+"\n"
		ey += "LET_F5_SAVE_F6_LOAD: "+boolToEgmBool(self.getMember("savekey"))+"\n"
		ey += "LET_F9_SCREENSHOT: "+boolToEgmBool(self.getMember("screenshotkey"))+"\n"
		ey += "TREAT_CLOSE_AS_ESCAPE: "+boolToEgmBool(self.getMember("closesecondary"))+"\n"
		ey += "GAME_PRIORITY: "+intEgmPriority(self.getMember("priority"))+"\n"#NORMAL
		ey += "FREEZE_ON_LOSE_FOCUS: "+boolToEgmBool(self.getMember("freeze"))+"\n"
		ey += "LOAD_BAR_MODE: "+intEgmShowProgress(self.getMember("showprogress"))+"\n"#DEFAULT
		ey += "SHOW_CUSTOM_LOAD_IMAGE: "+boolToEgmBool(self.getMember("loadImage"))+"\n"
		ey += "IMAGE_PARTIALLY_TRANSPARENTY: "+boolToEgmBool(self.getMember("loadtransparent"))+"\n"
		ey += "LOAD_IMAGE_ALPHA: "+str(self.getMember("loadalpha"))+"\n"
		ey += "SCALE_PROGRESS_BAR: "+boolToEgmBool(self.getMember("scaleprogress"))+"\n"
		ey += "DISPLAY_ERRORS: "+boolToEgmBool(self.getMember("displayerrors"))+"\n"
		ey += "WRITE_TO_LOG: "+boolToEgmBool(self.getMember("writeerrors"))+"\n"
		ey += "ABORT_ON_ERROR: "+boolToEgmBool(self.getMember("aborterrors"))+"\n"
		ey += "TREAT_UNINIT_AS_0: "+boolToEgmBool(self.getMember("treatUninitializedVariablesAsZero"))+"\n"
		ey += "ERROR_ON_ARGS: "+boolToEgmBool(self.getMember("argumenterrors"))+"\n"
		ey += "AUTHOR: "+self.getMember("author")+"\n"
		ey += "VERSION: "+str(self.getMember("version"))+"\n"
		ey += "LAST_CHANGED: "+str(41000)+"\n"
		ey += "INFORMATION: "+self.getMember("version_information")+"\n"
		ey += "INCLUDE_FOLDER: MAIN\n"
		ey += "OVERWRITE_EXISTING: "+boolToEgmBool(self.getMember("OVERWRITE_EXISTING"))+"\n"
		ey += "REMOVE_AT_GAME_END: "+boolToEgmBool(self.getMember("REMOVE_AT_GAME_END"))+"\n"
		ey += "VERSION_MAJOR: "+str(self.getMember("version_major"))+"\n"
		ey += "VERSION_MINOR: "+str(self.getMember("version_minor"))+"\n"
		ey += "VERSION_RELEASE: "+str(self.getMember("version_release"))+"\n"
		ey += "VERSION_BUILD: "+str(self.getMember("version_build"))+"\n"
		ey += "COMPANY: "+self.getMember("version_company")+"\n"
		ey += "PRODUCT: "+self.getMember("version_product")+"\n"
		ey += "COPYRIGHT: "+self.getMember("version_copyright")+"\n"
		ey += "DESCRIPTION: "+self.getMember("version_description")+"\n"
		z.writestr("Global Game Settings.ey", ey)
		if self.getMember("iconImage"):
			z.writestr("icon.ico", self.getMember("iconImage").Read())
		else:
			z.writestr("icon.ico", "")
			print_error("no iconImage")

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
		settingsStream.Serialize(self.getMember("iconImage"), False)
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
		og.gameIcon = b"../../CompilerSource/stupidity-buffer/enigma.ico"
