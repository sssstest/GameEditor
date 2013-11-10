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

import argparse
import sys
from CliClass import *
if sys.version_info[0]<3:
	from ConfigParser import *
else:
	from configparser import *

testGameFile=tmpDir+"testgame.exe"

def newGame(code):
	resourcePath=os.path.join(module_path(),"ideicons")+"/"
	game=GameFile()
	room=game.newRoom()
	room.setMember("caption","room 0")
	instance=room.newInstance()
	object=game.newObject()
	event=GameEvent(game)
	action=GameAction(game)
	action.setActionCode(code)#'show_message("show");game_end();'
	#event.eventNumber=0
	#event.setMember("eventKind",0)
	event.actions.append(action)
	object.addEvent(event)
	sprite=game.newSprite()
	sprite.newSubimageFile(resourcePath+"resources/sprite.png")
	object.setMember("sprite",sprite)
	instance.setMember("object",object)
	game.newSettings()
	game.newGameInformation()
	return game

def loadPreferences():
	print_notice("loading preferences: "+os.path.expanduser("~/.GameEditor.cfg"))
	config = ConfigParser()
	config.read([os.path.join(module_path(), "GameEditor.cfg"), os.path.expanduser("~/.GameEditor.cfg")])
	global enigmaPath
	enigmaPath = config.get("Editor", "enigmadev")
	#print_notice("changing directory to enigma-dev: "+self.enigmaPath)
	try:
		os.chdir(enigmaPath)
	except:
		print_notice("error changing directory to enigma-dev: "+self.enigmaPath)
	if IfEnigmaDir():
		print_notice("enigma installation found")
	else:
		print_error("enigma installation not found")

def cli():
	loadPreferences()
	parser = argparse.ArgumentParser(description="input file with no options builds in debug mode and runs game")
	parser.add_argument("filein", metavar="FILE.GMK", type=str, nargs="?",help="read file (gmk gm81 egm gmx gmz formats)")
	parser.add_argument("-o", dest="writefile", help="convert to output file and exit (gmk ggg formats)")
	parser.add_argument("-c", dest="code", help="empty game with object create event code")
	parser.add_argument("-r", dest="run", action="store_true", help="run game emode")
	parser.add_argument("-t", dest="test", action="store_true", help="test")
	parser.add_argument("-s", dest="stats", action="store_true", help="stats")
	parser.add_argument("-p", dest="python", help="run python code")
	parser.add_argument("-i", dest="interactive", action="store_true", help="interactive")
	parser.add_argument("-j", dest="dejavu", action="store_true", help="print dejavu AST for scripts")
	if len(sys.argv)==1:
		args = parser.parse_args(["--help"])
	else:
		args = parser.parse_args()
	try:
		app = QtGui.QApplication(["python"])
	except:
		print_warning("pyqt4 is not installed")
	if args.filein:
		p=args.filein
		if p[-1] in ["/","\\"]:
			p=p[:-1]
		ext=os.path.splitext(p)[1]
		gameFile=GameFile()
		print_notice("loading "+p)
		gameFile.Read(p)
	if args.code:
		gameFile=newGame(args.code)
	if args.stats:
		gameFile.printBasicStats()
		sys.exit(0)
	if args.python:
		import code
		t=code.InteractiveConsole(locals())
		t.runsource(args.python)
	if args.interactive:
		gameFile.resourceTree.PrintRecursive()
		import code
		t=code.InteractiveConsole(locals())
		t.interact()
		sys.exit(0)
	if args.dejavu:
		import dejavu.parser
		for s in gameFile.scripts:
			print_notice("AST for script "+s.getMember("name"))
			code=s.getMember("value")
			#print code
			print(dejavu.parser.parseGML(s.getMember("name"), code.decode()))
		for o in gameFile.objects:
			for ec in o.events:
				name = o.getMember("name") + "_" + str(ec.eventNumber) + "_" + str(ec.getMember("eventKind"))
				print_notice("AST for "+name)
				code = getActionsCode(ec.actions)#.encode()
				#print code
				print(dejavu.parser.parseGML(name, code))
		sys.exit(0)
	if args.writefile:
		if args.writefile=="-":
			ext=".ggg"
			gameFile.SaveExt(ext,tmpDir+"crap",wfile=sys.stdout)
		else:
			ext=os.path.splitext(os.path.split(args.writefile)[1])[1]
			if ext not in [".gmk",".gm81",".egm",".gmx",".ggg"]:
				print_error("unsupported output type "+ext)
			print_notice("saving "+args.writefile)
			gameFile.SaveExt(ext,args.writefile)
		sys.exit(0)
	gameFile.app=app
	if args.test:
		sys.exit(0)
	emode=emode_compile#make turns compile into debug
	if args.run:
		emode=emode_run
	#if os.name!="nt":
	#	redirectStdout()
		#realStdout=sys.stdout
	#	setRealStdout(realStdout)
	LoadPluginLib()
	print_notice("ENIGMA compile")
	gameFile.compileRunEnigma(testGameFile,emode)
	restoreStdout()
	if emode==emode_compile:
		print_notice("run game")
		print_notice(subprocess.check_output([testGameFile]))

if __name__=="__main__":
	cli()