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
			RtUnknown,
			GameObject,
			GameSprite,
			GameSound,
			GameRoom,
			RtUnknown,
			GameBackground,
			GameScript,
			GamePath,
			GameFont,
			RtUnknown,
			RtUnknown,
			GameTimeline,
			RtUnknown,
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
		self.AddGroupName("Game Information")
		self.AddGroupName("Global Game Settings")
		self.AddGroupName("Extensions")

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
		elif name=="sounds" or name=="sound":
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

	def PrintRecursive(self):
		self.PrintRecursiveNode(self, "-")

	def PrintRecursiveNode(self, r, start):
		for x in r.contents:
			print_notice(start+x.name)
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
