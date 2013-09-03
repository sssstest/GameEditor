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
import CliClass
from IdeRoomEditor import *
from IdeSciLexer import *
 
resourcePath="GameEditor/ideicons/"

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


class ResourceWindow(QtGui.QMdiSubWindow):
	def __init__(self, mainwindow, res):
		QtGui.QMdiSubWindow.__init__(self)
		self.mainwindow=mainwindow
		self.res=res
		self.setWindowTitle(res.getMember("name"))
		n=QLabel("Properties panel")
		self.setWidget(n)
		self.propertiesList=[]

	def saveResource(self):
		CliClass.print_warning("save resource unsupported "+str(self.res))

	def closeEvent(self, closeEvent):
		self.mainwindow.propertiesTable.updatedTable=False
		self.mainwindow.propertiesTable.res=None
		self.mainwindow.propertiesTable.clearContents()
		self.mainwindow.propertiesTable.setRowCount(1)
		self.hide()
		closeEvent.accept()
		a=self.mdiArea()
		a.removeSubWindow(self)#clifix stop showing in window list
		w=a.activeSubWindow()
		if w:
			w.showMaximized()

	def updatePropertiesTable(self):
		self.mainwindow.propertiesTable.updatedTable=False
		font=QFont("Helvetica", 10)
		fontbold=QFont("Helvetica", 10, QFont.Bold)
		fontitalic=QFont("Helvetica", 10)
		fontitalic.setItalic(True)
		self.mainwindow.propertiesTable.setSortingEnabled(False)
		self.mainwindow.propertiesTable.clearContents()
		self.mainwindow.propertiesTable.setRowCount(1)
		if self.propertiesList:
			propertiesList=self.propertiesList
		else:
			propertiesList=self.res.members
		for m in propertiesList:
			r=self.res.getMember(m)
			types = [str,int,float]
			if sys.version_info[0]<3:
				types.append(unicode)
			if type(r) not in types or (type(r)==str and r.count("\n")>0):
				CliClass.print_warning("not inserting property "+m+" "+str(type(r)))
				continue
			ind=self.mainwindow.propertiesTable.rowCount()-1
			self.mainwindow.propertiesTable.insertRow(ind)
			item=QTableWidgetItem(m)
			item.setFlags(Qt.ItemIsEnabled)
			if self.res.ifDefault(m):
				item.setFont(fontitalic)
			else:
				item.setFont(fontbold)
			self.mainwindow.propertiesTable.setItem(ind, 0, item)
			if type(r)==bool:
				item=QTableWidgetItem()
				item.setFlags(Qt.ItemIsSelectable|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled)#|Qt.ItemIsTristateQt.ItemIsEditable|
				item.setCheckState(Qt.Unchecked)
				if r:
					item.setCheckState(Qt.Checked)
			else:
				item=QTableWidgetItem(str(r))
				item.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEditable|Qt.ItemIsEnabled)
			item.setFont(font)
			self.mainwindow.propertiesTable.setItem(ind, 1, item)
		self.mainwindow.propertiesTable.resizeRowsToContents()
		self.mainwindow.propertiesTable.res=self.res
		self.mainwindow.propertiesTable.subwindow=self
		self.mainwindow.propertiesTable.updatedTable=True

