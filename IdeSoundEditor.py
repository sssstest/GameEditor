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

class SoundWindow(ResourceWindow):
	def __init__(self, mainwindow, res):
		ResourceWindow.__init__(self, mainwindow, res)
		self.setWindowIcon(QIcon(resourcePath+"resources/sound.png"))
		self.propertiesList=["name","id","kind","effects","preload",
		"volume","pan","mp3BitRate","oggQuality","extension","origname"]
		self.propertiesType={"kind":"soundKind"}
		play=QPushButton("&Play", self)
		play.pressed.connect(self.handlePlayPressed)
		stop=QPushButton("S&top", self)
		stop.pressed.connect(self.handleStopPressed)
		load=QPushButton("&Load File", self)
		save=QPushButton("&Save File", self)
		q=QWidget()
		self.setWidget(q)
		layout = QHBoxLayout(q)
		layout.addWidget(play)
		layout.addWidget(stop)
		layout.addWidget(load)
		layout.addWidget(save)
		q.setLayout(layout)

	def handlePlayPressed(self):
		CliClass.print_warning("starting avplay")
		self.playerProcess = QProcess()
		self.playerProcess.start("avplay -vn -nodisp -autoexit -i pipe:")
		#self.playerProcess.readyReadStandardOutput.connect(self.handleProcessOutput)
		#self.playerProcess.readyReadStandardError.connect(self.handleProcessErrorOutput)
		self.playerProcess.finished.connect(self.handleProcessFinished)
		self.playerProcess.writeData(self.res.getMember("data").Read())
		self.playerProcess.closeWriteChannel()

	def handleStopPressed(self):
		self.playerProcess.kill()

	def handleProcessFinished(self):
		CliClass.print_warning("done avplay")
		self.playerProcess.close()
