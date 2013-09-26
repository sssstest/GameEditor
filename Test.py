#!/usr/bin/env python

from CliClass import *
from PyQt4 import QtGui, QtCore#font

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
g.compileRunEnigma("/tmp/testgame",emode_debug)