class EditorWindow(ResourceWindow):
	def initEditor(self):
		self.sciEditor = QsciScintilla(self)
		self.sciEditor.setFrameStyle(QsciScintilla.NoFrame)
		#self.sciEditor.setWrapMode(QsciScintilla.WrapCharacter)
		self.sciEditor.setCaretLineVisible(True)
		font = QFont("Courier 10 Pitch", 10)
		font.setFixedPitch(True)
		self.sciEditor.setFont(font)
		lexer = LexerGame(self.mainwindow)
		lexer.setFont(font)
		self.sciEditor.setLexer(lexer)
		fontmetrics = QFontMetrics(font)
		self.sciEditor.setMarginWidth(0, fontmetrics.width("__")+8)
		self.sciEditor.setMarginLineNumbers(0, True)
		self.sciEditor.setMarginSensitivity(1, True)
		self.BREAK_MARKER_NUM = 8
		#self.setMarginWidth()
		self.sciEditor.marginClicked.connect(self.handleMarginClicked)
		#connect(sciEditor,SIGNAL(marginClicked(int, int, Qt.KeyboardModifiers)), self,SLOT(on_margin_clicked(int, int, Qt.KeyboardModifiers)))
		self.sciEditor.markerDefine(QImage(resourcePath+"actions/link_break.png"),self.BREAK_MARKER_NUM);
		self.sciEditor.setBraceMatching(QsciScintilla.SloppyBraceMatch)
		self.sciEditor.setFolding(QsciScintilla.BoxedTreeFoldStyle, 3)
		self.sciEditor.setMarginsFont(font)
		if self.mainwindow.ideTheme==1:
			self.sciEditor.setMarginsForegroundColor(QColor("#bbbbbb"))
			self.sciEditor.setCaretLineBackgroundColor(QColor("#333333"))
			self.sciEditor.setMarginsBackgroundColor(QColor("#222222"))
			self.sciEditor.setFoldMarginColors(QColor("#282828"), QColor("#282828"))
			lexer.setPaper(QColor("#222222"))
		else:
			self.sciEditor.setCaretLineBackgroundColor(QColor("#ffe4e4"))
			self.sciEditor.setMarginsBackgroundColor(QColor("#dddddd"))
			self.sciEditor.setFoldMarginColors(QColor("#dddddd"), QColor("#dddddd"))
			lexer.setPaper(QColor("#ffffff"))
		#setIndentationWidth
		self.sciEditor.setTabWidth(2)
		self.sciEditor.SendScintilla(QsciScintillaBase.SCI_SETMULTIPASTE,1)
		q=QWidget()
		self.setWidget(q)
		layout = QVBoxLayout(q)
		layout.addWidget(self.sciEditor)
		layout.setContentsMargins(0, 0, 0, 0)
		q.setLayout(layout)
		# sciEditor.setFixedHeight(300);

	def __init__(self, mainwindow, res):
		ResourceWindow.__init__(self, mainwindow, res)
		self.initEditor()

	def closeEvent(self, closeEvent):
		ResourceWindow.closeEvent(self, closeEvent)

	def handleMarginClicked(self, nmargin, nline, modifiers):
		# Toggle marker for the line the margin was clicked on
		if self.sciEditor.markersAtLine(nline) != 0:
			self.sciEditor.markerDelete(nline, self.BREAK_MARKER_NUM)
		else:
			self.sciEditor.markerAdd(nline, self.BREAK_MARKER_NUM)

class SpriteWindow(ResourceWindow):
	def __init__(self, mainwindow, res):
		ResourceWindow.__init__(self, mainwindow, res)
		self.setWindowIcon(QIcon(resourcePath+"resources/sprite.png"))
		imageLabel = QLabel()
		p=QPixmap()
		if len(res.subimages)>0:
			p.convertFromImage(res.subimages[0].getQImage())
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
		layout = QVBoxLayout(q) # no initialization here
		layout.addWidget(scrollArea) # layout is uninitialized and probably garbage
		layout.setContentsMargins(0, 0, 0, 0)
		q.setLayout(layout)

class SoundWindow(ResourceWindow):
	def __init__(self, mainwindow, res):
		ResourceWindow.__init__(self, mainwindow, res)
		self.setWindowIcon(QIcon(resourcePath+"resources/sprite.png"))

class BackgroundWindow(ResourceWindow):
	def __init__(self, mainwindow, res):
		ResourceWindow.__init__(self, mainwindow, res)
		self.setWindowIcon(QIcon(resourcePath+"resources/sprite.png"))

class PathWindow(ResourceWindow):
	def __init__(self, mainwindow, res):
		ResourceWindow.__init__(self, mainwindow, res)
		self.setWindowIcon(QIcon(resourcePath+"resources/sprite.png"))

