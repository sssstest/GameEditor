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

import sys
import os
bhex=hex
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.Qsci import *
import CliClass
from IdeSciLexer import *

resourcePath=os.path.join(CliClass.module_path(),"ideicons")+"/"
stylePath=os.path.join(CliClass.module_path(),"styles")+"/"

class ColorQTableWidgetItem(QTableWidgetItem):
	def __init__(self, item):
		QTableWidgetItem.__init__(self, item)

class ResourceQComboBox(QComboBox):
	def __init__(self, parent, mainwindow, resourceClass, resSelected):
		QComboBox.__init__(self, parent)
		self.mainwindow=mainwindow
		if resourceClass==CliClass.GameSprite:
			resIcon=QIcon(resourcePath+"resources/sprite.png")
			self.addItem(resIcon, "none")
			for s in self.mainwindow.gmk.sprites:
				resIcon=s.getQIcon()
				if not resIcon:
					resIcon=QIcon(resourcePath+"resources/sprite.png")
				self.addItem(resIcon, s.getMember("name"))
				if resSelected==s:
					self.setCurrentIndex(self.count()-1)
		if resourceClass==CliClass.GameObject:
			resIcon=QIcon(resourcePath+"resources/object.png")
			self.addItem(resIcon, "none")
			for s in self.mainwindow.gmk.objects:
				resIcon=QIcon(resourcePath+"resources/object.png")
				sprite=s.getMember("sprite")
				if sprite:
					resIcon=sprite.getQIcon(True)
				if not resIcon:
					resIcon=QIcon(resourcePath+"resources/object.png")
				self.addItem(resIcon, s.getMember("name"))
				if resSelected==s:
					self.setCurrentIndex(self.count()-1)
		if resourceClass==CliClass.GameRoom:
			resIcon=QIcon(resourcePath+"resources/room.png")
			self.addItem(resIcon, "none")
			for s in self.mainwindow.gmk.rooms:
				resIcon=QIcon(resourcePath+"resources/room.png")
				self.addItem(resIcon, s.getMember("name"))
				if resSelected==s:
					self.setCurrentIndex(self.count()-1)


