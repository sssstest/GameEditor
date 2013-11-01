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
import sys
import os
if sys.version_info[0]<3:
	from ConfigParser import *
else:
	from configparser import *
import CliClass
#from IdeResource import *
from IdeGGGWindow import *
from IdeSpriteEditor import *
from IdeSoundEditor import *
from IdeBackgroundEditor import *
from IdePathEditor import *
from IdeScriptEditor import *
from IdeShaderEditor import *
from IdeFontEditor import *
from IdeTimelineEditor import *
from IdeObjectEditor import *
from IdeRoomEditor import *
from IdeGameInformationEditor import *
from IdeGameSettingsEditor import *

class SpriteQIconUpdateThread(QtCore.QThread):
			outputSignal = pyqtSignal(object, name = 'stepIncreased')
			def run(self):
				for s in self.mainwindow.gmk.sprites:
					self.outputSignal.emit(s)
					#s.updateQIcon()
				#self.mainwindow
			#def outputLine(self, text):
			#	self.outputSignal.emit(text)

class PreferencesDialog(QDialog):
	def __init__(self, parent=None):
		self.mainwindow=parent
		self.enigmaPath=parent.enigmaPath
		self.projectSavingEnabled=parent.projectSavingEnabled
		super(PreferencesDialog, self).__init__(parent)
		label = QLabel("enigma-dev path:")
		lineEdit = QLineEdit()
		lineEdit.setText(self.enigmaPath)
		lineEdit.setMaximumWidth(400)
		lineEdit.setFixedWidth(420)
		label.setBuddy(lineEdit)
		savingEnabledLabel = QLabel("saving gmk enabled:")
		self.savingEnabledQCheckBox = QCheckBox("saving")
		if self.projectSavingEnabled:
			self.savingEnabledQCheckBox.setChecked(True)

		setButton = QPushButton("&Set")
		setButton.clicked.connect(self.handleSetAction)
		doneButton = QPushButton("&Done")
		doneButton.clicked.connect(self.handleDoneAction)
		doneButton.setDefault(True)
		closeButton = QPushButton("Close")
		closeButton.clicked.connect(self.handleCloseAction)
		buttonBox = QDialogButtonBox(Qt.Horizontal)
		#buttonBox.addButton(setButton, QDialogButtonBox.ActionRole)
		buttonBox.addButton(doneButton, QDialogButtonBox.ActionRole)
		buttonBox.addButton(closeButton, QDialogButtonBox.ActionRole)
		topLeftLayout = QGridLayout()
		topLeftLayout.addWidget(label, 0, 0)
		topLeftLayout.addWidget(lineEdit, 0, 1)
		topLeftLayout.addWidget(setButton, 0, 2)
		savingEnabledLayout = QGridLayout()
		savingEnabledLayout.addWidget(savingEnabledLabel, 0, 0)
		savingEnabledLayout.addWidget(self.savingEnabledQCheckBox, 0, 1)
		leftLayout = QVBoxLayout()
		leftLayout.addLayout(topLeftLayout)
		leftLayout.addLayout(savingEnabledLayout)
		mainLayout = QVBoxLayout()
		mainLayout.setSizeConstraint(QLayout.SetFixedSize)
		mainLayout.addLayout(leftLayout)
		mainLayout.addWidget(buttonBox)
		self.setLayout(mainLayout)
		self.setWindowTitle("Preferences")

	def handleDoneAction(self):
		self.mainwindow.enigmaPath=self.enigmaPath
		self.mainwindow.projectSavingEnabled=self.savingEnabledQCheckBox.checkState()
		self.mainwindow.savePreferences()
		self.accept()

	def handleCloseAction(self):
		self.mainwindow.enigmaPath=self.enigmaPath
		self.mainwindow.projectSavingEnabled=self.savingEnabledQCheckBox.checkState()
		self.mainwindow.savePreferences()
		self.accept()

	def handleSetAction(self):
		self.enigmaPath = QFileDialog.getExistingDirectory(self,"Open", "", QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
		if self.enigmaPath!="":
			self.mainwindow.enigmaPath=self.enigmaPath
			self.mainwindow.projectSavingEnabled=self.savingEnabledQCheckBox.checkState()
			CliClass.print_notice("new enigma path: "+self.enigmaPath)
			self.mainwindow.savePreferences()
			self.accept()

class FindDialog(QDialog):
	def __init__(self, parent=None):
		super(FindDialog, self).__init__(parent)
		label = QLabel("Find what:")
		lineEdit = QLineEdit()
		label.setBuddy(lineEdit)
		label2 = QLabel("Replace with:")
		lineEdit2 = QLineEdit()
		label2.setBuddy(lineEdit2)
		wholeWordCheckBox = QCheckBox("Whole word")
		caseCheckBox = QCheckBox("Case sensitive")
		escapeCheckBox = QCheckBox("Escape sequences")
		reCheckBox = QCheckBox("Regular expression")
		fromStartCheckBox = QCheckBox("Search from &start")
		wrapAroundCheckBox = QCheckBox("Wrap around")
		wrapAroundCheckBox.setChecked(True)
		searchBackwardsCheckBox = QCheckBox("Search backwards")

		selectionRadio= QRadioButton("Selection")
		resourceRadio = QRadioButton("Open Resource")
		resourceRadio.setChecked(True)
		allOpenResourcesRadio = QRadioButton("All Open Resources")
		allScriptsRadio = QRadioButton("All Scripts")
		allObjectsRadio = QRadioButton("All Objects")
		allScriptsAndObjectsRadio = QRadioButton("All Scripts and Objects")
		allResourcesGGG = QRadioButton("All Resources")

		findButton = QPushButton("&Find")
		findButton.setDefault(True)
		replaceButton = QPushButton("&Replace")
		replaceAllButton = QPushButton("Replace all")
		closeButton = QPushButton("Close")
		buttonBox = QDialogButtonBox(Qt.Horizontal)
		buttonBox.addButton(findButton, QDialogButtonBox.ActionRole)
		buttonBox.addButton(replaceButton, QDialogButtonBox.ActionRole)
		buttonBox.addButton(replaceAllButton, QDialogButtonBox.ActionRole)
		buttonBox.addButton(closeButton, QDialogButtonBox.ActionRole)
		#moreButton.toggled.connect=setVisible
		topLeftLayout = QGridLayout()
		topLeftLayout.addWidget(label, 0, 0)
		topLeftLayout.addWidget(lineEdit, 0, 1)
		topLeftLayout.addWidget(label2, 1, 0) 
		topLeftLayout.addWidget(lineEdit2, 1,1)
		leftLayout = QVBoxLayout()
		leftLayout.addLayout(topLeftLayout)
		leftLayout4 = QVBoxLayout()
		leftLayout4.addWidget(wholeWordCheckBox)
		leftLayout4.addWidget(caseCheckBox)
		leftLayout4.addWidget(escapeCheckBox)
		leftLayout4.addWidget(reCheckBox)
		leftLayout4.addWidget(fromStartCheckBox)
		leftLayout4.addWidget(wrapAroundCheckBox)
		leftLayout2 = QVBoxLayout()
		leftLayout2.addWidget(selectionRadio)
		leftLayout2.addWidget(resourceRadio)
		leftLayout2.addWidget(allOpenResourcesRadio)
		leftLayout2.addWidget(allScriptsRadio)
		leftLayout2.addWidget(allObjectsRadio)
		leftLayout2.addWidget(allScriptsAndObjectsRadio)
		leftLayout2.addWidget(allResourcesGGG)
		topLeftLayout3 = QHBoxLayout()
		topLeftLayout3.addLayout(leftLayout4)
		topLeftLayout3.addLayout(leftLayout2)
		mainLayout = QVBoxLayout()
		mainLayout.setSizeConstraint(QLayout.SetFixedSize)
		mainLayout.addLayout(leftLayout)
		mainLayout.addLayout(topLeftLayout3)
		mainLayout.addWidget(buttonBox)
		self.setLayout(mainLayout)
		self.setWindowTitle("Find")

class PropertiesTable(QTableWidget):
	def __init__(self, parent):
		QTableWidget.__init__(self, parent)
		self.res=None
		self.subwindow=None

	def dataChanged(self, topLeft, bottomRight):
		if self.updatedTable:
			if topLeft != bottomRight:
				CliClass.print_notice("multple items change unsupported")
			if topLeft.column() != 1:
				return
			member=str(self.item(topLeft.row(),0).text())
			text=str(self.item(topLeft.row(),topLeft.column()).text())
			checked=self.item(topLeft.row(),topLeft.column()).checkState()
			if self.res:
				value=self.res.getMember(member)
				if type(value)==bool:
					if value!=bool(checked):
						self.res.setMember(member,bool(checked))
						self.subwindow.updatePropertiesTable()
				elif type(value)==int:
					if value!=int(text):
						self.res.setMember(member,int(text))
						self.subwindow.updatePropertiesTable()
				elif type(value)==float:
					if value!=float(text):
						self.res.setMember(member,float(text))
						self.subwindow.updatePropertiesTable()
				else:
					if value!=text:
						self.res.setMember(member,text)
						self.subwindow.updatePropertiesTable()
						if member=="name":
							self.mainwindow.updateHierarchyTree()

class MainWindow(QtGui.QMainWindow):
	def __init__(self, app):
		QtGui.QMainWindow.__init__(self)
		self.app=app
		self.findDialog=None
		self.prefsDialog=None
		self.recentFiles=[]

		self.editorFontName = "DejaVu Sans Mono"
		self.editorSize = 10
		self.editorFont=QFont("DejaVu Sans Mono", 8)#Courier 10 Pitch
		self.ideTheme=0
		self.enigmaPath="enigma-dev"
		self.projectSavingEnabled=False
		self.colors = {0: 0xff000000,#DOCUMENT_DEFAULT                        = 0
		1: 0xff008400,#COMMENT                        = 1
		2: 0xff008400,#COMMENTLINE                    = 2
		4: 0xff008484,#NUMBER                        = 4
		5: 0xff0000ff,#7f,#dark blue for funcs#WORD                        = 5
		6: 0xff840084,#STRING                        = 6
		7: 0xff840084,#CHARACTER                    = 7
		9: 0xff7f7f00,#PREPROCESSOR                = 9
		10: 0xffa30000,#OPERATOR                    = 10
		11: 0xff000000,#default#IDENTIFIER                    = 11
		12: 0xff840084,#7f007f,#STRING#STRINGEOL                    = 12
		16: 0xffff0000,#constants red#WORD2                        = 16
		}
		self.themeColors = {32: 0xffc3c3c3,0: 0xff7f7f7f,1: 0xffff80ff,2: 0xffff80ff,3: 0xffc08fc0,4: 0xffff8080,5: 0xff80ff80,6: 0xffffff80,7: 0xff80ff80,
		8: 0xffc3c3c3,9: 0xff8080ff,10: 0xffffffff,11: 0xffc3c3c3,12: 0xffffffff,13: 0xffff80ff,14: 0xffc080c0,15: 0xffc08fc0,16: 0xffc3c3c3,
		17: 0xffcf9f5f,18: 0xff7fbfdf,19: 0xffc3c3c3,20: 0xff80ff80,40: 0xff4f6f4f,64: 0xff3f3f3f,65: 0xff6f4f6f,66: 0xff6f4f6f,67: 0xff2f2f2f,
		68: 0xff6f4f6f,69: 0xff6f6f4f,70: 0xff4f6f4f,71: 0xff4f6f4f,72: 0xff3f3f3f,73: 0xff4f4f6f,74: 0xff4f4f4f,75: 0xff4f4f4f,76: 0xffffffff,
		77: 0xff6f4f6f,78: 0xff805080,79: 0xff3f3f3f,80: 0xff3f3f3f,81: 0xff3f3f3f,82: 0xff3f3f3f,83: 0xff4f4f4f}
		self.loadPreferences()

		self.projectModified=False
		self.projectTitle="noname"
		self.projectLoadPluginLib=False
		self.projectPath=None
		self.debuggerCommands=[]
		self.projectEmode=CliClass.emode_run
		CliClass.print_error=self.outputLine
		CliClass.print_warning=self.outputLine
		CliClass.print_notice=self.outputLine
		self.exitAction = QAction("E&xit", self)
		self.exitAction.setShortcuts(QKeySequence.Quit)
		self.exitAction.triggered.connect(self.handleCloseApplication)
		#self.mdiAction = QAction("&Multiple Document Interface", self)
		#self.mdiAction.triggered.connect(self.handleToggleMdiTabs)
		self.licenseAction = QAction("&License", self)
		self.licenseAction.triggered.connect(self.handleShowLicenseDialog)
		self.aboutAction = QAction("&About", self)
		self.aboutAction.triggered.connect(self.handleShowAboutDialog)
		mainMenuBar = QMenuBar(self)
		fileMenu = QMenu("&File", self)
		buildMenu = QMenu("&Build", self)
		debugMenu = QMenu("&Debug", self)
		editMenu = QMenu("&Edit", self)
		findAction = QAction("&Find", self)
		findAction.setShortcuts(QKeySequence.Find)
		findAction.triggered.connect(self.handleFind)
		editMenu.addAction(findAction)
		viewMenu = QMenu("&View", self)
		#viewMenu.addAction(self.mdiAction)
		themeAction = QAction("&Theme", self)
		themeAction.triggered.connect(self.switchTheme)
		viewMenu.addAction(themeAction)
		updAction = QAction("&Update", self)
		updAction.triggered.connect(self.updateHierarchyTree)
		viewMenu.addAction(updAction)
		statsAction = QAction("Game Stats", self)
		statsAction.triggered.connect(self.handleGameStats)
		viewMenu.addAction(statsAction)
		resourceMenu = QMenu("&Resources", self)
		windowMenu = QMenu("&Window", self)
		helpMenu = QMenu("&Help", self)
		helpMenu.addAction(self.licenseAction)
		helpMenu.addAction(self.aboutAction)
		mainMenuBar.addMenu(fileMenu)
		mainMenuBar.addMenu(buildMenu)
		mainMenuBar.addMenu(debugMenu)
		mainMenuBar.addMenu(editMenu)
		mainMenuBar.addMenu(viewMenu)
		mainMenuBar.addMenu(resourceMenu)
		mainMenuBar.addMenu(windowMenu)
		mainMenuBar.addMenu(helpMenu)
		self.setMenuBar(mainMenuBar)
		fileToolbar = QToolBar()
		newAction = QAction(QIcon(resourcePath+"actions/new.png"), "&New", self)
		newAction.triggered.connect(self.handleNewAction)
		newAction.setShortcuts(QKeySequence.New)
		fileToolbar.addAction(newAction)
		fileMenu.addAction(newAction)
		openAction = QAction(QIcon(resourcePath+"actions/open.png"), "&Open", self)
		openAction.triggered.connect(self.handleOpenAction)
		openAction.setShortcuts(QKeySequence.Open)
		fileToolbar.addAction(openAction)
		fileMenu.addAction(openAction)
		revertAction = QAction(QIcon(resourcePath+"actions/open.png"), "&Revert", self)
		openAction.triggered.connect(self.handleRevertAction)
		#revertAction.setShortcuts(QKeySequence.Revert)
		#fileToolbar.addAction(revertAction)
		fileMenu.addAction(revertAction)
		saveAction = QAction(QIcon(resourcePath+"actions/save.png"), "&Save", self)
		saveAction.triggered.connect(self.handleSaveAction)
		saveAction.setShortcuts(QKeySequence.Save)
		fileToolbar.addAction(saveAction)
		fileMenu.addAction(saveAction)
		saveAsAction = QAction(QIcon(resourcePath+"actions/save-as.png"), "Save As", self)
		saveAsAction.triggered.connect(self.handleSaveAsAction)
		saveAsAction.setShortcuts(QKeySequence.SaveAs)
		fileToolbar.addAction(saveAsAction)
		fileMenu.addAction(saveAsAction)
		fileMenu.addSeparator()
		# add recent projects list
		for fileName in self.recentFiles:
			recentFile=QAction(fileName, self)
			recentFile.triggered.connect(lambda x,fileName=fileName:self.openProject(fileName))
			fileMenu.addAction(recentFile)
		fileMenu.addSeparator()
		preferencesAction = QAction(QIcon(resourcePath+"actions/preferences.png"), "Preferences", self)
		preferencesAction.triggered.connect(self.actionPreferences)
		fileMenu.addAction(preferencesAction)
		fileMenu.addSeparator()
		fileMenu.addAction(self.exitAction)
		self.addToolBar(fileToolbar)
		buildToolbar = QToolBar(self)
		runAction = QAction(QIcon(resourcePath+"actions/execute.png"), "Run", self)
		runAction.triggered.connect(self.handleRunAction)
		runAction.setShortcuts(QKeySequence("F5"))
		buildToolbar.addAction(runAction)
		buildMenu.addAction(runAction)
		debugAction = QAction(QIcon(resourcePath+"actions/debug.png"), "Debug", self)
		debugAction.triggered.connect(self.handleDebugAction)
		buildToolbar.addAction(debugAction)
		buildMenu.addAction(debugAction)
		self.buildTypeList=QComboBox(buildToolbar)
		self.buildTypeList.addItem("Run")
		self.buildTypeList.addItem("Debug")
		#self.buildTypeList.addItem("Design")
		self.buildTypeList.currentIndexChanged.connect(self.handleBuildTypeListChanged)
		buildToolbar.addWidget(self.buildTypeList)
		#buildToolbar.addWidget(QLabel("Platform:"))
		self.buildPlatformList=QComboBox(buildToolbar)
		#if sys.platform.startswith('linux'):
		if os.name=="nt":
			self.buildPlatformList.addItem("Windows")
		else:
			self.buildPlatformList.addItem("Linux X11")
			self.buildPlatformList.addItem("Windows mingw32")
			self.buildPlatformList.addItem("Android")
		self.buildPlatformList.currentIndexChanged.connect(self.handleBuildPlatformListChanged)
		buildToolbar.addWidget(self.buildPlatformList)
		#buildToolbar.addWidget(QLabel("Graphics:"))
		self.buildGraphicsList=QComboBox(buildToolbar)
		self.buildGraphicsList.addItem("OpenGL 1.1")
		self.buildGraphicsList.addItem("OpenGL 3.0")
		if os.name=="nt":
			self.buildGraphicsList.addItem("Direct3D 9.0")
		self.buildGraphicsList.addItem("OpenGLES")
		self.buildGraphicsList.setCurrentIndex(1)
		self.buildGraphicsList.currentIndexChanged.connect(self.handleBuildGraphicsListChanged)
		buildToolbar.addWidget(self.buildGraphicsList)
		"""designAction = QAction(QIcon(resourcePath+"actions/compile.png"), "Design", self)
		buildToolbar.addAction(designAction)
		buildMenu.addAction(designAction)
		compileAction = QAction(QIcon(resourcePath+"actions/compile.png"), "Compile", self)
		buildToolbar.addAction(compileAction)
		buildMenu.addAction(compileAction)
		rebuildAction = QAction(QIcon(resourcePath+"actions/debug.png"), "Rebuild All", self)
		buildToolbar.addAction(rebuildAction)
		buildMenu.addAction(rebuildAction)"""
		enigmaPluginAction = QAction(QIcon(resourcePath+"actions/compile.png"), "Rebuild ENIGMA Compiler", self)
		enigmaPluginAction.triggered.connect(self.handleRebuildEnigmaPlugin)
		buildToolbar.addAction(enigmaPluginAction)
		buildMenu.addAction(enigmaPluginAction)
		self.addToolBar(buildToolbar)
		debugToolbar = QToolBar(self)
		contAction = QAction("Cont", self)
		contAction.triggered.connect(self.handleContAction)
		debugToolbar.addAction(contAction)
		debugMenu.addAction(contAction)
		pauseAction = QAction("Pause", self)
		pauseAction.triggered.connect(self.handlePauseAction)
		debugToolbar.addAction(pauseAction)
		debugMenu.addAction(pauseAction)
		stopAction = QAction("Stop", self)
		stopAction.triggered.connect(self.handleStopAction)
		debugToolbar.addAction(stopAction)
		debugMenu.addAction(stopAction)
		self.addToolBar(debugToolbar)
		"""resourceToolbar = QToolBar(self)
		spriteAction = QAction(QIcon(resourcePath+"resources/sprite.png"), "New Sprite", self)
		spriteAction.triggered.connect(self.actionNewSprite)
		resourceToolbar.addAction(spriteAction)
		soundAction = QAction(QIcon(resourcePath+"resources/sound.png"), "New Sound", self)
		resourceToolbar.addAction(soundAction)
		backgroundAction = QAction(QIcon(resourcePath+"resources/background.png"), "New Background", self)
		resourceToolbar.addAction(backgroundAction)
		pathAction = QAction(QIcon(resourcePath+"resources/path.png"), "New Path", self)
		resourceToolbar.addAction(pathAction)
		scriptAction = QAction(QIcon(resourcePath+"resources/script.png"), "New Script", self)
		scriptAction.triggered.connect(self.actionNewScript)
		resourceToolbar.addAction(scriptAction)
		shaderAction = QAction(QIcon(resourcePath+"resources/shader.png"), "New Shader", self)
		resourceToolbar.addAction(shaderAction)
		fontAction = QAction(QIcon(resourcePath+"resources/font.png"), "New Font", self)
		resourceToolbar.addAction(fontAction)
		timelineAction = QAction(QIcon(resourcePath+"resources/timeline.png"), "New Timeline", self)
		resourceToolbar.addAction(timelineAction)
		objectAction = QAction(QIcon(resourcePath+"resources/object.png"), "New Object", self)
		objectAction.triggered.connect(self.actionNewObject)
		resourceToolbar.addAction(objectAction)
		roomAction = QAction(QIcon(resourcePath+"resources/room.png"), "New Room", self)
		roomAction.triggered.connect(self.actionNewRoom)
		resourceToolbar.addAction(roomAction)
		self.addToolBar(resourceToolbar)"""
		"""settingsToolbar = QToolBar(self)
		settingsToolbar.addAction(preferencesAction)
		gameSettingsAction = QAction(QIcon(resourcePath+"resources/gm.png"), "Global Game Settings", self)
		gameSettingsAction.triggered.connect(self.actionShowGameSettings)
		settingsToolbar.addAction(gameSettingsAction)
		gameInformationAction = QAction(QIcon(resourcePath+"resources/info.png"), "Game Information", self)
		gameInformationAction.triggered.connect(self.actionShowGameInformation)
		settingsToolbar.addAction(gameInformationAction)
		extensionsAction = QAction(QIcon(resourcePath+"resources/extension.png"), "Extensions", self)
		settingsToolbar.addAction(extensionsAction)
		manualAction = QAction(QIcon(resourcePath+"actions/manual.png"), "Manual", self)
		settingsToolbar.addAction(manualAction)
		self.addToolBar(settingsToolbar)"""
		self.hierarchyDock = QDockWidget("Hierarchy", self)
		self.hierarchyTree = QTreeWidget(self)
		self.hierarchyTree.setContextMenuPolicy(Qt.CustomContextMenu)
		self.hierarchyTree.customContextMenuRequested.connect(self.handleContextMenu)
		#self.hierarchyTree.setContextMenuPolicy(Qt.ActionsContextMenu)
		#self.hierarchyTree.addAction(self.aboutAction)
		self.hierarchyTree.itemActivated.connect(self.handleItemActivated)
		self.hierarchyTree.header().setVisible(False)
		self.hierarchyTree.setIconSize(QSize(18, 18))
		self.hierarchyDock.setWidget(self.hierarchyTree)
		self.hierarchyDock.setMaximumWidth(200)#160
		#self.hierarchyDock.setFeatures(QDockWidget.NoDockWidgetFeatures)
		self.addDockWidget(Qt.LeftDockWidgetArea, self.hierarchyDock)
		windowMenu.addAction(self.hierarchyDock.toggleViewAction())
		self.setCorner( Qt.TopLeftCorner, Qt.LeftDockWidgetArea )
		self.setCorner( Qt.TopRightCorner, Qt.RightDockWidgetArea )
		self.setCorner( Qt.BottomLeftCorner, Qt.LeftDockWidgetArea )
		self.setCorner( Qt.BottomRightCorner, Qt.RightDockWidgetArea )
		self.propertiesTable = PropertiesTable(self)
		self.propertiesTable.setColumnCount(2)
		self.propertiesTable.setRowCount(0)
		self.propertiesTable.mainwindow=self
		headers=[]
		headers.append("Name")
		headers.append("Value")
		self.propertiesTable.setHorizontalHeaderLabels(headers)
		self.propertiesTable.verticalHeader().setVisible(False)
		self.propertiesTable.horizontalHeader().resizeSection(0,150)
		#self.propertiesTable.setSortingEnabled(True)
		self.propertiesDock = QDockWidget("Properties", self)
		self.propertiesDock.setWidget(self.propertiesTable)
		self.addDockWidget(Qt.RightDockWidgetArea, self.propertiesDock)
		windowMenu.addAction(self.propertiesDock.toggleViewAction())
		self.logDock = QDockWidget("Log", self)
		self.logText = QTextEdit(self)
		self.logText.setReadOnly(True)
		self.logText.setMaximumHeight(100)
		self.logDock.setWidget(self.logText)
		#self.logDock.setFeatures(QDockWidget.NoDockWidgetFeatures)
		self.addDockWidget(Qt.BottomDockWidgetArea, self.logDock)
		windowMenu.addAction(self.logDock.toggleViewAction())
		#self.tabifyDockWidget(self.logDock, messagesDock)
		self.mainMdiArea = QMdiArea(self)
		# MDIArea's can bet set to tabs, interesting...
		self.mainMdiArea.setDocumentMode(True)
		self.mainMdiArea.setViewMode(QMdiArea.TabbedView)
		#self.mainMdiArea.setBackground(QBrush(QPixmap(resourcePath+"lgm1.png")))
		self.mainMdiArea.setTabsClosable(True)
		self.mainMdiArea.subWindowActivated.connect(self.handleSubWindowActivated)
		self.setCentralWidget(self.mainMdiArea)
		mainStatusBar = QStatusBar(self)
		self.setStatusBar(mainStatusBar)
		mainStatusBar.addWidget(QLabel("Ready"), 0)
		#mainProgressBar = QProgressBar()
		#mainProgressBar.setValue(75)
		#mainStatusBar.addWidget(mainProgressBar)
		self.setWindowIcon(QIcon(resourcePath+"lgm-logo.png"))
		self.projectUpdateWindowTitle()
		self.resize(1000, 600)
		self.showMaximized()
		self.aboutDialog = None
		self.handleNewAction()
		self.updateHierarchyTree()
		if CliClass.IfEnigmaDir():
			CliClass.print_notice("enigma installation found: "+self.enigmaPath)
		else:
			CliClass.print_error("enigma compiler library not found: "+self.enigmaPath)
			if self.enigmaPath==".":
				self.actionPreferences()
			runAction.setDisabled(True)
			debugAction.setDisabled(True)

	def loadPreferences(self):
		config = ConfigParser()
		#config.readfp(open('GameEditor.cfg'))
		config.read([os.path.join(CliClass.module_path(),"GameEditor.cfg"), os.path.expanduser("~/.GameEditor.cfg")])
		self.editorFontName = config.get('Editor', 'fontName')
		self.editorSize = int(config.get('Editor', 'size'))
		#self.editorFont=QFont("DejaVu Sans Mono", 8)#Courier 10 Pitch
		self.editorFont=QFont(self.editorFontName, self.editorSize)
		self.ideTheme=not int(config.get('Editor', 'theme'))
		self.enigmaPath = config.get('Editor', 'enigmadev')
		self.projectSavingEnabled = config.get('Editor', 'savingenabled') in ["True","2"]
		#CliClass.print_notice("changing directory to enigma-dev: "+self.enigmaPath)
		try:
			os.chdir(self.enigmaPath)
		except:
			CliClass.print_notice("error changing directory to enigma-dev: "+self.enigmaPath)
		self.switchTheme()
		for x,file in config.items("Recent"):
			self.recentFiles.append(file)
		for key,color in config.items("Colors"):
			self.colors[int(key)]=int(color,16)
		for key,color in config.items("ThemeColors"):
			self.themeColors[int(key)]=int(color,16)

	def savePreferences(self):
		config = ConfigParser()
		config.add_section('Recent')
		for x in self.recentFiles:
			config.set("Recent", str(x), str(x))
		config.add_section('Editor')
		config.set('Editor', 'savingenabled', str(self.projectSavingEnabled))
		config.set('Editor', 'enigmadev', str(self.enigmaPath))
		try:
			os.chdir(self.enigmaPath)
		except:
			CliClass.print_notice("error changing directory to enigma-dev: "+self.enigmaPath)
		config.set('Editor', 'theme', str(self.ideTheme))
		config.set('Editor', 'fontName', self.editorFontName)
		config.set('Editor', 'size', str(self.editorSize))
		#config.set('Editor', 'showLineNumbers', True)
		#config.set('Editor', '', '')
		config.add_section('Colors')
		for key in self.colors:
			hexcolor=__builtins__.hex(int(self.colors[key]))
			if hexcolor[-1]=="L":
				hexcolor=hexcolor[:-1]
			config.set('Colors', str(key), hexcolor)
		config.add_section('ThemeColors')
		for key in self.themeColors:
			hexcolor=__builtins__.hex(int(self.themeColors[key]))
			if hexcolor[-1]=="L":
				hexcolor=hexcolor[:-1]
			config.set('ThemeColors', str(key), hexcolor)
		config.write(open(os.path.expanduser("~/.GameEditor.cfg"),"w"))

	def handleGameStats(self, event):
		self.outputClear()
		self.gmk.printBasicStats()

	def handleBuildTypeListChanged(self, event):
		mode=self.buildTypeList.currentText()
		if mode=="Run":
			self.projectEmode=CliClass.emode_run
		elif mode=="Debug":#emode_debug
			self.projectEmode=CliClass.emode_compile
		elif mode=="Design":
			self.projectEmode=CliClass.emode_design
		else:
			CliClass.print_error("unsupported emode "+mode)

	def handleBuildPlatformListChanged(self, event):
		platform=self.buildPlatformList.currentText()
		if platform=="Linux X11":
			self.gmk.EnigmaTargetAudio="OpenAL"
			self.gmk.EnigmaTargetWindowing="xlib"
			self.gmk.EnigmaTargetCompiler="gcc"
			#self.gmk.EnigmaTargetCompiler="clang"
			self.gmk.EnigmaTargetWidget="None"
			self.gmk.EnigmaTargetCollision="BBox"
		elif platform=="Windows":
			self.gmk.EnigmaTargetAudio="OpenAL"
			#self.gmk.EnigmaTargetAudio="DirectSound"
			#self.gmk.EnigmaTargetAudio="FMODAudio"
			self.gmk.EnigmaTargetWindowing="Win32"
			self.gmk.EnigmaTargetCompiler="gcc"
			self.gmk.EnigmaTargetWidget="Win32"
			self.gmk.EnigmaTargetCollision="Precise"
		elif platform=="Windows mingw32":
			self.gmk.EnigmaTargetAudio="OpenAL"
			self.gmk.EnigmaTargetWindowing="Win32"
			self.gmk.EnigmaTargetCompiler="i686-w64-mingw32-gcc"#x86_64-w64-mingw32-gcc
			self.gmk.EnigmaTargetWidget="Win32"
			self.gmk.EnigmaTargetCollision="BBox"
		elif platform=="Android":
			self.gmk.EnigmaTargetAudio="AndroidAudio"
			self.gmk.EnigmaTargetWindowing="Android"
			self.gmk.EnigmaTargetCompiler="Linux/Android"
			self.gmk.EnigmaTargetGraphics="OpenGLES"
			self.gmk.EnigmaTargetWidget="None"
			self.gmk.EnigmaTargetCollision="BBox"
		else:
			CliClass.print_error("unsupported target platform "+platform)

	def handleBuildGraphicsListChanged(self, event):
		graphics=self.buildGraphicsList.currentText()
		if graphics=="OpenGL 1.1":
			self.gmk.EnigmaTargetGraphics="OpenGL1"
		elif graphics=="OpenGL 3.0":
			self.gmk.EnigmaTargetGraphics="OpenGL3"
		elif graphics=="Direct3D 9.0":
			self.gmk.EnigmaTargetGraphics="Direct3D9"
		elif graphics=="OpenGLES":
			self.gmk.EnigmaTargetGraphics="OpenGLES"
		else:
			CliClass.print_error("unsupported target graphics "+graphics)

	def handleContextMenu(self, aPosition):
		item = self.hierarchyTree.itemAt(aPosition)
		if item:
			if item.res:
				menu=QMenu(self)
				openAction = QAction("Open", menu)
				openAction.triggered.connect(lambda x:self.openTreeResource(item))
				menu.addAction(openAction)
				openWindowAction = QAction("Open Window", menu)
				openWindowAction.triggered.connect(lambda x:self.openWindowTreeResource(item))
				menu.addAction(openWindowAction)
				openGGGWindowAction = QAction("Open GGG", menu)
				openGGGWindowAction.triggered.connect(lambda x:self.openGGGWindowTreeResource(item))
				menu.addAction(openGGGWindowAction)
				renameAction = QAction("Rename", menu)
				renameAction.triggered.connect(lambda x:self.renameTreeResource(item))
				menu.addAction(renameAction)
				deleteAction = QAction("Delete", menu)
				deleteAction.triggered.connect(lambda x:self.deleteTreeResource(item))
				menu.addAction(deleteAction)
				aPosition.setX(aPosition.x()+20)
				aPosition.setY(aPosition.y()+80)
				menu.popup(self.mapToGlobal(aPosition))
			else:
				menu=QMenu(self)
				newAction = QAction("New Resource", menu)
				newAction.triggered.connect(lambda x:self.newTreeResource(item))
				menu.addAction(newAction)
				newGroupAction = QAction("New Group", menu)
				newGroupAction.triggered.connect(lambda x:self.newTreeGroup(item))
				menu.addAction(newGroupAction)
				renameAction = QAction("Rename", menu)
				renameAction.triggered.connect(lambda x:self.renameTreeGroup(item))
				menu.addAction(renameAction)
				deleteAction = QAction("Delete", menu)
				deleteAction.triggered.connect(lambda x:self.deleteTreeGroup(item))
				menu.addAction(deleteAction)
				aPosition.setX(aPosition.x()+20)
				aPosition.setY(aPosition.y()+80)
				menu.popup(self.mapToGlobal(aPosition))

	def deleteTreeResource(self, item):
		if item.res:
			self.gmk.DeleteResource(item.res)
			for w in self.mainMdiArea.subWindowList():
				if w.res==item.res:
					w.close()
					#self.mainMdiArea.setActiveSubWindow(w)
					return
		self.updateHierarchyTree()

	def newTreeResource(self, item):
		group=item.text(0)
		if group=="Sprites":
			id=self.gmk.GetResourceHighestId(CliClass.GameSprite)
			s=CliClass.GameSprite(self.gmk,id+1)
			self.gmk.sprites.append(s)
			self.gmk.resourceTree.AddResourcePath("Sprites/"+s.getMember("name"),s)
		elif group=="Sounds":
			id=self.gmk.GetResourceHighestId(CliClass.GameSound)
			s=CliClass.GameSound(self.gmk,id+1)
			self.gmk.sounds.append(s)
			self.gmk.resourceTree.AddResourcePath("Sounds/"+s.getMember("name"),s)
		elif group=="Backgrounds":
			id=self.gmk.GetResourceHighestId(CliClass.GameBackground)
			s=CliClass.GameBackground(self.gmk,id+1)
			self.gmk.backgrounds.append(s)
			self.gmk.resourceTree.AddResourcePath("Backgrounds/"+s.getMember("name"),s)
		elif group=="Paths":
			id=self.gmk.GetResourceHighestId(CliClass.GamePath)
			s=CliClass.GamePath(self.gmk,id+1)
			self.gmk.paths.append(s)
			self.gmk.resourceTree.AddResourcePath("Paths/"+s.getMember("name"),s)
		elif group=="Scripts":
			id=self.gmk.GetResourceHighestId(CliClass.GameScript)
			s=CliClass.GameScript(self.gmk,id+1)
			self.gmk.scripts.append(s)
			self.gmk.resourceTree.AddResourcePath("Scripts/"+s.getMember("name"),s)
		elif group=="Shaders":
			id=self.gmk.GetResourceHighestId(CliClass.GameShader)
			s=CliClass.GameShader(self.gmk,id+1)
			self.gmk.shaders.append(s)
			self.gmk.resourceTree.AddResourcePath("Shaders/"+s.getMember("name"),s)
		elif group=="Fonts":
			id=self.gmk.GetResourceHighestId(CliClass.GameFont)
			s=CliClass.GameFont(self.gmk,id+1)
			self.gmk.fonts.append(s)
			self.gmk.resourceTree.AddResourcePath("Fonts/"+s.getMember("name"),s)
		elif group=="Timelines":
			id=self.gmk.GetResourceHighestId(CliClass.GameTimeline)
			s=CliClass.GameTimeline(self.gmk,id+1)
			self.gmk.timelines.append(s)
			self.gmk.resourceTree.AddResourcePath("Timelines/"+s.getMember("name"),s)
		elif group=="Objects":
			id=self.gmk.GetResourceHighestId(CliClass.GameObject)
			s=CliClass.GameObject(self.gmk,id+1)
			self.gmk.objects.append(s)
			self.gmk.resourceTree.AddResourcePath("Objects/"+s.getMember("name"),s)
		elif group=="Rooms":
			id=self.gmk.GetResourceHighestId(CliClass.GameRoom)
			s=CliClass.GameRoom(self.gmk,id+1)
			self.gmk.rooms.append(s)
			self.gmk.resourceTree.AddResourcePath("Rooms/"+s.getMember("name"),s)
		self.updateHierarchyTree()
		i=self.findTreeItemRes(s)
		self.handleItemActivated(i,0)

	def findTreeItemRes(self, res):
		for c in range(self.hierarchyTree.topLevelItemCount()):
			i=self.hierarchyTree.topLevelItem(c)
			for c in range(i.childCount()):
				x=i.child(c)
				if x.res==res:
					return x
		return None

	def handleSubWindowActivated(self, window):
		if window:
			window.updatePropertiesTable()
			i=self.findTreeItemRes(window.res)
			if i:
				self.hierarchyTree.setCurrentItem(i)
				return
			#CliClass.print_warning("not found activate")

	def handleFind(self, event):
		if not self.findDialog:
			self.findDialog = FindDialog(self)
			#self.findDialog.findNext.connect(self.findNext)
		self.findDialog.show()
		self.findDialog.raise_()
		self.findDialog.activateWindow()

	def openTreeResource(self, event):
		self.handleItemActivated(self.hierarchyTree.currentItem(),0)

	def openWindowTreeResource(self, event):
		self.handleItemActivated(self.hierarchyTree.currentItem(),0,False,False)
		
	def openGGGWindowTreeResource(self, event):
		self.handleItemActivated(self.hierarchyTree.currentItem(),0,True)
		
	def renameTreeResource(self, event):
		CliClass.print_notice("rename tree resource using properties panel")
		msgBox=QMessageBox()
		msgBox.setText("Rename tree resource using properties panel")
		msgBox.exec_()
		
	def renameTreeGroup(self, event):
		CliClass.print_error("unsupported rename tree group")
	
	def deleteTreeGroup(self, event):
		CliClass.print_error("unsupported delete tree group")

	def handleItemActivated(self, item, column, GGG=False, parent=True):
		if not item.res:
			#CliClass.print_notice("no res "+str(item.res))
			return
		for w in self.mainMdiArea.subWindowList():
			if w.res==item.res:
				self.mainMdiArea.setActiveSubWindow(w)
				return
		if GGG:
			s = GGGWindow(self,item.res)
		elif item.res.__class__==CliClass.GameSprite:
			s = SpriteWindow(self,item.res)
			item.res.updateQIcon()
			self.updateHierarchyTree()
		elif item.res.__class__==CliClass.GameSound:
			s = SoundWindow(self,item.res)
		elif item.res.__class__==CliClass.GameBackground:
			s = BackgroundWindow(self,item.res)
		elif item.res.__class__==CliClass.GamePath:
			s = PathWindow(self,item.res)
		elif item.res.__class__==CliClass.GameScript:
			s = ScriptWindow(self,item.res)
		elif item.res.__class__==CliClass.GameShader:
			s = ShaderWindow(self,item.res)
		elif item.res.__class__==CliClass.GameFont:
			s = FontWindow(self,item.res)
		elif item.res.__class__==CliClass.GameTimeline:
			s = TimelineWindow(self,item.res)
		elif item.res.__class__==CliClass.GameObject:
			s = ObjectWindow(self,item.res)
		elif item.res.__class__==CliClass.GameRoom:
			s = RoomWindow(self,item.res)
		elif item.res.__class__==CliClass.GameInformation:
			s = GameInformationWindow(self,item.res)
		elif item.res.__class__==CliClass.GameSettings:
			s = GameSettingsWindow(self,item.res)
		else:
			CliClass.print_notice("unsupported class "+str(item.res))
			return
		self.mainMdiArea.addSubWindow(s, Qt.Window)
		if not parent:
			self.mainMdiArea.removeSubWindow(s)
			s.show()
			return
		s.showMaximized()

	def saveOpenResources(self):
		for w in self.mainMdiArea.subWindowList():
			w.saveResource()

	def projectUpdateWindowTitle(self):
		self.setWindowTitle("GameEditor - " + self.projectTitle+" "+["","*"][self.projectModified])

	def projectSetModified(self,m):
		self.projectModified = m
		self.projectUpdateWindowTitle()

	def updateHierarchyTreeRecursive(self, treeItemRoot, treeNode, resIcon, root=False):
		if treeNode.status==CliClass.GameTree.StatusSecondary:
			treeItem = QTreeWidgetItem(treeItemRoot,[treeNode.name])
			if root:
				if treeNode.name=="Game Information":
					q=QIcon(resourcePath+"resources/info.png")
				elif treeNode.name=="Global Game Settings":
					q=QIcon(resourcePath+"resources/gm.png")
				elif treeNode.name=="Extensions":
					q=QIcon(resourcePath+"resources/extension.png")
				else:
					q=QIcon(resourcePath+"resources/script.png")
			else:
				q=resIcon
			if treeNode.group==CliClass.GameTree.GroupSprites:
				q=treeNode.resource.getQIcon()
			if treeNode.group==CliClass.GameTree.GroupObjects:
				sprite=treeNode.resource.getMember("sprite")
				if sprite:
					q=sprite.getQIcon()
			if not q:
				q=resIcon
			treeItem.setIcon(0, q)
			treeItem.res=treeNode.resource
			if not treeItem.res:
				if treeNode.name=="Game Information":
					treeItem.res=self.gmk.gameInformation
				elif treeNode.name=="Global Game Settings":
					treeItem.res=self.gmk.settings
				#elif treeNode.name=="Extensions":
				#	treeItem.res=
				#else:
				#	CliClass.print_warning("no resource for "+treeNode.name)
		else:
			if root:
				if treeNode.name=="Triggers":
					resIcon=QIcon(resourcePath+"resources/script.png")
				elif treeNode.name=="Constants":
					resIcon=QIcon(resourcePath+"resources/script.png")
				elif treeNode.name=="Sounds":
					resIcon=QIcon(resourcePath+"resources/sound.png")
				elif treeNode.name=="Sprites":
					resIcon=QIcon(resourcePath+"resources/sprite.png")
				elif treeNode.name=="Backgrounds":
					resIcon=QIcon(resourcePath+"resources/background.png")
				elif treeNode.name=="Paths":
					resIcon=QIcon(resourcePath+"resources/path.png")
				elif treeNode.name=="Scripts":
					resIcon=QIcon(resourcePath+"resources/script.png")
				elif treeNode.name=="Shaders":
					resIcon=QIcon(resourcePath+"resources/shader.png")
				elif treeNode.name=="Fonts":
					resIcon=QIcon(resourcePath+"resources/font.png")
				elif treeNode.name=="Timelines":
					resIcon=QIcon(resourcePath+"resources/timeline.png")
				elif treeNode.name=="Objects":
					resIcon=QIcon(resourcePath+"resources/object.png")
				elif treeNode.name=="Rooms":
					resIcon=QIcon(resourcePath+"resources/room.png")
				else:
					resIcon=QIcon(resourcePath+"resources/script.png")
			treeItem = QTreeWidgetItem(treeItemRoot,[treeNode.name])
			treeItem.res=None
			treeItem.setIcon(0, QIcon(resourcePath+"resources/group.png"))
			if root:
				treeItem.setExpanded(True)
			for treeNodeChild in treeNode.contents:
				self.updateHierarchyTreeRecursive(treeItem, treeNodeChild, resIcon)

	def updateHierarchyTree(self):
		self.hierarchyTree.clear()
		if self.gmk.resourceTree!=None:
			for treeNode in self.gmk.resourceTree.contents:
				self.updateHierarchyTreeRecursive(self.hierarchyTree, treeNode, None, True)

	def addResourceToGroup(self, groupName, res, icon):
		if type(res)==tuple:
			resName=res[0]
		else:
			resName=res.getMember("name")
		for c in range(self.hierarchyTree.topLevelItemCount()):
			i=self.hierarchyTree.topLevelItem(c)
			if i.text(0)==groupName:
				treeItem = QTreeWidgetItem(i,[resName])
				treeItem.res=res
				treeItem.setIcon(0, icon)
				return
		#clifix missing resource group
		treeItem = QTreeWidgetItem(self.hierarchyTree,[groupName])
		treeItem.res=None
		treeItem.setIcon(0, QIcon(resourcePath+"resources/group.png"))
		treeItem.setExpanded(True)
		treeItem = QTreeWidgetItem(treeItem,[resName])
		treeItem.res=res
		treeItem.setIcon(0, icon)

	def switchTheme(self):
		if self.ideTheme:
			self.ideTheme=0
			self.app.setStyleSheet(open(stylePath+"default.css").read())
		else:
			self.ideTheme=1
			self.app.setStyleSheet(open(stylePath+"dark.css").read())

	def handleRebuildEnigmaPlugin(self):
		CliClass.print_notice("Rebuilding ENIGMA running make")
		self.gameProcessGdb=False
		self.gameProcess = QProcess()
		self.gameProcess.start("make")
		self.gameProcess.setProcessChannelMode(QProcess.MergedChannels)
		self.gameProcess.readyRead.connect(self.handleProcessOutput)
		self.gameProcess.readyReadStandardError.connect(self.handleProcessErrorOutput)
		self.gameProcess.error.connect(self.handleProcessError)
		self.gameProcess.finished.connect(self.handleProcessFinished)

	def handleRunAction(self):
		self.saveOpenResources()
		#es=self.gmk.WriteES()
		if self.projectLoadPluginLib==False:
			def ede_output_redirect_file(filepath):
				redir=open(filepath.decode()).read()
				CliClass.print_error(redir)
			def ede_dia_progress(progress):
				self.setCompileProgress(progress)
				#self.progressSignal.emit(progress)
			CliClass.ede_output_redirect_file=ede_output_redirect_file
			#CliClass.ede_dia_progress=ede_dia_progress
			CliClass.LoadPluginLib()
			self.projectLoadPluginLib=True

		class AThread(QtCore.QThread):
			outputSignal = pyqtSignal(str, name = 'stepIncreased')
			progressSignal = pyqtSignal(int, name = 'progressSignal')

			def run(self):
				CliClass.print_error=self.outputLine
				CliClass.print_warning=self.outputLine
				CliClass.print_notice=self.outputLine

				self.mainwindow.gmk.compileRunEnigma(CliClass.tmpDir+"testgame.exe",self.mainwindow.projectEmode)
				if self.mainwindow.projectEmode == CliClass.emode_compile:#emode_debug
					self.mainwindow.gameProcessGdb=False
					self.gameProcess = QProcess()
					self.gameProcess.start(CliClass.tmpDir+"testgame.exe")
					self.gameProcess.readyReadStandardOutput.connect(self.handleProcessOutput)
					self.gameProcess.readyReadStandardError.connect(self.handleProcessErrorOutput)
					#self.mainwindow.gameProcess.finished.connect(self.mainwindow.handleProcessFinished)

			def outputLine(self, text):
				self.outputSignal.emit(text)

			def handleProcessErrorOutput(self):
				self.gameProcess.setReadChannel(QProcess.StandardError)
				while 1:
					s=self.gameProcess.read(600)
					CliClass.print_notice(str(s))
					if s=="":
						return
					for l in s.split("\n"):
						if l != "":
							self.outputLine(l)

			def handleProcessOutput(self):
				self.gameProcess.setReadChannel(QProcess.StandardOutput)
				while 1:
					s=self.gameProcess.read(600).decode()
					CliClass.print_notice(str(s))
					if s=="":
						return
					for l in s.split("\n"):
						if l != "":
							self.outputLine(l)
						if self.gameProcessGdb and l=="(gdb) ":
							if len(self.debuggerCommands)>0:
								c=self.debuggerCommands.pop()
								self.gameProcess.write(c+"\n")
								self.outputLine(c)

		global thread
		thread = AThread()
		thread.outputSignal.connect(self.outputLine)
		thread.progressSignal.connect(self.setCompileProgress)
		thread.mainwindow=self
		#thread.finished.connect(app.exit)
		thread.start()

	def handleDebugAction(self):
		self.gameProcessGdb=True
		self.gameProcess = QProcess()
		self.gameProcess.start("gdb "+CliClass.tmpDir+"testgame.exe")
		self.gameProcess.setProcessChannelMode(QProcess.MergedChannels)
		#self.gameProcess.start(CliClass.tmpDir+"testgame.exe")
		self.debuggerCommands=["b main","run"]
		self.debuggerCommands.reverse()
		self.gameProcess.readyRead.connect(self.handleProcessOutput)
		self.gameProcess.readyReadStandardError.connect(self.handleProcessErrorOutput)
		self.gameProcess.error.connect(self.handleProcessError)
		self.gameProcess.finished.connect(self.handleProcessFinished)
		
	def handleContAction(self):
		self.outputText("c")
		self.gameProcess.write("c\n")
		pass

	def handlePauseAction(self):
		#clifix get child
		p=self.gameProcess.pid()
		os.kill(p,2)

	def handleStopAction(self):
		self.outputText("quit")
		self.gameProcess.write("quit\n")

	def handleProcessError(self,error):
		self.outputLine("Error "+str(error))

	def handleProcessFinished(self,exit):
		self.outputLine("Finished "+str(exit))

	def handleProcessErrorOutput(self):
		self.gameProcess.setReadChannel(QProcess.StandardError)
		while 1:
			s=self.gameProcess.read(600)
			CliClass.print_notice(str(s))
			if s=="":
				return
			for l in s.split("\n"):
				if l != "":
					self.outputLine(l)

	def handleProcessOutput(self):
		self.gameProcess.setReadChannel(QProcess.StandardOutput)
		while 1:
			s=self.gameProcess.read(600).decode()
			CliClass.print_notice(str(s))
			if s=="":
				return
			for l in s.split("\n"):
				if l != "":
					self.outputLine(l)
				if self.gameProcessGdb and l=="(gdb) ":
					if len(self.debuggerCommands)>0:
						c=self.debuggerCommands.pop()
						self.gameProcess.write(c+"\n")
						self.outputLine(c)

	def setCompileProgress(self, progress):
		self.setWindowTitle("GameEditor - " + self.projectTitle+" "+["","*"][self.projectModified]+str(progress)+"%")
		#if progress==100:
		#	self.projectUpdateWindowTitle()

	def actionPreferences(self):
		#if not self.prefsDialog:
		self.prefsDialog=PreferencesDialog(self)
		self.prefsDialog.show()
		self.prefsDialog.raise_()
		self.prefsDialog.activateWindow()

	def actionNewSprite(self):
		pass

	def actionNewScript(self):
		pass

	def actionNewObject(self):
		pass

	def actionNewRoom(self):
		pass

	def actionShowGameSettings(self):
		pass

	def actionShowGameInformation(self):
		pass

	def handleNewAction(self):
		self.gmk = CliClass.GameFile()
		self.gmk.app=self.app
		self.gmk.resourceTree=CliClass.GameTree(self.gmk)
		self.gmk.resourceTree.NewTree()
		self.gmk.newSettings()
		self.gmk.newGameInformation()
		self.projectTitle="<new game>"
		self.projectUpdateWindowTitle()
		self.updateHierarchyTree()

	def openProject(self,fileName):
		self.recentFiles.append(fileName)
		self.savePreferences()
		fileName=str(fileName)
		self.gmk = CliClass.GameFile()
		self.gmk.app=self.app
		self.gmk.Read(fileName)
		self.projectSetModified(False)
		self.projectTitle=os.path.split(fileName)[1]
		self.projectUpdateWindowTitle()
		self.updateHierarchyTree()
		self.startBackgroundThread()

	def startBackgroundThread(self):
		global backgroundThread
		backgroundThread = SpriteQIconUpdateThread()
		backgroundThread.outputSignal.connect(self.backgroundSignal)
		backgroundThread.mainwindow=self
		#thread.finished.connect(app.exit)
		backgroundThread.start()

	def backgroundSignal(self, s):
		#s.updateQIcon()
		#CliClass.print_warning("background signal")
		self.updateHierarchyTree()

	def handleOpenAction(self):
		projectPath = QFileDialog.getOpenFileName(self,"Open", "", "Game Files (*.gmk *.gm81 *.gm6 *.egm *.gmx)")
		if projectPath and projectPath!="":
			self.projectPath=projectPath
			CliClass.print_notice("opening file "+self.projectPath)
			self.openProject(self.projectPath)

	def handleRevertAction(self):
		if self.projectPath and self.projectPath!="":
			CliClass.print_notice("opening file "+self.projectPath)
			self.openProject(self.projectPath)

	def handleSaveAction(self):
		self.saveOpenResources()
		if not self.projectSavingEnabled:
			CliClass.print_warning("saving not enabled")
			self.actionPreferences()
			return
		if self.projectPath and self.projectPath!="":
			#reply = QMessageBox::question(this, "save", MESSAGE, QMessageBox::Yes | QMessageBox::No | QMessageBox::Cancel);
			#if reply == QMessageBox::Yes:
			#elif reply == QMessageBox::No:
			CliClass.print_notice("saving file "+self.projectPath)
			self.gmk.Save(os.path.splitext(self.projectPath)[1], self.projectPath)
			self.projectSetModified(False)
		else:
			self.handleSaveAsAction()

	def handleSaveAsAction(self):
		self.saveOpenResources()
		if not self.projectSavingEnabled:
			CliClass.print_error("saving not enabled")
			self.actionPreferences()
			return
		projectPath = QFileDialog.getSaveFileName(self,"Save", "", "Game Files (*.gmk *.gm81 *.gm6 *.egm *.gmx)")
		if projectPath and projectPath!="":
			self.projectPath=projectPath
			CliClass.print_notice("saving file "+self.projectPath)
			self.gmk.Save(os.path.splitext(self.projectPath)[1], self.projectPath)
			self.projectSetModified(False)

	def handleCloseApplication(self):
		self.savePreferences()
		self.saveOpenResources()
		if self.projectModified:
			CliClass.print_notice("close modified")
		self.close()

	def handleShowLicenseDialog(self):
		if self.aboutDialog == None:
			self.aboutDialog = AboutDialog()
		self.aboutDialog.show(":/license.html", "License")

	def handleShowAboutDialog(self):
		if self.aboutDialog == None:
			self.aboutDialog = AboutDialog()
		self.aboutDialog.show(":/about.html", "About");

	#def handleToggleMdiTabs(self):
	#	self.mainMdiArea.setDocumentMode(True);
	#	if self.mainMdiArea.viewMode()==QMdiArea.TabbedView:
	#		self.mainMdiArea.setViewMode(QMdiArea.SubWindowView)
	#	if self.mainMdiArea.viewMode()==QMdiArea.SubWindowView:
	#		self.mainMdiArea.setViewMode(QMdiArea.TabbedView)

	def outputClear(self):
		self.logText.clear()

	def outputText(self, text):
		self.logText.insertPlainText(text)

	def outputLine(self, text):
		self.logText.append(text)

	#def outputMessage(self, origin, location, description):
	#	ind = self.messagesTable.rowCount()
	#	self.messagesTable.insertRow(ind)
	#	self.messagesTable.setItem(ind, 0, QTableWidgetItem(QString.number(ind)))
	#	self.messagesTable.setItem(ind, 1, QTableWidgetItem(origin))
	#	self.messagesTable.setItem(ind, 2, QTableWidgetItem(location))
	#	self.messagesTable.setItem(ind, 3, QTableWidgetItem(description))

	def addResourceGroup(self, name):
		treeItem = QTreeWidgetItem(self.hierarchyTree,[name])
		treeItem.res=None
		treeItem.setIcon(0, QIcon(resourcePath+"resources/group.png"))
		treeItem.setExpanded(True)
	def addResource(self, name, icon):
		treeItem = QTreeWidgetItem(self.hierarchyTree,[name])
		treeItem.setIcon(0, icon)
		treeItem.res=None

import traceback
import io

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	app.setStyleSheet(" QTabBar::tab { height: 16; icon-size: 18px; } QStatusBar::item { border: 0px solid black; }");
	errorMessageDialog=QErrorMessage()
	def my_excepthook(type, value, tback):
		s=io.StringIO()
		traceback.print_last(file=s)
		s.seek(0)
		errorMessageDialog.showMessage("exception\n"+s.read())

		# then call the default handler
		sys.__excepthook__(type, value, tback) 

	sys.excepthook = my_excepthook
	window = MainWindow(app)
	window.show()
	#if os.name=="nt":
	#	CliClass.redirectStdout()
	#	CliClass.setRealStdout(CliClass.realStdout)
	if len(sys.argv)>1:
		if sys.argv[1]!="":
			window.openProject(sys.argv[1])
	sys.exit(app.exec_())
