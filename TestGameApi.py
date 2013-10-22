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

from CliClass import *
from PyQt4 import QtGui, QtCore#font
testGameFile=tmpDir+"testgame.exe"

resourcePath=os.path.join(module_path(),"ideicons")+"/"

LoadPluginLib()
g=GameFile()
g.app = QtGui.QApplication(["python"])
r=g.newRoom()
i=r.newInstance()
o=g.newObject()
s=g.newSprite()
s.newSubimageFile(resourcePath+"resources/sprite.png")
o.setMember("sprite",s)
i.setMember("object",o)
g.newSettings()
g.compileRunEnigma(testGameFile,emode_debug)