class ResourceWindow(QtGui.QMdiSubWindow):
	def __init__(self, mainwindow, res, defaultTitle=None):
		QtGui.QMdiSubWindow.__init__(self)
		self.mainwindow=mainwindow
		self.res=res
		self.setWindowTitle(res.getMember("name",defaultTitle))
		n=QLabel("Properties panel")
		self.setWidget(n)
		self.propertiesList=[]
		self.propertiesType={}

	def saveResource(self):
		CliClass.print_warning("save resource unsupported "+str(self.res))

	def closeEvent(self, closeEvent):
		self.mainwindow.propertiesTable.updatedTable=False
		self.mainwindow.propertiesTable.res=None
		self.mainwindow.propertiesTable.clearContents()
		self.mainwindow.propertiesTable.setRowCount(1)
		self.hide()
		closeEvent.accept()
		a=self.mdiArea()
		a.removeSubWindow(self)#clifix stop showing in window list
		w=a.activeSubWindow()
		if w:
			w.showMaximized()

	def updatePropertiesTable(self):
		self.mainwindow.propertiesTable.updatedTable=False
		font=QFont("Helvetica", 10)
		fontbold=QFont("Helvetica", 10, QFont.Bold)
		fontitalic=QFont("Helvetica", 10)
		fontitalic.setItalic(True)
		self.mainwindow.propertiesTable.setSortingEnabled(False)
		self.mainwindow.propertiesTable.clearContents()
		self.mainwindow.propertiesTable.setRowCount(1)
		if self.propertiesList != None:
			propertiesList=self.propertiesList
		else:
			propertiesList=self.res.members
		resLists=[]
		for m in propertiesList:
			if m == "id":
				continue
			r=self.res.getMember(m)
			types = [str,int,float,bool]
			mltypes = [str]
			if sys.version_info[0]<3:
				mltypes.append(unicode)
				types.append(unicode)
				types.append(long)
				if type(r)==long:
					r=int(r)
			resType=self.propertiesType.get(m,None)
			if not resType and (type(r) not in types) or (type(r) in mltypes and r.count("\n")>0):
				#CliClass.print_warning("not inserting property "+m+" "+str(type(r)))
				continue
			ind=self.mainwindow.propertiesTable.rowCount()-1
			self.mainwindow.propertiesTable.insertRow(ind)
			item=QTableWidgetItem(m)
			item.setFlags(Qt.ItemIsEnabled)
			if self.res.ifDefault(m):
				item.setFont(fontitalic)
			else:
				item.setFont(fontbold)
			self.mainwindow.propertiesTable.setItem(ind, 0, item)
			if resType=="color":
				item=ColorQTableWidgetItem(bhex(r))
				#item=ColorQTableWidgetItem(__builtins__.hex(r))
				colortext=item.text()
				if colortext[-1]=="L":
					colortext=colortext[:-1]
				item.setBackgroundColor(QColor(int(str(colortext),16)))
				item.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEditable|Qt.ItemIsEnabled)
				item.setFont(font)
				self.mainwindow.propertiesTable.setItem(ind, 1, item)
				continue
			elif resType=="shadertype":
				item=QComboBox(self)
				item.addItem("GLSL")
				item.addItem("GLSLES")
				item.addItem("HLSL")
				item.addItem("HLSL9")
				item.addItem("Cg")
				item.setCurrentIndex(item.findText(self.res.getMember(m)))
				def setType(e,i=item,m=m,resType=resType):
					self.res.setMember(m,str(i.currentText()))
					self.updatePropertiesTable()
				item.currentIndexChanged.connect(setType)
				self.mainwindow.propertiesTable.setCellWidget(ind, 1, item)
			elif resType=="fontAntiAliasing":
				item=QComboBox(self)
				item.addItem("0")
				item.addItem("1")
				item.addItem("2")
				item.addItem("3")
				item.addItem("4")
				fontAa=str(self.res.getMember(m))
				item.setCurrentIndex(item.findText(fontAa))
				def setType(e,i=item,m=m,resType=resType):
					self.res.setMember(m,int(str(i.currentText())))
					self.updatePropertiesTable()
				item.currentIndexChanged.connect(setType)
				self.mainwindow.propertiesTable.setCellWidget(ind, 1, item)
			elif resType=="pathConnectionKind":
				item=QComboBox(self)
				item.addItem("0 Straight")
				item.addItem("1 Smooth")
				kind=self.res.getMember(m)
				item.setCurrentIndex(kind)
				def setType(e,i=item,m=m,resType=resType):
					self.res.setMember(m,int(str(i.currentText()).split()[0]))
					self.updatePropertiesTable()
				item.currentIndexChanged.connect(setType)
				self.mainwindow.propertiesTable.setCellWidget(ind, 1, item)
			elif resType=="soundKind":
				item=QComboBox(self)
				item.addItem("0 Normal")
				item.addItem("1 Background")
				item.addItem("2 3D")
				item.addItem("3 Multimedia")
				kind=self.res.getMember(m)
				item.setCurrentIndex(kind)
				def setType(e,i=item,m=m,resType=resType):
					self.res.setMember(m,int(str(i.currentText()).split()[0]))
					self.updatePropertiesTable()
				item.currentIndexChanged.connect(setType)
				self.mainwindow.propertiesTable.setCellWidget(ind, 1, item)
			elif resType=="spriteMaskshape":
				item=QComboBox(self)
				item.addItem("0 Precise")
				item.addItem("1 Rectangle")
				item.addItem("2 Disc")
				item.addItem("3 Diamond")
				kind=self.res.getMember(m)
				item.setCurrentIndex(kind)
				def setType(e,i=item,m=m,resType=resType):
					self.res.setMember(m,int(str(i.currentText()).split()[0]))
					self.updatePropertiesTable()
				item.currentIndexChanged.connect(setType)
				self.mainwindow.propertiesTable.setCellWidget(ind, 1, item)
			elif resType=="spriteBboxmode":
				item=QComboBox(self)
				item.addItem("0 Automatic")
				item.addItem("1 Full")
				item.addItem("2 Manual")
				kind=self.res.getMember(m)
				item.setCurrentIndex(kind)
				def setType(e,i=item,m=m,resType=resType):
					self.res.setMember(m,int(str(i.currentText()).split()[0]))
					self.updatePropertiesTable()
				item.currentIndexChanged.connect(setType)
				self.mainwindow.propertiesTable.setCellWidget(ind, 1, item)
			elif resType:
				item=ResourceQComboBox(self,self.mainwindow,resType,r)
				resLists.append(item)
				def setResourceFromName(e,i=item,m=m,resType=resType):
					if i.currentText()=="none":
						self.res.setMember(m,None)
						self.res.setMember(m+"Index",-1)
						return
					else:
						self.res.setMember(m,self.mainwindow.gmk.GetResourceName(resType,i.currentText()))
					self.res.setMember(m+"Index",self.res.getMember(m).getMember("id"))
					self.updatePropertiesTable()
				item.currentIndexChanged.connect(setResourceFromName)
				self.mainwindow.propertiesTable.setCellWidget(ind, 1, item)
				continue
			if type(r)==bool:
				item=QTableWidgetItem()
				item.setFlags(Qt.ItemIsSelectable|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled)#|Qt.ItemIsTristateQt.ItemIsEditable|
				item.setCheckState(Qt.Unchecked)
				if r:
					item.setCheckState(Qt.Checked)
			else:
				item=QTableWidgetItem(str(r))
				item.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEditable|Qt.ItemIsEnabled)
			item.setFont(font)
			self.mainwindow.propertiesTable.setItem(ind, 1, item)
		self.mainwindow.propertiesTable.resizeRowsToContents()
		self.mainwindow.propertiesTable.res=self.res
		self.mainwindow.propertiesTable.subwindow=self
		self.mainwindow.propertiesTable.updatedTable=True
		self.mainwindow.propertiesTable.itemClicked.connect(self.handleitemClicked)

	def handleitemClicked(self, item):
		if type(item)==ColorQTableWidgetItem:
			col = QtGui.QColorDialog.getColor(QColor(int(str(item.text()),16)))
			color=col.rgba()
			if col.isValid():
				#col.getRgb()
				item.setText(str(color))
				#item.setBackgroundColor(QColor(color))
				self.updatePropertiesTable()

