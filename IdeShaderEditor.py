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

class ShaderWindow(EditorWindow):
	def __init__(self, mainwindow, res):
		EditorWindow.__init__(self, mainwindow, res)
		self.setWindowIcon(QIcon(resourcePath+"resources/shader.png"))
		self.propertiesList=["name","id","type","precompile"]
		self.propertiesType={"type":"shadertype"}
		self.shaderIndex="vertex"
		self.sciEditor.setText(self.res.getMember(str(self.shaderIndex)))
		
		q=QWidget(self)
		self.setWidget(q)
		layout = QVBoxLayout(q)

		q2=QWidget(q)
		layout2 = QHBoxLayout(q2)
		layout2.addWidget(QLabel("Shader:"))
		self.shaderList=QComboBox(q)
		self.shaderList.addItem("vertex")
		self.shaderList.addItem("fragment")
		self.shaderList.currentIndexChanged.connect(self.handleShaderListChanged)
		layout2.addWidget(self.shaderList)
		q2.setLayout(layout2)

		layout.addWidget(q2)
		layout.addWidget(self.sciEditor)
		layout.setContentsMargins(0, 0, 0, 0)
		q.setLayout(layout)

	def handleShaderListChanged(self, event):
		self.saveResource()
		self.shaderIndex=self.shaderList.currentText()
		self.sciEditor.setText(self.res.getMember(str(self.shaderIndex)))

	def saveResource(self):
		if self.sciEditor.isModified():
			self.mainwindow.projectSetModified(True)
			self.res.setMember(str(self.shaderIndex),str(self.sciEditor.text()))

	def closeEvent(self, closeEvent):
		if self.sciEditor.isModified():
			self.mainwindow.projectSetModified(True)
			self.res.setMember(str(self.shaderIndex),str(self.sciEditor.text()))
		EditorWindow.closeEvent(self, closeEvent)
