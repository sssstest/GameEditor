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

class ObjectWindow(EditorWindow):
	def __init__(self, mainwindow, res):
		EditorWindow.__init__(self, mainwindow, res)
		self.setWindowIcon(QIcon(resourcePath+"resources/object.png"))
		self.propertiesList=["name","id",#"spriteIndex",
		"sprite","depth",
		#"parentIndex",
		"parent",#"maskIndex",
		"mask","visible","solid","persistent",
		"PhysicsObject","PhysicsObjectSensor","PhysicsObjectShape","PhysicsObjectDensity",
		"PhysicsObjectRestitution","PhysicsObjectGroup","PhysicsObjectLinearDamping","PhysicsObjectAngularDamping",
		"PhysicsObjectFriction","PhysicsObjectAwake","PhysicsObjectKinematic","PhysicsShapePoints"]
		self.propertiesType={"sprite":CliClass.GameSprite,"parent":CliClass.GameObject,"mask":CliClass.GameSprite}
		ggg=res.WriteGGG(False)
		self.sciEditor.setText(ggg)
		
		q=QWidget(self)
		self.setWidget(q)
		layout = QVBoxLayout(q)

		q2=QWidget(q)
		layout2 = QHBoxLayout(q2)
		layout2.addWidget(QLabel("Events:"))
		self.eventsList=QComboBox(q)
		m_lw=QListWidget(q)
		names=[]
		for event in self.res.events:
			names.append(event.eventGGGName())
		ev_createDone=False
		ev_destroyDone=False
		#for event in names:
		#	self.eventsList.addItem(event)
		#self.eventsList.insertSeparator(99)
		self.m_lwAddItem(m_lw,"@ev_create","@ev_create" in names)
		self.m_lwAddItem(m_lw,"@ev_destroy","@ev_destroy" in names)
		for event in names:
			if event.startswith("@ev_alarm"):
				self.m_lwAddItem(m_lw,event,True)
		self.m_lwAddItem(m_lw,"@ev_alarm()")
		for event in names:
			if event.startswith("@ev_step"):
				self.m_lwAddItem(m_lw,event,True)
		if "@ev_step(normal)" not in names:
			self.m_lwAddItem(m_lw,"@ev_step(normal)")
		if "@ev_step(begin)" not in names:
			self.m_lwAddItem(m_lw,"@ev_step(begin)")
		if "@ev_step(end)" not in names:
			self.m_lwAddItem(m_lw,"@ev_step(end)")
		for event in names:
			if event.startswith("@ev_collision"):
				self.m_lwAddItem(m_lw,event,True)
		self.m_lwAddItem(m_lw,"@ev_collision()")
		for event in names:
			if event.startswith("@ev_keyboard"):
				self.m_lwAddItem(m_lw,event,True)
		self.m_lwAddItem(m_lw,"@ev_keyboard()")
		for event in names:
			if event.startswith("@ev_mouse"):
				self.m_lwAddItem(m_lw,event,True)
		self.m_lwAddItem(m_lw,"@ev_mouse()")
		for event in names:
			if event.startswith("@ev_other"):
				self.m_lwAddItem(m_lw,event,True)
		self.m_lwAddItem(m_lw,"@ev_other()")
		for event in names:
			if event.startswith("@ev_draw"):
				self.m_lwAddItem(m_lw,event,True)
		if "@ev_draw(normal)" not in names:
			self.m_lwAddItem(m_lw,"@ev_draw(normal)")
		if "@ev_draw(gui)" not in names:
			self.m_lwAddItem(m_lw,"@ev_draw(gui)")
		for event in names:
			if event.startswith("@ev_press"):
				self.m_lwAddItem(m_lw,event,True)
		self.m_lwAddItem(m_lw,"@ev_press()")
		for event in names:
			if event.startswith("@ev_release"):
				self.m_lwAddItem(m_lw,event,True)
		self.m_lwAddItem(m_lw,"@ev_release()")
		for event in names:
			if event.startswith("@ev_async"):
				self.m_lwAddItem(m_lw,event,True)
		self.m_lwAddItem(m_lw,"@ev_async()")
		
		self.eventsList.setModel(m_lw.model())
		self.eventsList.setView(m_lw)

		self.eventsList.currentIndexChanged.connect(self.handleEventsListChanged)
		layout2.addWidget(self.eventsList)
		layout2.addWidget(QLabel("Actions:"))
		self.actionsList=QComboBox(q)
		self.actionsList.addItem("@code")
		self.actionsList.addItem("@comment")
		self.actionsList.addItem("@else")
		self.actionsList.addItem("@start")
		self.actionsList.addItem("@repeat")
		self.actionsList.addItem("@end")
		self.actionsList.addItem("@exitevent")
		self.actionsList.addItem("@set")
		self.actionsList.currentIndexChanged.connect(self.handleActionsListChanged)
		layout2.addWidget(self.actionsList)
		q2.setLayout(layout2)

		layout.addWidget(q2)
		layout.addWidget(self.sciEditor)
		layout.setContentsMargins(0, 0, 0, 0)
		q.setLayout(layout)

	def m_lwAddItem(self,m_lw,text,bold=False):
		lwi = QListWidgetItem(text)
		font = lwi.font()
		font.setBold(bold)
		lwi.setFont(font)
		m_lw.addItem(lwi)

	def handleEventsListChanged(self, event):
		self.saveResource()
		#self.shaderIndex=self.shaderList.currentText()
		#self.sciEditor.setText(self.res.getMember(str(self.shaderIndex)))

	def handleActionsListChanged(self, event):
		self.saveResource()
		#self.shaderIndex=self.shaderList.currentText()
		#self.sciEditor.setText(self.res.getMember(str(self.shaderIndex)))

	def saveResource(self):
		if self.sciEditor.isModified():
			self.mainwindow.projectSetModified(True)
			try:
				self.res.ReadGGG(str(self.sciEditor.text()))
			except NotImplementedError:
				CliClass.print_warning("unsupported")
				closeEvent.ignore()
				return

	def closeEvent(self, closeEvent):
		if self.sciEditor.isModified():
			self.mainwindow.projectSetModified(True)
			try:
				closeEvent.ignore()
				self.res.ReadGGG(str(self.sciEditor.text()))
			except NotImplementedError:
				CliClass.print_warning("unsupported")
				closeEvent.ignore()
				return
			#except:
			#	closeEvent.ignore()
			#	return
		EditorWindow.closeEvent(self,closeEvent)
