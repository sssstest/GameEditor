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

RtUnknown=9

def gmkKindName(kind):
	groupKind = [
			"Unknown",
			"Objects",
			"Sprites",
			"Sounds",
			"Rooms",
			"RtUnknown5",
			"Backgrounds",
			"Scripts",
			"Paths",
			"Fonts",
			"GameInformation",
			"GameOptions",
			"Timelines",
			"Extensions",
			"Shaders"]
	if kind in [5]:
		print_error("unsupported group "+str(kind))
	return groupKind[kind]

def nameGmkKind(group):
	if group=="Unknown":
		return 0
	elif group=="Sprites":
		return 2
	elif group=="Sounds":
		return 3
	elif group=="Backgrounds":
		return 6
	elif group=="Paths":
		return 8
	elif group=="Scripts":
		return 7
	elif group=="Shaders":
		return 14
	elif group=="Fonts":
		return 9
	elif group=="Timelines":
		return 12
	elif group=="Objects":
		return 1
	elif group=="Rooms":
		return 4
	elif group=="Included Files":
		return 9
	#elif group=="Constants":
	#	return "GameConstant"
	elif group=="Help" or group=="GameInformation":
		return 10
	elif group=="Settings" or group=="GameOptions":
		return 11
	elif group=="Extensions":
		return 13
	else:
		print_notice("unsupported group "+group)
		return 0

def groupKind(group):
	if group=="Unknown":
		return None
	elif group=="Sprites":
		return GameSprite
	elif group=="Sounds":
		return GameSound
	elif group=="Backgrounds":
		return GameBackground
	elif group=="Paths":
		return GamePath
	elif group=="Scripts":
		return GameScript
	elif group=="Shaders":
		return GameShader
	elif group=="Fonts":
		return GameFont
	elif group=="Timelines":
		return GameTimeline
	elif group=="Objects":
		return GameObject
	elif group=="Rooms":
		return GameRoom
	#elif group=="Included Files":
	#	return "GameIncludedFile"
	#elif group=="Constants":
	#	return "GameConstant"
	elif group=="Help" or group=="GameInformation":
		return None
	#	return "GameInformation"
	elif group=="Settings" or group=="GameOptions":
		return None
	#	return "GameSettings"
	elif group=="Extensions":
		return None
	#	return "GameExtension"
	else:
		print_error("unsupported group "+str(group))
		return None

class GameTreeNode(object):
	def __init__(self, _status, _group, _index, _name):
		self.index=_index
		self.name=_name
		self.status=_status
		self.group=_group
		self.resource=None
		self.contents=[]
		if type(_group)!=str:
			print(_group)
			raise 5

	def Finalize(self, parent):
		if not self.resource:
			if groupKind(self.group):
				self.resource = parent.gameFile.GetResource(groupKind(self.group), self.index)
		for i in range(len(self.contents)):
			self.contents[i].Finalize(parent)

	def AddResource(self, resource):
		self.index = resource.GetId()
		node = GameTreeNode(StatusSecondary, self.group, self.index, self.resource.name)
		node.resource = self.resource
		self.contents.append(node)

	def AddFilter(self, value):
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
		GroupPaths = 8
		GroupDataFiles = 9
		GroupFonts = GroupDataFiles
		GroupGameInformation = 10
		GroupGameOptions = 11
		GroupGlobalGameOptions = GroupGameOptions
		GroupTimelines = 12
		GroupExtensionPackages = 13
		GroupShaders=14
		GroupCount = 15

	def __init__(self, gameFile):
		GameResource.__init__(self, gameFile, -1)
		self.contents=[]

	def NewTree(self):
		self.AddGroupName("Sprites")
		self.AddGroupName("Sounds")
		self.AddGroupName("Backgrounds")
		self.AddGroupName("Paths")
		self.AddGroupName("Scripts")
		self.AddGroupName("Shaders")
		self.AddGroupName("Fonts")
		self.AddGroupName("Timelines")
		self.AddGroupName("Objects")
		self.AddGroupName("Rooms")
		self.AddGroupName("Included Files")
		self.AddGroupName("Constants")
		self.AddGroupName("Help")
		self.AddGroupName("Settings")
		self.AddGroupName("Extensions")
		#self.AddGroupName("Game Information")
		#self.AddGroupName("Global Game Settings")

	def ReadGmk(self, stream):
		if self.gameFile.gmkVersion>=700:
			count=12
		else:#<500 and 540>
			count=11
		for i in range(count):
			status = stream.ReadDword()
			group = gmkKindName(stream.ReadDword())
			stream.ReadDword()
			name = stream.ReadString()
			node = GameTreeNode(status, group, -1, name)
			self.ReadRecursiveTree(stream, node, stream.ReadDword())
			self.contents.append(node)

	def ReadRecursiveTree(self, stream, parent, count):
		for c in range(count):
			status = stream.ReadDword()
			group = gmkKindName(stream.ReadDword())
			index = stream.ReadDword()
			name = stream.ReadString()
			node = GameTreeNode(status, group, index, name)
			self.ReadRecursiveTree(stream, node, stream.ReadDword())
			parent.contents.append(node)

	def WriteGmk(self, stream):
		for i in range(12):
			stream.WriteDword(self.contents[i].status)
			stream.WriteDword(nameGmkKind(self.contents[i].group))
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
			stream.WriteDword(nameGmkKind(parent.contents[i].group))
			if parent.contents[i].status == GameTree.StatusGroup or parent.contents[i].status == GameTree.StatusPrimary:#clifix StatusPrimary
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
		if name=="sprites":
			group="Sprites"
		elif name=="sounds" or name=="sound":
			group="Sounds"
		elif name=="backgrounds" or name=="background":
			group="Backgrounds"
		elif name=="paths":
			group="Paths"
		elif name=="scripts":
			group="Scripts"
		elif name=="shaders":
			group="Shaders"
		elif name=="fonts":
			group="Fonts"
		elif name=="timelines":
			group="Timelines"
		elif name=="objects":
			group="Objects"
		elif name=="rooms":
			group="Rooms"
		elif name=="included files":
			group="DataFiles"
		elif name=="constants":
			group="Constants"
		elif name=="game information" or name=="help":
			group="GameInformation"
			status=GameTree.StatusSecondary
		elif name=="global game settings" or name=="settings":
			group="GameOptions"
			status=GameTree.StatusSecondary
		elif name=="extensions":
			group="Extensions"
			status=GameTree.StatusSecondary
		else:
			print_error("unsupported group name "+name)
		return group,status

	def AddGroupName(self, name):
		group,status = self.PrimaryGroupName(name)
		node = GameTreeNode(status, group, -1, name)
		self.contents.append(node)
		return node

	def PrintRecursive(self):
		self.PrintRecursiveNode(self, "-")

	def PrintRecursiveNode(self, r, start):
		for x in r.contents:
			if x.resource:
				print_notice(start+x.name+" "+str(x.resource.getMember("id"))+" "+str(x.resource.getMember("name")))
			else:
				print_notice(start+x.name+" status "+str(x.status))
			self.PrintRecursiveNode(x,start+"-")

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
		group=None
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