class EditorWindow(ResourceWindow):
	def initEditor(self):
		self.sciEditor = QsciScintilla(self)
		self.sciEditor.setFrameStyle(QsciScintilla.NoFrame)
		#self.sciEditor.setWrapMode(QsciScintilla.WrapCharacter)
		self.sciEditor.setCaretLineVisible(True)
		font = self.mainwindow.editorFont
		font.setFixedPitch(True)
		self.sciEditor.setFont(font)
		lexer = LexerGame(self.mainwindow)
		lexer.setFont(font)
		self.sciEditor.setLexer(lexer)
		fontmetrics = QFontMetrics(font)
		self.sciEditor.setMarginWidth(0, fontmetrics.width("__")+8)
		self.sciEditor.setMarginLineNumbers(0, True)
		self.sciEditor.setMarginSensitivity(1, True)
		self.BREAK_MARKER_NUM = 8
		#self.setMarginWidth()
		self.sciEditor.marginClicked.connect(self.handleMarginClicked)
		#connect(sciEditor,SIGNAL(marginClicked(int, int, Qt.KeyboardModifiers)), self,SLOT(on_margin_clicked(int, int, Qt.KeyboardModifiers)))
		self.sciEditor.markerDefine(QImage(resourcePath+"actions/link_break.png"),self.BREAK_MARKER_NUM);
		self.sciEditor.setBraceMatching(QsciScintilla.SloppyBraceMatch)
		self.sciEditor.setFolding(QsciScintilla.BoxedTreeFoldStyle, 3)
		self.sciEditor.setMarginsFont(font)
		if self.mainwindow.ideTheme==1:
			self.sciEditor.setMarginsForegroundColor(QColor("#bbbbbb"))
			self.sciEditor.setCaretLineBackgroundColor(QColor("#333333"))
			self.sciEditor.setMarginsBackgroundColor(QColor("#222222"))
			self.sciEditor.setFoldMarginColors(QColor("#282828"), QColor("#282828"))
			lexer.setPaper(QColor("#222222"))
		else:
			self.sciEditor.setCaretLineBackgroundColor(QColor("#ffe4e4"))
			self.sciEditor.setMarginsBackgroundColor(QColor("#dddddd"))
			self.sciEditor.setFoldMarginColors(QColor("#dddddd"), QColor("#dddddd"))
			lexer.setPaper(QColor("#ffffff"))
		#setIndentationWidth
		self.sciEditor.setTabWidth(2)
		self.sciEditor.SendScintilla(QsciScintillaBase.SCI_SETMULTIPASTE,1)
		q=QWidget()
		self.setWidget(q)
		layout = QVBoxLayout(q)
		layout.addWidget(self.sciEditor)
		layout.setContentsMargins(0, 0, 0, 0)
		q.setLayout(layout)
		# sciEditor.setFixedHeight(300);

	def __init__(self, mainwindow, res, defaultTitle=None):
		ResourceWindow.__init__(self, mainwindow, res, defaultTitle)
		self.initEditor()

	def closeEvent(self, closeEvent):
		ResourceWindow.closeEvent(self, closeEvent)

	def handleMarginClicked(self, nmargin, nline, modifiers):
		# Toggle marker for the line the margin was clicked on
		if self.sciEditor.markersAtLine(nline) != 0:
			self.sciEditor.markerDelete(nline, self.BREAK_MARKER_NUM)
		else:
			self.sciEditor.markerAdd(nline, self.BREAK_MARKER_NUM)
