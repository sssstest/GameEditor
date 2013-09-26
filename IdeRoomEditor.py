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

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.Qsci import *
import CliClass

class RoomViewInstance(QWidget):
	def __init__(self, image, res, parent, qTreeWidgetItem):
		QWidget.__init__(self, parent)
		self.image=image
		self.rotation=0
		if image:
			self.scaledWidth=self.image.width()
			self.scaledHeight=self.image.height()
			self.resize(self.scaledWidth+8,self.scaledHeight+8)
			self.containerWidth=self.scaledHeight+8
			self.containerHeight=self.image.height()+8
		else:
			self.resize(64,64)
			self.containerWidth=64
			self.containerHeight=64
			self.scaledWidth=64
			self.scaledHeight=64
		self.res=res
		self.selected=False
		self.qTreeWidgetItem=qTreeWidgetItem

		self.updateFromRes()

	def updateFromRes(self):
		x=self.res.getMember("x")
		y=self.res.getMember("y")
		scaleX=self.res.getMember("scaleX")
		scaleY=self.res.getMember("scaleY")
		self.rotation=self.res.getMember("rotation")
		self.move(x-4,y-4)

		transform=QTransform()
		transform.rotate(self.rotation)
		rect=self.contentsRect()
		mapRect=transform.mapRect(rect)
		self.resize(mapRect.width(),mapRect.height())

	def paintEvent(self, event):
		painter = QtGui.QPainter(self)
		matrix=QMatrix()
		matrix.translate(self.width()/2, self.height()/2)
		matrix.rotate(self.rotation)
		matrix.translate(-self.scaledWidth/2, -self.scaledHeight/2)
		transform=QTransform(matrix)
		rect=self.contentsRect()
		mapRect=transform.mapRect(rect)
		painter.setTransform(transform)
		if self.image:
			painter.drawImage(QRect(0,0,self.scaledWidth,self.scaledHeight),self.image)
			self.containerWidth=self.scaledWidth+8
			self.containerHeight=self.scaledHeight+8
		else:
			painter.drawText(6,6,64,64,0,"no\nsprite")
			self.containerWidth=64
			self.containerHeight=64
		if self.selected:
			transform=QTransform()
			painter.setTransform(transform)
			painter.setPen(QColor(0))
			painter.setBrush(QColor(255,0,0))
			painter.drawRect(0,0,7,7)
			painter.drawRect(self.containerWidth-8,0,7,7)
			painter.drawRect(0,self.containerHeight-8,7,7)
			painter.drawRect(self.containerWidth-8,self.containerHeight-8,7,7)
			painter.setBrush(QColor(0,255,0))
			painter.drawEllipse(self.containerWidth-8,(self.containerHeight-8)/2,7,7)

	def setRotation(self, angle):
		self.rotation=angle

	def moveRes(self, qPoint):
		self.move(qPoint)
		self.res.setMember("x", qPoint.x()+4)
		self.res.setMember("y", qPoint.y()+4)

	def setScaleImageSize(self, width, height):
		self.scaledWidth=width
		self.scaledHeight=height
		self.resize(self.scaledWidth+8,self.scaledHeight+8)

	def getScaledWidth(self):
		return self.scaledWidth

	def getScaledHeight(self):
		return self.scaledHeight