class ScriptWindow(EditorWindow):
	def __init__(self, mainwindow, res):
		EditorWindow.__init__(self, mainwindow, res)
		self.setWindowIcon(QIcon(resourcePath+"resources/script.png"))
		self.sciEditor.setText(res.getMember("value"))

	def saveResource(self):
		if self.sciEditor.isModified():
			self.mainwindow.projectSetModified(True)
			self.res.setMember("value",str(self.sciEditor.text()))

	def closeEvent(self, closeEvent):
		if self.sciEditor.isModified():
			self.mainwindow.projectSetModified(True)
			self.res.setMember("value",str(self.sciEditor.text()))
		EditorWindow.closeEvent(self, closeEvent)

class ShaderWindow(EditorWindow):
	def __init__(self, mainwindow, res):
		EditorWindow.__init__(self, mainwindow, res)
		self.setWindowIcon(QIcon(resourcePath+"resources/sprite.png"))
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

class FontWindow(ResourceWindow):
	def __init__(self, mainwindow, res):
		ResourceWindow.__init__(self, mainwindow, res)
		self.setWindowIcon(QIcon(resourcePath+"resources/sprite.png"))

class TimelineWindow(ResourceWindow):
	def __init__(self, mainwindow, res):
		ResourceWindow.__init__(self, mainwindow, res)
		self.setWindowIcon(QIcon(resourcePath+"resources/sprite.png"))

class ObjectWindow(EditorWindow):
	def __init__(self, mainwindow, res):
		EditorWindow.__init__(self, mainwindow, res)
		self.setWindowIcon(QIcon(resourcePath+"resources/object.png"))
		ggg=res.WriteGGG(False)
		self.sciEditor.setText(ggg)

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
				self.res.ReadGGG(str(self.sciEditor.text()))
			except NotImplementedError:
				CliClass.print_warning("unsupported")
				closeEvent.ignore()
				return
			#except:
			#	closeEvent.ignore()
			#	return
		EditorWindow.closeEvent(self,closeEvent)

class RoomWindow(ResourceWindow):
	def __init__(self, mainwindow, res):
		ResourceWindow.__init__(self, mainwindow, res)
		self.setWindowIcon(QIcon(resourcePath+"resources/room.png"))
		self.propertiesList=["name","id","caption","width","height","speed","persistent","clearViewBackground","color","code",
		"rememberRoomEditorInfo","roomEditorWidth","roomEditorHeight","showGrid",
		"showObjects","showTiles","showBackgrounds","showForegrounds","showViews",
		"deleteUnderlyingObj","deleteUnderlyingTiles","page","hsnap","vsnap","isometric",
		"bgFlags","showcolor","enableViews","xoffset","yoffset",
		"PhysicsWorld","PhysicsWorldTop","PhysicsWorldLeft","PhysicsWorldRight","PhysicsWorldBottom","PhysicsWorldGravityX",
		"PhysicsWorldGravityY","PhysicsWorldGravityY","PhysicsWorldPixToMeters"]
		self.app=app
		splitter = QSplitter(self)
		q=QWidget(splitter)
		splitter.addWidget(q)
		layout = QVBoxLayout(q)
		self.tree=QTreeWidget(q)
		self.tree.header().setVisible(False)
		self.tree.itemSelectionChanged.connect(self.handleItemSelectionChanged)
		layout.addWidget(self.tree)

		q2=QWidget(q)
		layout2 = QHBoxLayout(q2)
		layout2.addWidget(QLabel("Add Object:"))
		self.shaderList=QComboBox(q)
		self.shaderList.addItem("obj")
		layout2.addWidget(self.shaderList)
		q2.setLayout(layout2)
		layout.addWidget(q2)

		layout.setContentsMargins(0, 0, 0, 0)
		q.setLayout(layout)
		self.scrollAreas = QScrollArea(splitter)
		self.updateTree()
		splitter.addWidget(self.scrollAreas)
		splitter.setSizes([self.width()*.25,self.width()*.75])
		self.setWidget(splitter)
		self.activeItem=None
		self.res.addListener(self.resListener)

	def resListener(self,type,member,value,val):
		self.updateTree()

	def keyReleaseEvent(self, event):
		QWidget.keyReleaseEvent(self, event)
		if event.matches(QKeySequence.Delete):
			item=self.tree.currentItem()
			if item:
				if type(item.res) == CliClass.GameRoomInstance:
					self.res.instances.remove(item.res)
			self.updateTree()

	def handleItemSelectionChanged(self):
		item=self.tree.selectedItems()
		if len(item)>0:
			self.activeItem=item[0].text(0)

	def updateTree(self):
		self.tree.clear()
		self.instancesItem = QTreeWidgetItem(self.tree,["Instances"])
		self.instancesItem.setIcon(0, QIcon(resourcePath+"resources/group.png"))
		self.instancesItem.setExpanded(True)
		self.instancesItem.res=None
		self.viewsItem = QTreeWidgetItem(self.tree,["Views"])
		self.viewsItem.setIcon(0, QIcon(resourcePath+"resources/group.png"))
		self.viewsItem.setExpanded(True)
		self.viewsItem.res=None
		self.backgroundsItem = QTreeWidgetItem(self.tree,["Backgrounds"])
		self.backgroundsItem.setIcon(0, QIcon(resourcePath+"resources/group.png"))
		self.backgroundsItem.setExpanded(True)
		self.backgroundsItem.res=None
		self.tilesItem = QTreeWidgetItem(self.tree,["Tiles"])
		self.tilesItem.setIcon(0, QIcon(resourcePath+"resources/group.png"))
		self.tilesItem.setExpanded(True)
		self.tilesItem.res=None
		for i in self.res.instances:
			if i.getMember("object"):
				name=i.getMember("object").getMember("name")
			else:
				name=""
			item = QTreeWidgetItem(self.instancesItem,[name,str(i.getMember("x"))+","+str(i.getMember("y"))])
			item.res=i
		for i in self.res.views:
			item = QTreeWidgetItem(self.viewsItem,[str(i.getMember("objectFollowingIndex"))])
			item.res=i
		for i in self.res.backgrounds:
			item = QTreeWidgetItem(self.backgroundsItem,[str(i.getMember("imageIndex"))])
			item.res=i
		for i in self.res.tiles:
			item = QTreeWidgetItem(self.tilesItem,[str(i.getMember("id")),str(i.getMember("backgroundIndex"))])
			item.res=i

		roomView=RoomView(self.scrollAreas, self.res, self)
		roomView.gridX=self.res.getMember("hsnap")
		roomView.gridY=self.res.getMember("vsnap")
		roomView.updateBrush()
		self.scrollAreas.setWidget(roomView)

