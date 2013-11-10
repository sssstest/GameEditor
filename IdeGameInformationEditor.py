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

class GameInformationWindow(EditorWindow):
	def __init__(self, mainwindow, res):
		EditorWindow.__init__(self, mainwindow, res, "Game Information")
		self.setWindowIcon(QIcon(resourcePath+"resources/info.png"))
		self.propertiesList=["left","top","width","height",
		"showborder","sizeable","alwaysontop","freeze",
		"showInSeperateWindow","caption",
		"backgroundcolor"]
		self.propertiesType={"backgroundcolor":"color"}
		self.sciEditor.setText(self.res.getMember("information").decode())
