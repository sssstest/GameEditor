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

from IdeResource import *
from IdeRoomEditor import *

class PathWindow(ResourceWindow):
	def __init__(self, mainwindow, res):
		ResourceWindow.__init__(self, mainwindow, res)
		self.setWindowIcon(QIcon(resourcePath+"resources/path.png"))
		self.propertiesList=["name","id","snapX","snapY",#"roomIndex",
		"room","connectionKind","closed","precision"]
		self.propertiesType={"room":CliClass.GameRoom,"connectionKind":"pathConnectionKind"}
		self.app=mainwindow.app
		splitter = QSplitter(self)
		q=QWidget(splitter)
		splitter.addWidget(q)
		layout = QVBoxLayout(q)
		self.tree=QTreeWidget(q)
		self.tree.header().setVisible(False)
		#self.tree.itemSelectionChanged.connect(self.handleItemSelectionChanged)
		layout.addWidget(self.tree)

		q2=QWidget(q)
		layout2 = QHBoxLayout(q2)
		#layout2.addWidget(QLabel("Add Object:"))
		#self.addObjectList=ResourceQComboBox(q,mainwindow,CliClass.GameObject,None)
		#self.addObjectList.setCurrentIndex(1)
		#self.addObjectList.currentIndexChanged.connect(self.handleCurrentIndexChanged)
		#layout2.addWidget(self.addObjectList)
		q2.setLayout(layout2)
		layout.addWidget(q2)
		#layout.addWidget(QLabel("Control click to add object instances"))

		layout.setContentsMargins(0, 0, 0, 0)
		q.setLayout(layout)
		self.scrollAreas = QScrollArea(splitter)
		self.updateTree()
		splitter.addWidget(self.scrollAreas)
		splitter.setSizes([self.width()*.25,self.width()*.75])
		self.setWidget(splitter)
		self.activeItem=None
		self.res.addListener(self.resListener)
		#self.activeItem=self.addObjectList.currentText()

	def resListener(self,type,member,value,val):
		self.updateTree()

	#def keyReleaseEvent(self, event):
	#	QWidget.keyReleaseEvent(self, event)
	#	if event.matches(QKeySequence.Delete):
	#		item=self.tree.currentItem()
	#		if item:
	#			if type(item.res) == CliClass.GameRoomInstance:
	#				self.res.instances.remove(item.res)
	#		self.updateTree()

	#def handleCurrentIndexChanged(self):
	#	self.activeItem=self.addObjectList.currentText()

	#def handleItemSelectionChanged(self):
	#	item=self.tree.selectedItems()
		#if len(item)>0:
		#	self.activeItem=item[0].text(0)

	def updateTree(self):
		#self.tree.clear()
		#for i in self.res.points:
		#	item = QTreeWidgetItem(self.instancesItem,[name,str(i.getMember("x"))+","+str(i.getMember("y"))])
		#	item.res=i
		roomView=RoomView(self.scrollAreas, None, self)
		roomView.gridX=self.res.getMember("snapX")
		roomView.gridY=self.res.getMember("snapY")
		roomView.updateBrush()
		self.scrollAreas.setWidget(roomView)
