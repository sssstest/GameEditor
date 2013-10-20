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

class GameSettingsWindow(EditorWindow):
	def __init__(self, mainwindow, res):
		EditorWindow.__init__(self, mainwindow, res, "Game Settings")
		self.setWindowIcon(QIcon(resourcePath+"resources/gm.png"))
		self.propertiesList=["fullscreen","scale","interpolate","windowcolor","sizeable",
		"stayontop","noborder","nobuttons","showcursor","freeze",
		"vsync","changeresolution",
		"quitkey","helpkey","fullscreenkey","savekey","screenshotkey","priority",
		"loadImage","loadtransparent","loadalpha",
		"showprogress","frontImage","backImage","scaleprogress","iconImage",#gameId
		"displayerrors","writeerrors","aborterrors","treatUninitializedVariablesAsZero","argumenterrors",
		"version_product","author","version","version_copyright",#"version_information",
		
		"version_major","version_minor","version_release","version_build",
		"version_company","version_description",
		
		"colordepth","resolution","frequency",
		"noscreensaver","closesecondary",
		"errorFlags"]
		self.propertiesType={"windowcolor":"color"}
		self.sciEditor.setText(self.res.getMember("version_information"))
		
		q=QWidget(self)
		self.setWidget(q)
		layout = QVBoxLayout(q)

		q2=QWidget(q)
		layout2 = QHBoxLayout(q2)
		layout2.addWidget(QLabel("Version Information"))
		q2.setLayout(layout2)

		layout.addWidget(q2)
		layout.addWidget(self.sciEditor)
		layout.setContentsMargins(0, 0, 0, 0)
		q.setLayout(layout)