class RoomView(QWidget):
	def __init__(self, parent, res, roomWindow):
		QWidget.__init__(self, parent)
		self.res=res
		self.roomWindow=roomWindow
		self.app=self.roomWindow.app
		self.rubberBand=None
		self.resize(self.res.getMember("width"), self.res.getMember("height"))
		self.gridX=160
		self.gridY=160
		self.updateBrush()
		self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
		for c in range(self.roomWindow.tree.topLevelItemCount()):
			item=self.roomWindow.tree.topLevelItem(c)
			for c in range(item.childCount()):
				x=item.child(c)
				if x.res and type(x.res)==CliClass.GameRoomInstance:
					i=x.res
					imageLabel=None
					if i.getMember("object"):
						if i.getMember("object").getMember("sprite"):
							if len(i.getMember("object").getMember("sprite").subimages)>0:
								q=i.getMember("object").getMember("sprite").subimages[0].getQImage()
								imageLabel=RoomViewInstance(q,i,self,x)
					if not imageLabel:
						imageLabel=RoomViewInstance(None,i,self,x)
					imageLabel.updateFromRes()

	def updateBrush(self):
		x=0
		y=0
		height=self.gridY
		width=self.gridX
		i=QtGui.QImage(width,height,QtGui.QImage.Format_ARGB32)
		painter=QtGui.QPainter(i)
		color = QColor(0xff000000 | self.res.getMember("color"))
		colorLighter=QColor()
		colorLighter.setRgb((color.getRgb()[0]+40) % 255,(color.getRgb()[1]+40) % 255,(color.getRgb()[2]+40) % 255,255)
		painter.setBrush(color)#0x1ea0e6))
		painter.drawRect(-1,-1,width,height)
		painter.setPen(colorLighter)#0x13648f))
		painter.drawLine(width-1,0,width-1,height-1)
		painter.drawLine(0,height-1,width-1,height-1)
		painter.setPen(colorLighter.lighter())#0x73c4ef))
		painter.drawLine(0,0,width,0)
		painter.drawLine(0,0,0,height)
		painter.end()
		self.brush=QBrush(i)
		x=0
		y=0
		height=self.gridY
		width=self.gridX
		i=QtGui.QImage(width,height,QtGui.QImage.Format_ARGB32)
		painter=QtGui.QPainter(i)
		cx0 = x + (width >> 1)
		cy0 = y + (height >> 1)
		cx1 = x + (width + 1 >> 1)
		cy1 = y + (height + 1 >> 1)
		painter.setBrush(QColor(0x1ea0e6))
		painter.drawRect(-1,-1,width+1,height+1)
		painter.setPen(QColor(0,0,50))
		painter.drawLine(x + 1,cy1,cx0,y + height - 1)
		painter.drawLine(cx1,y + height - 1,x + width - 1,cy1)
		painter.drawLine(x + width,cy0 - 1,cx1 + 1,y)
		painter.drawLine(cx0 - 1,y,x,cy0 - 1)
		painter.setPen(QColor(200,200,250))
		painter.drawLine(x + width - 1,cy0,cx1,y + 1)
		painter.drawLine(cx0,y + 1,x + 1,cy0)
		painter.drawLine(x,cy1 + 1,cx0 - 1,y + height)
		painter.drawLine(cx1 + 1,y + height,x + width,cy1 + 1)
		painter.end()
		self.isometricBrush=QBrush(i)

	def paintEvent(self, event):
		side = min(self.width(), self.height())
		painter = QtGui.QPainter(self)
		if self.res.getMember("isometric"):
			painter.setBrush(self.isometricBrush)
		else:
			painter.setBrush(self.brush)
		painter.setPen(Qt.NoPen)
		painter.drawRect(0,0,1000,1000)

	def mousePressEvent(self, event):
		self.origin = event.pos()
		self.moveSelection=False
		self.resizeSelection=False
		self.rotateSelection=False
		if self.app.keyboardModifiers() == Qt.ControlModifier:
			item=self.res.gameFile.GetResourceName(CliClass.GameObject, self.roomWindow.activeItem)
			if item:
				inst=self.res.newInstance()
				inst.setMember("x",self.origin.x())
				inst.setMember("y",self.origin.y())
				inst.setMember("object",item)
				self.roomWindow.updateTree()
			return
		for c in reversed(self.children()):
			if type(c)==RoomViewInstance and c.geometry().contains(self.origin):
				if not c.selected:
					for chil in self.children():
						if self.app.keyboardModifiers() != Qt.ShiftModifier:
							chil.selected=False
							chil.update()
					c.selected=True
					c.update()
				point = self.origin-c.geometry().topLeft()
				if QRect(0,0,8,8).contains(point):
					CliClass.print_notice("resize unsupported")
				elif QRect(c.containerWidth-8,0,8,8).contains(point):
					CliClass.print_notice("resize unsupported")
				elif QRect(0,c.containerHeight-8,8,8).contains(point):
					CliClass.print_notice("resize unsupported")
				elif QRect(c.containerWidth-8,c.containerHeight-8,8,8).contains(point):
					self.resizeSelection=True
					return
				elif QRect(c.containerWidth-8,(c.containerHeight-8)/2,8,8).contains(point):
					self.rotateSelection=True
					self.origin=QPoint(c.x()+(c.width()/2),c.y()+(c.height()/2))
				self.moveSelection=True
				self.roomWindow.tree.setCurrentItem(c.qTreeWidgetItem)
				return
		self.rubberBand.setGeometry(QRect(self.origin, QSize()))
		self.rubberBand.show()

	def mouseMoveEvent(self, event):
		if self.rotateSelection:
			import math
			x=event.pos().x()-self.origin.x()
			y=event.pos().y()-self.origin.y()
			angle=math.atan2(y,x) * 180 / math.pi
			for c in self.children():
				if type(c)==RoomViewInstance and c.selected:
					angle=(angle+360)%360
					c.setRotation(angle)
					c.update()
			return
		if self.resizeSelection:
			for c in self.children():
				if type(c)==RoomViewInstance and c.selected:
					c.setScaleImageSize(c.scaledWidth+(event.pos().x()-self.origin.x()),c.scaledHeight+(event.pos().y()-self.origin.y()))
					c.update()
			self.origin=event.pos()
			return
		if self.moveSelection:
			for c in self.children():
				if type(c)==RoomViewInstance and c.selected:
					c.moveRes(c.pos()+(event.pos()-self.origin))
			self.origin=event.pos()
			return
		if self.rubberBand:
			self.rubberBand.setGeometry(QRect(self.origin, event.pos()).normalized())

	def mouseReleaseEvent(self, event):
		if not self.moveSelection and not self.resizeSelection and not self.rotateSelection:
			self.rubberBand.hide()
			for c in self.children():
				if type(c)==RoomViewInstance and c.selected:
					c.selected=False
					c.update()
				if self.origin.x()<event.pos().x() and self.origin.y()<event.pos().y():
					rect=QRect(self.origin,event.pos())
				else:
					rect=QRect(event.pos(),self.origin)
				if rect.intersects(c.geometry()):
					if type(c)==RoomViewInstance:
						c.selected=True
						c.update()
