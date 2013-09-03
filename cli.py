#!/usr/bin/env python

import argparse
import sys
from CliClass import *

testGameFile="/tmp/testgame"

def newGameCode(code):
	es=EnigmaStruct()
	obj=ESObject()
	ev=ESEvent()
	ev.code = code
	ev.id = 0
	mev=ESMainEvent()
	mev.id = 0
	mev.eventCount = 1
	mev.events = pointer(ev)
	obj.mainEventCount = 1
	obj.mainEvents = pointer(mev)
	obj.name = "obj_0"
	obj.id=0
	obj.spriteId = obj.parentId = obj.maskId = -1
	es.gmObjects = pointer(obj)
	es.gmObjectCount = 1
	inst=ESRoomInstance()
	inst.x=20
	inst.y=20
	inst.objectId=obj.id
	inst.id=100001
	inst.creationCode=""
	room=ESRoom()
	room.name="room_0"
	room.id=0
	room.caption="room 0"
	room.width=640
	room.height=480
	room.speed=30
	room.background=0xff00a0e6
	room.drawBackgroundColor=1
	room.creationCode=""
	room.instances=pointer(inst)
	room.instanceCount=1
	es.rooms = pointer(room)
	es.roomCount = 1
	return es

def cli():
	parser = argparse.ArgumentParser(description="input file with no options builds in debug mode and runs game")
	parser.add_argument('filein', metavar='FILE.GMK', type=str, nargs="?",help='read file (gmk gm81 egm gmx gmz formats)')
	parser.add_argument('-o', dest='writefile', help="convert to output file and exit (gmk ggg formats)")
	parser.add_argument('-c', dest='code', help="empty game with object create event code")
	parser.add_argument('-r', dest='run', action='store_true', help="run game emode")
	parser.add_argument('-t', dest='test', action='store_true', help="test")
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
	if args.writefile:
		if args.writefile=="-":
			ext=".ggg"
			gameFile.Save(ext,"/tmp/crap",wfile=sys.stdout)
		else:
			ext=os.path.splitext(os.path.split(args.writefile)[1])[1]
			if ext not in [".gmk",".gm81",".egm",".gmx",".ggg"]:
				print_error("unsupported output type "+ext)
		print_notice("saving "+args.writefile)
		gameFile.Save(ext,args.writefile)
		sys.exit(0)
	if args.code:
		es=newGameCode(args.code)
	else:
		print_notice("writing EnigmaStruct")
		gameFile.app=app
		es=gameFile.WriteES()
	if args.test:
		sys.exit(0)
	emode=emode_compile#make turns compile into debug
	if args.run:
		emode=emode_run
	LoadPluginLib()
	GameFile.compileRunES(es,testGameFile,emode)
	if emode==emode_compile:
		print_notice("run game")
		print_notice(subprocess.check_output([testGameFile]))

if __name__=='__main__':
	cli()