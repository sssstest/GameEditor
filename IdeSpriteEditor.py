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

class SpriteWindow(ResourceWindow):
	def __init__(self, mainwindow, res):
		ResourceWindow.__init__(self, mainwindow, res)
		self.setWindowIcon(QIcon(resourcePath+"resources/sprite.png"))
		self.propertiesList=["name","id","smoothedges","preload","transparent","xorigin","yorigin",
		"maskshape","bboxmode","bbox_left","bbox_right","bbox_bottom","bbox_top",
		"alphatolerance","precisecollisionchecking","seperatemasks",
		"HTile","VTile","For3D","width","height"]
		self.propertiesType={"maskshape":"spriteMaskshape","bboxmode":"spriteBboxmode"}
		for subimage in res.subimages:
			imageLabel = QLabel()
			p=QPixmap()
			if len(res.subimages)>0:
				p.convertFromImage(subimage.getQImage())
			imageLabel.setPixmap(p)
			imageLabel.setBackgroundRole(QPalette.Base)
			#imageLabel.setSizePolicy(QSizePolicy::Ignored, QSizePolicy::Ignored);
			imageLabel.setScaledContents(True)
			w=p.size().width()
			h=p.size().height()
			ww = self.size().width()
			wh = self.size().height()
			imageLabel.resize(w,h)
		scrollArea = QScrollArea()
		scrollArea.setBackgroundRole(QPalette.Dark)
		scrollArea.setWidget(imageLabel)
		q=QWidget()
		self.setWidget(q)
		layout = QVBoxLayout(q)
		layout.addWidget(scrollArea)
		load=QPushButton("&Load File", self)
		save=QPushButton("&Save File", self)
		q2=QWidget()
		layout2 = QHBoxLayout(q2)
		layout2.addWidget(load)
		layout2.addWidget(save)
		q2.setLayout(layout2)
		layout.addWidget(q2)
		layout.setContentsMargins(0, 0, 0, 0)
		q.setLayout(layout)
