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

from CliEnigmaStruct import *
from CliBinaryStream import *
from CliEefReader import *
from CliApng import *
#from PyQt4 import QtGui, QtCore#font
import xml.etree.ElementTree

Class=1

def boolToGmxBool(b):
	if b:
		return "True"
	else:
		return "False"

def boolToGmxIntbool(b):
	if b:
		return -1
	else:
		return 0

def gmxBoolToBool(text):
	return text.lower()=="true"

def gmxFloat(string):
	return float(string.replace(",","."))

def emptyTextToString(chil):
	if not chil:
		return ""
	return chil

def tabStringLines(stri,tab="\t"):
	stri="\n".join([tab+y for y in stri.strip().split("\n")])+"\n"
	return stri

def ARGBtoRGBA(color):
	return ((color&0xff0000)<<8) | ((color&0xff00)<<8) | ((color&0xff)<<8) | ((color&0xff000000)>>24)

def gmxCreateTag(root, name, text):
	tag=xml.etree.ElementTree.Element(name)
	tag.tail="\n"
	tag.text=text
	root.append(tag)

class GameResource(object):
	def __init__(self, gameFile, id=-1):
		self.gameFile=gameFile
		self.exists=True
		self.members={}
		self.listeners=[]
		if id!=-1:
			self.members["id"]=id

	def name(self):
		return self.getMember("name")

	def rename(self, name):
		self.setMember("name",name)

	def id(self):
		return self.getMember("id")

	def ifDefault(self, member):
		if not member in self.defaults:
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

	def getMember(self, member, default=None):
		if member in self.members:
			return self.members[member]
		elif member in self.defaults:
			return self.defaults[member]
		elif default:
			return default
		else:
			print_error("unsupported member "+member)

	def setMember(self, member, val):
		if not member in self.defaults:
			print_warning("setting member not in defaults "+member)
		if type(self.defaults[member])!=type(val) and type(self.defaults[member])!=type(None):
			if type(self.defaults[member])!=str and sys.version_info[0]<3 and type(val)!=unicode:
				if type(self.defaults[member])!=int and type(val)!=long:
					print_error("changed type of "+member+" "+str(type(self.defaults[member]))+" "+str(type(val)))
		if member=="name" and self.gameFile.resourceTree:
			node,tree=self.gameFile.resourceTree.FindNodeName(self.members.get(member,"noname"))
			if node:
				node.name=val
		#if member not in self.members or self.members[member]!=val:
		#	for callBack in self.listeners:
		#		callBack("property",member,self.members[member],val)
		oldValue=self.members.get(member,None)
		self.members[member]=val
		if member not in self.members or oldValue!=val:
			for callBack in self.listeners:
				callBack("property",member,oldValue,val)

	def addListener(self, callBack):
		self.listeners.append(callBack)

	def deleteListener(self, callBack):
		self.listeners.remove(callBack)