class MainWindow(QtGui.QMainWindow):
	def __init__(self, app):
		QtGui.QMainWindow.__init__(self)
		self.app=app
		self.ideTheme=0
		self.projectModified=False
		self.projectTitle="noname"
		self.projectLoadPluginLib=False
		self.projectPath=None
		self.debuggerCommands=[]
		self.projectSavingEnabled=False
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
		viewMenu = QMenu("&View", self)
		#viewMenu.addAction(self.mdiAction)
		updAction = QAction("&Update", self)
		updAction.triggered.connect(self.updateHierarchyTree)
		viewMenu.addAction(updAction)
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
		"""designAction = QAction(QIcon(resourcePath+"actions/compile.png"), "Design", self)
		buildToolbar.addAction(designAction)
		buildMenu.addAction(designAction)
		compileAction = QAction(QIcon(resourcePath+"actions/compile.png"), "Compile", self)
		buildToolbar.addAction(compileAction)
		buildMenu.addAction(compileAction)
		rebuildAction = QAction(QIcon(resourcePath+"actions/debug.png"), "Rebuild All", self)
		buildToolbar.addAction(rebuildAction)
		buildMenu.addAction(rebuildAction)"""
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
		settingsToolbar = QToolBar(self)
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
		self.addToolBar(settingsToolbar)
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
				#openGGGWindowAction.triggered.connect(lambda x:self.openGGGWindowTreeResource(item))
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
			id=self.gmk.GetResourceHighestId(CliClass.GameFile.RtSprite)
			s=CliClass.GameSprite(self.gmk,id+1)
			self.gmk.sprites.append(s)
		elif group=="Sounds":
			id=self.gmk.GetResourceHighestId(CliClass.GameFile.RtSound)
			s=CliClass.GameSound(self.gmk,id+1)
			self.gmk.sounds.append(s)
		elif group=="Backgrounds":
			id=self.gmk.GetResourceHighestId(CliClass.GameFile.RtBackground)
			s=CliClass.GameBackground(self.gmk,id+1)
			self.gmk.backgrounds.append(s)
		elif group=="Paths":
			id=self.gmk.GetResourceHighestId(CliClass.GameFile.RtPath)
			s=CliClass.GamePath(self.gmk,id+1)
			self.gmk.paths.append(s)
		elif group=="Scripts":
			id=self.gmk.GetResourceHighestId(CliClass.GameFile.RtScript)
			s=CliClass.GameScript(self.gmk,id+1)
			self.gmk.scripts.append(s)
		elif group=="Shaders":
			id=self.gmk.GetResourceHighestId(CliClass.GameFile.RtShader)
			s=CliClass.GameShader(self.gmk,id+1)
			self.gmk.shaders.append(s)
		elif group=="Fonts":
			id=self.gmk.GetResourceHighestId(CliClass.GameFile.RtFont)
			s=CliClass.GameFont(self.gmk,id+1)
			self.gmk.fonts.append(s)
		elif group=="Timelines":
			id=self.gmk.GetResourceHighestId(CliClass.GameFile.RtTimeline)
			s=CliClass.GameTimeline(self.gmk,id+1)
			self.gmk.timelines.append(s)
		elif group=="Objects":
			id=self.gmk.GetResourceHighestId(CliClass.GameFile.RtObject)
			s=CliClass.GameObject(self.gmk,id+1)
			self.gmk.objects.append(s)
		elif group=="Rooms":
			id=self.gmk.GetResourceHighestId(CliClass.GameFile.RtRoom)
			s=CliClass.GameRoom(self.gmk,id+1)
			self.gmk.rooms.append(s)
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

	def handleSubWindowActivated(self,window):
		if window:
			window.updatePropertiesTable()
			i=self.findTreeItemRes(window.res)
			if i:
				self.hierarchyTree.setCurrentItem(i)
				return
			CliClass.print_warning("not found activate")

	def handleItemActivated(self, item, column):
		if not item.res:
			return
		for w in self.mainMdiArea.subWindowList():
			if w.res==item.res:
				self.mainMdiArea.setActiveSubWindow(w)
				return
		if item.res.__class__==CliClass.GameSprite:
			s = SpriteWindow(self,item.res)
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
		else:
			CliClass.print_notice("unsupported class "+str(item.res))
			return
		self.mainMdiArea.addSubWindow(s, Qt.Window)
		s.showMaximized()

	def saveOpenResources(self):
		for w in self.mainMdiArea.subWindowList():
			w.saveResource()

	def projectUpdateWindowTitle(self):
		self.setWindowTitle(self.projectTitle+" "+["","*"][self.projectModified]+" - GameEditor")

	def projectSetModified(self,m):
		self.projectModified = m
		self.projectUpdateWindowTitle()

	def updateHierarchyTree(self):
		self.hierarchyTree.clear()
		self.addResourceGroup("Sprites")
		self.addResourceGroup("Sounds")
		self.addResourceGroup("Backgrounds")
		self.addResourceGroup("Paths")
		self.addResourceGroup("Scripts")
		self.addResourceGroup("Shaders")
		self.addResourceGroup("Fonts")
		self.addResourceGroup("Timelines")
		self.addResourceGroup("Objects")
		self.addResourceGroup("Rooms")
		self.addResource("Game Information", QIcon(resourcePath+"resources/info.png"))
		self.addResource("Global Game Settings", QIcon(resourcePath+"resources/gm.png"))
		self.addResource("Extensions", QIcon(resourcePath+"resources/extension.png"))
		for t in self.gmk.triggers:
			self.addResourceToGroup("Triggers",t,QIcon(resourcePath+"resources/script.png"))
		for t in self.gmk.constants:
			self.addResourceToGroup("Constants",t,QIcon(resourcePath+"resources/script.png"))
		for t in self.gmk.sounds:
			self.addResourceToGroup("Sounds",t,QIcon(resourcePath+"resources/sound.png"))
		for t in self.gmk.sprites:
			self.addResourceToGroup("Sprites",t,QIcon(resourcePath+"resources/sprite.png"))
		for t in self.gmk.backgrounds:
			self.addResourceToGroup("Backgrounds",t,QIcon(resourcePath+"resources/background.png"))
		for t in self.gmk.paths:
			self.addResourceToGroup("Paths",t,QIcon(resourcePath+"resources/path.png"))
		for t in self.gmk.scripts:
			self.addResourceToGroup("Scripts",t,QIcon(resourcePath+"resources/script.png"))
		for t in self.gmk.shaders:
			self.addResourceToGroup("Shaders",t,QIcon(resourcePath+"resources/shader.png"))
		for t in self.gmk.fonts:
			self.addResourceToGroup("Fonts",t,QIcon(resourcePath+"resources/font.png"))
		for t in self.gmk.timelines:
			self.addResourceToGroup("Timelines",t,QIcon(resourcePath+"resources/timeline.png"))
		for t in self.gmk.objects:
			self.addResourceToGroup("Objects",t,QIcon(resourcePath+"resources/object.png"))
		for t in self.gmk.rooms:
			self.addResourceToGroup("Rooms",t,QIcon(resourcePath+"resources/room.png"))

	def addResourceToGroup(self,groupName,res,icon):
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

	def handleRunAction(self):
		self.saveOpenResources()
		#es=self.gmk.WriteES()
		if self.projectLoadPluginLib==False:
			CliClass.LoadPluginLib()
			self.projectLoadPluginLib=True
		self.gmk.compileRunEnigma("/tmp/testgame",3)
		self.gameProcessGdb=False
		self.gameProcess = QProcess()
		self.gameProcess.start("/tmp/testgame")
		self.gameProcess.readyReadStandardOutput.connect(self.handleProcessOutput)
		self.gameProcess.readyReadStandardError.connect(self.handleProcessErrorOutput)
		self.gameProcess.finished.connect(self.handleProcessFinished)

	def handleDebugAction(self):
		self.gameProcessGdb=True
		self.gameProcess = QProcess()
		self.gameProcess.start("gdb /tmp/testgame")
		self.gameProcess.setProcessChannelMode(QProcess.MergedChannels)
		#self.gameProcess.start("/tmp/testgame.exe")
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
			s=self.gameProcess.read(600)
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

	def actionPreferences(self):
		pass

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
		self.projectTitle="noname"
		self.projectUpdateWindowTitle()
		self.updateHierarchyTree()

	def openProject(self,fileName):
		fileName=str(fileName)
		self.gmk = CliClass.GameFile()
		self.gmk.app=self.app
		self.gmk.Read(fileName)
		self.projectTitle=os.path.split(fileName)[1]
		self.projectUpdateWindowTitle()
		self.updateHierarchyTree()

	def handleOpenAction(self):
		self.projectPath = QFileDialog.getOpenFileName(self,"Open", "", "Game Files (*.gmk *.gm81 *.gm6 *.egm *.gmx)")
		if self.projectPath!="":
			CliClass.print_notice(self.projectPath)
			self.openProject(self.projectPath)

	def handleSaveAction(self):
		self.saveOpenResources()
		if not self.projectSavingEnabled:
			CliClass.print_error("saving not enabled")
			return
		if self.projectPath:
			CliClass.print_notice("save file "+fileName)
			self.gmk.Save(fileName)
			self.projectSetModified(False)
		else:
			self.handleSaveAsAction()

	def handleSaveAsAction(self):
		self.saveOpenResources()
		if not self.projectSavingEnabled:
			CliClass.print_error("saving not enabled")
			return
		self.projectPath = QFileDialog.getSaveFileName(self,"Save", "", "Game Files (*.gmk *.gm81 *.gm6 *.egm *.gmx)")
		if self.projectPath!="":
			CliClass.print_notice("save file "+fileName)
			self.gmk.Save(fileName)
			self.projectSetModified(False)

	def handleCloseApplication(self):
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

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	#app.setStyleSheet(open(resourcePath+"theme.qss").read())
	app.setStyleSheet(" QTabBar::tab { height: 16; icon-size: 18px; } QStatusBar::item { border: 0px solid black; }");
	window = MainWindow(app)
	window.show()
	if len(sys.argv)>1:
		window.openProject(sys.argv[1])
	sys.exit(app.exec_())
