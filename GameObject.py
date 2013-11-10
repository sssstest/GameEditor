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

from GameResource import *
from GameSprite import *
from GameSound import *
from GameBackground import *
from GamePath import *
from GameScript import *
from GameShader import *
from GameFont import *
from GameTimeline import *
from GameObject import *
from GameRoom import *
from GameTrigger import *
RtUnknown=9
from CliLexer import *

def ifWordArgumentValue(chil):
	for child in chil:
		if child not in "1234567890abcdefghijklmnopqrstuvwxyz_":
			return False
	return True

#* getActionsCode converted to python from https://github.com/enigma-dev/enigma-dev/blob/master/pluginsource/org/enigma/EnigmaWriter.java

#* Copyright (C) 2008, 2009 IsmAvatar <IsmAvatar@gmail.com>
#* 
#* Enigma Plugin is free software: you can redistribute it and/or modify
#* it under the terms of the GNU General Public License as published by
#* the Free Software Foundation, either version 3 of the License, or
#* (at your option) any later version.
#* 
#* Enigma Plugin is distributed in the hope that it will be useful,
#* but WITHOUT ANY WARRANTY; without even the implied warranty of
#* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#* GNU General Public License (COPYING) for more details.
#* 
#* You should have received a copy of the GNU General Public License
#* along with this program. If not, see <http://www.gnu.org/licenses/>.

def getActionsCode(actions):
	code=""
	numberOfBraces = 0
	numberOfIfs = 0
	for act in actions:
		#la = act.getLibAction()
		#if (la == null)
		#	print_error("EnigmaWriter.UNSUPPORTED_DND")
		#	continue
		if act.getMember("kind")==GameAction.ACT_BEGIN:
			code+='{'
			numberOfBraces+=1
		elif act.getMember("kind")==GameAction.ACT_CODE:
			#surround with brackets (e.g. for if conditions before it) and terminate dangling comments
			code+='{'+act.argumentValue[0]+"/**/\n}\n"
		elif act.getMember("kind")==GameAction.ACT_ELSE:
			if numberOfIfs > 0:
				code+="else "
				numberOfIfs-=1
		elif act.getMember("kind")==GameAction.ACT_END:
			if numberOfBraces > 0:
				code+='}'
				numberOfBraces-=1
		elif act.getMember("kind")==GameAction.ACT_EXIT:
			code+="exit "
		elif act.getMember("kind")==GameAction.ACT_REPEAT:
			code+="repeat ("+act.argumentValue[0]+") "
		elif act.getMember("kind")==GameAction.ACT_VARIABLE:
			if act.getMember("relative"):
				code+=act.argumentValue[0]+" += "+act.argumentValue[1]+"\n"
			else:
				code+=act.argumentValue[0]+" = "+act.argumentValue[1]+"\n"
		elif act.getMember("kind")==GameAction.ACT_NORMAL:
			if act.getMember("actionId") == 605:
				if act.getMember("type") != 0:
					print_warning("comment type not 0")
				return ""
			if act.getMember("type") == GameAction.EXEC_NONE:
				return ""
			if act.getMember("appliesToSomething") and act.getMember("appliesToObject") != GameObject.OBJECT_SELF:
				if act.question:
					# Question action using with statement
					if act.getMember("appliesToObject") == GameObject.OBJECT_OTHER:
						code+="with (other) "
					elif act.getMember("appliesToObject"):
						code+="with ("+str(act.appliesToObject)+") "
					else:
						code+="/*null with!*/"
				else:
					if act.getMember("appliesToObject") == GameObject.OBJECT_OTHER:
						code+="with (other) {"
						numberOfBraces+=1#clifixed
					elif act.getMember("appliesToObject"):
						code+="with ("+str(act.appliesToObject)+") {"
						numberOfBraces+=1#clifixed
					else:
						code+="/*null with!*/{"
						numberOfBraces+=1#clifixed
			if act.getMember("question"):
				code+="if "
				numberOfIfs+=1
			if act.getMember("notFlag"): code+='!'
			if act.getMember("mayBeRelative"):
				if act.getMember("question"):
					code+="(argument_relative := "+str(act.getMember("relative"))+", "
				else:
					code+="{argument_relative := "+str(act.getMember("relative"))+"; "
					numberOfBraces+=1#clifixed

			if act.getMember("question") and act.getMember("type") == GameAction.EXEC_CODE:
				code+="lib"+str(act.getMember("parentId"))+"_action"+str(act.getMember("id"))
			else:
				code+=act.getMember("functionName")
				if act.getMember("functionCode"):
					code+=act.getMember("functionCode")
			if act.getMember("type") == GameAction.EXEC_FUNCTION:
				code+='('
				for i in range(act.getMember("argumentsUsed")):
					if i != 0: code+=','
					code+=argToString(act.argumentValue[i],act.argumentKind[i])
				code+=')'
			if act.getMember("relative"):
				if act.getMember("question"):
					code+=')'
				else:
					code+="\n}"
					numberOfBraces-=1#clifixed
			code+="\n"

			if act.getMember("appliesToSomething") and act.getMember("appliesToObject") != GameObject.OBJECT_SELF and not act.getMember("question"):
				code+="\n}"
				numberOfBraces-=1#clifixed

	if numberOfBraces > 0:
		#someone forgot the closing block action
		for i in range(numberOfBraces):
			code+="\n}"
	return code

def argToString(val, kind):
		if kind==Argument.ARG_BOTH:
			#treat as literal if starts with quote (")
			if val.startswith("\"") or val.startswith("'"):
				return val
			#else fall through
		if kind==Argument.ARG_STRING:
			return "\"" + val.replace("\\","\\\\").replace("\"","\"+'\"'+\"") + "\""
		elif kind==Argument.ARG_BOOLEAN:
			return str(not val=="0")
		elif kind==Argument.ARG_MENU:
			return val
		elif kind==Argument.ARG_COLOR:
			return "$"+hex(int(val))
		else:
			if kind == 0:
				return val
			#	return arg.getRes().get().getName()
			#val = "-1"
			return val#clifix name

class Argument(object):
	ARG_EXPRESSION = 0
	ARG_STRING = 1
	ARG_BOTH = 2
	ARG_BOOLEAN = 3
	ARG_MENU = 4
	ARG_COLOR = 13

	ARG_FONTSTRING = 15
	ARG_SPRITE = 5
	ARG_SOUND = 6
	ARG_BACKGROUND = 7
	ARG_PATH = 8
	ARG_SCRIPT = 9
	ARG_GMOBJECT = 10
	ARG_ROOM = 11
	ARG_FONT = 12
	ARG_TIMELINE = 14

class GameEvent(GameResource):
	defaults={"id":-1,"name":"noname","eventKind":0}

	if Class:
		#Gmk eventKind ES Event id
		EnNormal = 0
		EnStepNormal = 0
		EnStepBegin = 1
		EnStepEnd = 2
		EnDrawNormal = 0
		EnDrawGUI = 64
		EnDrawResize = 64
		EnOtherOutsideRoom = 0
		EnOtherIntersectBoundary = 1
		EnOtherGameStart = 2
		EnOtherGameEnd = 3
		EnOtherRoomStart = 4
		EnOtherRoomEnd = 5
		EnOtherNoMoreLives = 6
		EnOtherAnimationEnd = 7
		EnOtherEndOfPath = 8
		EnOtherNoMoreHealth = 9
		EnOtherUser0 = 10
		EnOtherUser1 = 11
		EnOtherUser2 = 12
		EnOtherUser3 = 13
		EnOtherUser4 = 14
		EnOtherUser5 = 15
		EnOtherUser6 = 16
		EnOtherUser7 = 17
		EnOtherUser8 = 18
		EnOtherUser9 = 19
		EnOtherUser10 = 20
		EnOtherUser11 = 21
		EnOtherUser12 = 22
		EnOtherUser13 = 23
		EnOtherUser14 = 24
		EnOtherUser15 = 25
		EnOtherOutsideView0 = 40
		EnOtherOutsideView1 = 41
		EnOtherOutsideView2 = 42
		EnOtherOutsideView3 = 43
		EnOtherOutsideView4 = 44
		EnOtherOutsideView5 = 45
		EnOtherOutsideView6 = 46
		EnOtherOutsideView7 = 47
		EnOtherBoundaryView0 = 50
		EnOtherBoundaryViewView1 = 51
		EnOtherBoundaryViewView2 = 52
		EnOtherBoundaryViewView3 = 53
		EnOtherBoundaryViewView4 = 54
		EnOtherBoundaryViewView5 = 55
		EnOtherBoundaryViewView6 = 56
		EnOtherBoundaryViewView7 = 57
		EnOtherAyscDialog = 63
		EnOtherAyscIAP = 66
		EnOtherAyscCloud = 67
		EnOtherAyscNetworking = 68
		EnKeyboardBackspace = 8
		EnKeyboardEnter = 13
		EnKeyboardShift = 16
		EnKeyboardControl = 17
		EnKeyboardAlt = 18
		EnKeyboardEscape = 27
		EnKeyboardSpace = 32
		EnKeyboardPageUp = 33
		EnKeyboardPageDown = 34
		EnKeyboardEnd = 35
		EnKeyboardHome = 36
		EnKeyboardArrowLeft = 37
		EnKeyboardArrowUp = 38
		EnKeyboardArrowRight = 39
		EnKeyboardArrowDown = 40
		EnKeyboardInsert = 45
		EnKeyboardDelete = 46
		EnKeyboard0 = 48
		EnKeyboard1 = 49
		EnKeyboard2 = 50
		EnKeyboard3 = 51
		EnKeyboard4 = 52
		EnKeyboard5 = 53
		EnKeyboard6 = 54
		EnKeyboard7 = 55
		EnKeyboard8 = 56
		EnKeyboard9 = 57
		EnKeyboardA = 65
		EnKeyboardB = 66
		EnKeyboardC = 67
		EnKeyboardD = 68
		EnKeyboardE = 69
		EnKeyboardF = 70
		EnKeyboardG = 71
		EnKeyboardH = 72
		EnKeyboardI = 73
		EnKeyboardJ = 74
		EnKeyboardK = 75
		EnKeyboardL = 76
		EnKeyboardM = 77
		EnKeyboardN = 78
		EnKeyboardO = 79
		EnKeyboardP = 80
		EnKeyboardQ = 81
		EnKeyboardR = 82
		EnKeyboardS = 83
		EnKeyboardT = 84
		EnKeyboardU = 85
		EnKeyboardV = 86
		EnKeyboardW = 87
		EnKeyboardX = 88
		EnKeyboardY = 89
		EnKeyboardZ = 90
		EnKeyboardKeyPad0 = 96
		EnKeyboardKeyPad1 = 97
		EnKeyboardKeyPad2 = 98
		EnKeyboardKeyPad3 = 99
		EnKeyboardKeyPad4 = 100
		EnKeyboardKeyPad5 = 101
		EnKeyboardKeyPad6 = 102
		EnKeyboardKeyPad7 = 103
		EnKeyboardKeyPad8 = 104
		EnKeyboardKeyPad9 = 105
		EnKeyboardKeyPadMultiply = 106
		EnKeyboardKeyPadAdd = 107
		EnKeyboardKeyPadSubstract = 109
		EnKeyboardKeyPadPeriod = 110
		EnKeyboardKeyPadSlash = 111
		EnKeyboardF1 = 112
		EnKeyboardF2 = 113
		EnKeyboardF3 = 114
		EnKeyboardF4 = 115
		EnKeyboardF5 = 116
		EnKeyboardF6 = 117
		EnKeyboardF7 = 118
		EnKeyboardF8 = 119
		EnKeyboardF9 = 120
		EnKeyboardF10 = 121
		EnKeyboardF11 = 122
		EnKeyboardF12 = 123

		kindNames={0:{0:"NORMAL"},
		3:{#Step
		0:"Normal",1:"Begin",2:"End"},
		8:{#Draw
		0:"Normal",64:"GUI"},
		7:{#Other
		0:"OutsideRoom",1:"IntersectBoundary",2:"GameStart",3:"GameEnd",4:"RoomStart",5:"RoomEnd",6:"NoMoreLives",7:"AnimationEnd",
		8:"EndOfPath",9:"NoMoreHealth",
		10:"User0",11:"User1",12:"User2",13:"User3",14:"User4",15:"User5",16:"User6",17:"User7",
		18:"User8",19:"User9",20:"User10",21:"User11",22:"User12",23:"User13",24:"User14",25:"User15",
		40:"OutsideView0",41:"OutsideView1",42:"OutsideView2",43:"OutsideView3",44:"OutsideView4",45:"OutsideView5",
		46:"OutsideView6",47:"OutsideView7",
		50:"BoundaryView0",51:"BoundaryViewView1",52:"BoundaryViewView2",53:"BoundaryViewView3",
		54:"BoundaryViewView4",55:"BoundaryViewView5",56:"BoundaryViewView6",57:"BoundaryViewView7",
		63:"AyscDialog",66:"AyscIAP",67:"AyscCloud",68:"AyscNetworking"},
		5:{#Keyboard
		8:"Backspace",13:"Enter",16:"Shift",17:"Control",18:"Alt",27:"Escape",32:"Space",33:"PageUp",
		34:"PageDown",35:"End",36:"Home",37:"ArrowLeft",38:"ArrowUp",39:"ArrowRight",40:"ArrowDown",45:"Insert",
		46:"Delete",48:"Keyboard0",49:"Keyboard1",50:"Keyboard2",51:"Keyboard3",52:"Keyboard4",53:"Keyboard5",54:"Keyboard6",
		55:"Keyboard7",56:"Keyboard8",57:"Keyboard9",65:"A",66:"B",67:"C",68:"D",69:"E",
		70:"F",71:"G",72:"H",73:"I",74:"J",75:"K",76:"L",77:"M",
		78:"N",79:"O",80:"P",81:"Q",82:"R",83:"S",84:"T",85:"U",
		86:"V",87:"W",88:"X",89:"Y",90:"Z",96:"KeyPad0",97:"KeyPad1",98:"KeyPad2",
		99:"KeyPad3",100:"KeyPad4",101:"KeyPad5",102:"KeyPad6",103:"KeyPad7",104:"KeyPad8",105:"KeyPad9",106:"KeyPadMultiply",
		107:"KeyPadAdd",109:"KeyPadSubstract",110:"KeyPadPeriod",111:"KeyPadSlash",112:"F1",113:"F2",114:"F3",115:"F4",
		116:"F5",117:"F6",118:"F7",119:"F8",120:"F9",121:"F10",122:"F11",123:"F12"}}

		#Gmk eventNumber ES MainEvent id
		EkCreate = 0
		EkDestroy = 1
		EkAlarm = 2#Gmk eventKind alarm number
		EkStep = 3
		EkCollision = 4
		EkKeyboard = 5#Gmk eventKind key
		EkMouse = 6
		EkOther = 7
		EkDraw = 8
		EkPress = 9#Gmk eventKind key
		EkRelease = 10#Gmk eventKind key
		EkAsyncronous = 11
		EkUnknown = 12

		eventNames=["CREATE","DESTROY","ALARM","STEP","COLLISION","KEYBOARD","MOUSE","OTHER","DRAW","PRESS","RELEASE","ASYNC","UNKNOWN"]

	def __init__(self, gameFile):
		GameResource.__init__(self, gameFile, -1)
		self.eventNumber=0
		self.eventCollisionObject=None
		self.actions=[]

	def setMember(self, member, value):
		GameResource.setMember(self, member, value)
		if not self.gameFile.ifReadingFile:
			if self.eventNumber == 4 and member=="eventKind":
				if value != GameObject.SpriteIndexNone:
					self.eventCollisionObject = self.gameFile.GetResource(GameObject, value)

	def eventCollisionObjectName(self):
		if self.eventNumber == 4:
			id = self.getMember("eventKind")
			for o in self.gameFile.objects:
				if o.getMember("id") == id:
					return o.getMember("name")
			return None
		else:
			print_error("not collision")

	@staticmethod
	def eventKindNumber(eventNumber,name,gameFile):
		if eventNumber in [9,10]:
			eventNumber=5
		if eventNumber == 4:
			return gameFile.GetResourceName(GameObject, name).getMember("id")
		if eventNumber == 2:
			return int(name)
		kindNames=GameEvent.kindNames[eventNumber]
		for i in kindNames.keys():
			if kindNames[i].lower()==name.lower():
				return i
		print_error("unsupported kind name "+name)

	@staticmethod
	def eventNameNumber(name):
		for i in range(len(GameEvent.eventNames)):
			if GameEvent.eventNames[i].lower()==name.lower():
				return i
		print_error("unsupported event name "+name)

	def eventNumberName(self, n):
		if n in range(13):
			return self.eventNames[n].lower()
		return str(n)

	def eventKindName(self, n, k):
		if n==GameEvent.EkStep:
			return self.kindNames[GameEvent.EkStep].get(k,str(k)).lower()
		elif n in [GameEvent.EkKeyboard,GameEvent.EkPress,GameEvent.EkRelease]:
			return self.kindNames[GameEvent.EkKeyboard].get(k,str(k)).lower()
		elif n==GameEvent.EkOther:
			return self.kindNames[GameEvent.EkOther].get(k,str(k)).lower()
		elif n==GameEvent.EkDraw:
			return self.kindNames[GameEvent.EkDraw].get(k,str(k)).lower()
		elif n==GameEvent.EkAsyncronous:
			return self.kindNames[GameEvent.EkOther].get(k,str(k)).lower()
		return str(k)

	def eventGGGName(self):
		if self.eventNumber in [GameEvent.EkCreate,GameEvent.EkDestroy] and self.getMember("eventKind")==0:
			stri="@ev_"+self.eventNumberName(self.eventNumber)
		elif self.eventNumber == GameEvent.EkCollision:
			if self.eventCollisionObject:
				stri="@ev_"+self.eventNumberName(self.eventNumber)+"("+self.eventCollisionObject.getMember("name")+")"
			else:
				print_warning("collision event didn't find eventCollisionObject "+str(self.getMember("eventKind")))
				stri="@ev_"+self.eventNumberName(self.eventNumber)+"("+self.eventKindName(self.eventNumber,self.getMember("eventKind"))+")"
		else:
			stri="@ev_"+self.eventNumberName(self.eventNumber)+"("+self.eventKindName(self.eventNumber,self.getMember("eventKind"))+")"
		return stri

	def WriteGGG(self):
		stri=self.eventGGGName()+" {\n"
		for o in self.actions:
			stri=stri+tabStringLines(o.WriteGGG(len(self.actions)))
		stri+="}\n"
		return stri

	def Finalize(self):
		if self.eventNumber==GameEvent.EkCollision:
			self.eventCollisionObject=self.gameFile.GetResource(GameObject, self.getMember("eventKind"))

class GameAction(GameResource):
	if Class:
		ACT_NORMAL = 0
		ACT_BEGIN = 1
		ACT_END = 2
		ACT_ELSE = 3
		ACT_EXIT = 4
		ACT_REPEAT = 5
		ACT_VARIABLE = 6
		ACT_CODE = 7
		ACT_PLACEHOLDER = 8
		ACT_SEPARATOR = 9
		ACT_LABEL = 10

		EXEC_NONE = 0
		EXEC_FUNCTION = 1
		EXEC_CODE = 2

		ARGUMENT_COUNT = 8;

		ActionKindNormal=0
		ActionKindBeginGroup=1
		ActionKindEndGroup=2
		ActionKindElse=3
		ActionKindExit=4
		ActionKindRepeat=5
		ActionKindVariable=6
		ActionKindCode=7

		ArgumentKindExpression=0	#<string>
		ArgumentKindString=1		#<string>test&#xD;..</string>
		ArgumentKindBoth=2		#<string></string>
		ArgumentKindBoolean=3		#<string>0</string>
		ArgumentKindMenu=4		#<string>0</string>
		ArgumentKindSprite=5		#<sprite>-1</sprite>
		ArgumentKindSound=6		#<sound>-1</sound>
		ArgumentKindBackground=7	#<background>-1</background>
		ArgumentKindPath=8		#<path>-1</path>
		ArgumentKindScript=9		#<script>-1</script>
		ArgumentKindObject=10		#<object>-100</object>
		ArgumentKindRoom=11		#<room>-1</room>
		ArgumentKindFont=12		#<font>-1</font>
		ArgumentKindColor=13		#<string>16777215</string><string>255</string>
		ArgumentKindTimeline=14	#<timeline>-1</timeline>
		ArgumentKindFontString=15
		ArgumentKindCount=16

		#ActionType
		AtNothing=0
		AtFunction=1
		AtCode=2

		#AppliesTo
		ApObject		= 0	#// >= 0 refers to an object index
		ApSelf			= -1
		ApOther			= -2

	if Class:
		#kind0 type1 lib actionId
		actionIdFunctionName={}#appliesToObject=-1 relative=False appliesToSomething=True question=False appliesToSomething=False 
		actionIdArgumentKinds={}#notFlag=False
		actionIdKind={}
		actionIdMayBeRelative={}
		actionIdQuestion={}
		actionIdType={}
		actionIdFunctionName[101]="action_move"
		actionIdArgumentKinds[101]=[1,0]
		actionIdMayBeRelative[101]=True
		actionIdFunctionName[102]="action_set_motion"
		actionIdArgumentKinds[102]=[0,0]
		actionIdMayBeRelative[102]=True
		actionIdFunctionName[103]="action_set_hspeed"
		actionIdArgumentKinds[103]=[0]
		actionIdMayBeRelative[103]=True
		actionIdFunctionName[104]="action_set_vspeed"
		actionIdArgumentKinds[104]=[0]
		actionIdMayBeRelative[104]=True
		actionIdFunctionName[105]="action_move_point"
		actionIdArgumentKinds[105]=[0,0,0]
		actionIdMayBeRelative[105]=True
		actionIdFunctionName[107]="action_set_gravity"
		actionIdArgumentKinds[107]=[0,0]
		actionIdMayBeRelative[107]=True
		actionIdFunctionName[108]="action_set_friction"
		actionIdArgumentKinds[108]=[0]
		actionIdMayBeRelative[108]=True
		actionIdFunctionName[109]="action_move_to"
		actionIdArgumentKinds[109]=[0,0]
		actionIdMayBeRelative[109]=True
		actionIdFunctionName[110]="action_move_start"
		actionIdArgumentKinds[110]=[]
		actionIdFunctionName[111]="action_move_random"
		actionIdArgumentKinds[111]=[0,0]
		actionIdFunctionName[112]="action_wrap"
		actionIdArgumentKinds[112]=[4]
		actionIdFunctionName[113]="action_reverse_xdir"
		actionIdArgumentKinds[113]=[]
		actionIdFunctionName[114]="action_reverse_ydir"
		actionIdArgumentKinds[114]=[]
		actionIdFunctionName[115]="action_bounce"
		actionIdArgumentKinds[115]=[4,4]
		actionIdFunctionName[116]="action_move_contact"
		actionIdArgumentKinds[116]=[0,0,4]
		actionIdFunctionName[117]="action_snap"
		actionIdArgumentKinds[117]=[0,0]
		actionIdFunctionName[119]="action_path"
		actionIdArgumentKinds[119]=[8,0,4,4]
		actionIdFunctionName[120]="action_linear_step"
		actionIdArgumentKinds[120]=[0,0,0,4]
		actionIdMayBeRelative[120]=True
		actionIdFunctionName[121]="action_potential_step"
		actionIdArgumentKinds[121]=[0,0,0,4]
		actionIdMayBeRelative[121]=True
		actionIdFunctionName[122]="action_path_position"
		actionIdArgumentKinds[122]=[0]
		actionIdMayBeRelative[122]=True
		actionIdFunctionName[123]="action_path_speed"
		actionIdArgumentKinds[123]=[0]
		actionIdMayBeRelative[123]=True
		actionIdFunctionName[124]="action_path_end"
		actionIdArgumentKinds[124]=[]
		actionIdFunctionName[201]="action_create_object"
		actionIdArgumentKinds[201]=[10,0,0]
		actionIdMayBeRelative[201]=True
		actionIdFunctionName[202]="action_change_object"
		actionIdArgumentKinds[202]=[10,4]
		actionIdFunctionName[203]="action_kill_object"
		actionIdArgumentKinds[203]=[]
		actionIdFunctionName[204]="action_kill_position"
		actionIdArgumentKinds[204]=[0,0]
		actionIdMayBeRelative[204]=True
		actionIdFunctionName[206]="action_create_object_motion"
		actionIdArgumentKinds[206]=[10,0,0,0,0]
		actionIdMayBeRelative[206]=True
		actionIdFunctionName[207]="action_create_object_random"
		actionIdArgumentKinds[207]=[10,10,10,10,0,0]
		actionIdMayBeRelative[207]=True
		actionIdFunctionName[211]="action_sound"
		actionIdArgumentKinds[211]=[6,3]
		actionIdFunctionName[212]="action_end_sound"
		actionIdArgumentKinds[212]=[6]
		actionIdFunctionName[213]="action_if_sound"
		actionIdArgumentKinds[213]=[6]
		actionIdQuestion[213]=True
		actionIdFunctionName[221]="action_previous_room"
		actionIdArgumentKinds[221]=[4]
		#actionIdArgumentKinds[221]=[]#from gmx
		actionIdFunctionName[222]="action_next_room"
		actionIdArgumentKinds[222]=[4]
		#actionIdArgumentKinds[222]=[]#from gmx
		actionIdFunctionName[223]="action_current_room"
		actionIdArgumentKinds[223]=[4]
		#actionIdArgumentKinds[223]=[]#from gmx
		actionIdFunctionName[224]="action_another_room"
		actionIdArgumentKinds[224]=[11,4]
		#actionIdArgumentKinds[223]=[11]#from gmx
		actionIdFunctionName[225]="action_if_previous_room"
		actionIdArgumentKinds[225]=[]
		actionIdQuestion[225]=True
		actionIdFunctionName[226]="action_if_next_room"
		actionIdArgumentKinds[226]=[]
		actionIdQuestion[226]=True
		actionIdFunctionName[301]="action_set_alarm"
		actionIdArgumentKinds[301]=[0,4]
		actionIdQuestion[301]=True#from gmk not
		actionIdFunctionName[302]="action_sleep"#not in gmx
		actionIdArgumentKinds[302]=[0,3]
		actionIdFunctionName[303]="action_set_timeline"#not in gmx
		actionIdArgumentKinds[303]=[14,0]
		actionIdFunctionName[304]="action_set_timeline_position"
		actionIdArgumentKinds[304]=[0]
		actionIdQuestion[304]=True#not from gmx
		actionIdFunctionName[305]="action_timeline_set"#from gmx <userelative>0</userelative>
		actionIdArgumentKinds[305]=[14,0,4,4]
		actionIdFunctionName[306]="action_timeline_start"#from gmx
		actionIdArgumentKinds[306]=[]
		actionIdFunctionName[307]="action_timeline_pause"#from gmx
		actionIdArgumentKinds[307]=[]
		actionIdFunctionName[308]="action_timeline_stop"#from gmx
		actionIdArgumentKinds[308]=[]
		actionIdFunctionName[309]="action_set_timeline_speed"#from gmx
		actionIdArgumentKinds[309]=[0]
		actionIdFunctionName[321]="action_message"
		actionIdArgumentKinds[321]=[2]
		actionIdFunctionName[322]="action_show_info"
		actionIdArgumentKinds[322]=[]
		#from gmx kind=0 exetype=2 <codestring>url_open(argument0);</codestring>
		#actionIdArgumentKinds[322]=[1]#<string>http://www.yoyogames.com</string>
		actionIdFunctionName[323]="action_show_video"#not in gmx
		actionIdArgumentKinds[323]=[2,4,4]
		actionIdFunctionName[331]="action_restart_game"
		actionIdArgumentKinds[331]=[]
		actionIdFunctionName[332]="action_end_game"
		actionIdArgumentKinds[332]=[]
		actionIdFunctionName[333]="action_save_game"
		actionIdArgumentKinds[333]=[2]
		actionIdFunctionName[334]="action_load_game"
		actionIdArgumentKinds[334]=[2]
		actionIdFunctionName[401]="action_if_empty"
		actionIdArgumentKinds[401]=[0,0,4]
		actionIdQuestion[401]=True
		actionIdMayBeRelative[401]=True
		actionIdFunctionName[402]="action_if_collision"
		actionIdArgumentKinds[402]=[0,0,4]
		actionIdQuestion[402]=True
		actionIdMayBeRelative[402]=True
		actionIdFunctionName[403]="action_if_object"
		actionIdArgumentKinds[403]=[10,0,0]
		actionIdQuestion[403]=True
		actionIdMayBeRelative[403]=True
		actionIdFunctionName[404]="action_if_number"
		actionIdArgumentKinds[404]=[10,0,4]
		actionIdQuestion[404]=True
		actionIdFunctionName[405]="action_if_dice"
		actionIdArgumentKinds[405]=[0]
		actionIdQuestion[405]=True
		actionIdFunctionName[407]="action_if_question"
		actionIdArgumentKinds[407]=[2]
		actionIdQuestion[407]=True
		actionIdFunctionName[408]="action_if"
		actionIdArgumentKinds[408]=[0]
		actionIdQuestion[408]=True
		actionIdFunctionName[409]="action_if_mouse"
		actionIdArgumentKinds[409]=[4]
		actionIdQuestion[409]=True
		actionIdFunctionName[410]="action_if_aligned"
		actionIdArgumentKinds[410]=[0,0]
		actionIdQuestion[410]=True
		actionIdFunctionName[421]=""#else
		actionIdArgumentKinds[421]=[]
		actionIdKind[421]=3
		actionIdType[421]=2
		actionIdFunctionName[422]=""#start of block
		actionIdArgumentKinds[422]=[]
		actionIdKind[422]=1
		actionIdType[422]=2
		actionIdFunctionName[423]=""#repeat 3 times
		actionIdArgumentKinds[423]=[0]
		actionIdKind[423]=5
		actionIdType[423]=2
		actionIdFunctionName[424]=""#end of block
		actionIdArgumentKinds[424]=[]
		actionIdKind[424]=2
		actionIdType[424]=2
		actionIdFunctionName[425]=""#exit this event
		actionIdArgumentKinds[425]=[]
		actionIdKind[425]=4
		actionIdType[425]=2
		actionIdFunctionName[500]=""#exetype=2 #clifix type #from gmx #<codestring>draw_self();</codestring>
		actionIdArgumentKinds[500]=[]
		actionIdKind[500]=0
		actionIdFunctionName[501]="action_draw_sprite"
		actionIdArgumentKinds[501]=[5,0,0,0]
		actionIdMayBeRelative[501]=True
		actionIdFunctionName[502]="action_draw_background"
		actionIdArgumentKinds[502]=[7,0,0,3]
		actionIdMayBeRelative[502]=True
		actionIdFunctionName[511]="action_draw_rectangle"
		actionIdArgumentKinds[511]=[0,0,0,0,4]
		actionIdMayBeRelative[511]=True
		actionIdFunctionName[512]="action_draw_ellipse"
		actionIdArgumentKinds[512]=[0,0,0,0,4]
		actionIdMayBeRelative[512]=True
		actionIdFunctionName[513]="action_draw_line"
		actionIdArgumentKinds[513]=[0,0,0,0]
		actionIdMayBeRelative[513]=True
		actionIdFunctionName[514]="action_draw_text"
		actionIdArgumentKinds[514]=[2,0,0]
		actionIdMayBeRelative[514]=True
		actionIdFunctionName[515]="action_draw_arrow"
		actionIdArgumentKinds[515]=[0,0,0,0,0]
		actionIdMayBeRelative[515]=True
		actionIdFunctionName[516]="action_draw_gradient_hor"
		actionIdArgumentKinds[516]=[0,0,0,0,13,13]
		actionIdMayBeRelative[516]=True
		actionIdFunctionName[517]="action_draw_gradient_vert"
		actionIdArgumentKinds[517]=[0,0,0,0,13,13]
		actionIdMayBeRelative[517]=True
		actionIdFunctionName[518]="action_draw_ellipse_gradient"
		actionIdArgumentKinds[518]=[0,0,0,0,13,13]
		actionIdMayBeRelative[518]=True
		actionIdFunctionName[519]="action_draw_text_transformed"
		actionIdArgumentKinds[519]=[2,0,0,0,0,0]
		actionIdMayBeRelative[519]=True
		actionIdFunctionName[524]="action_color"
		actionIdArgumentKinds[524]=[13]
		actionIdFunctionName[526]="action_font"
		actionIdArgumentKinds[526]=[12,4]
		actionIdFunctionName[531]="action_fullscreen"
		actionIdArgumentKinds[531]=[4]
		actionIdFunctionName[532]="action_effect"
		actionIdArgumentKinds[532]=[4,0,0,4,13,4]
		actionIdMayBeRelative[532]=True
		actionIdFunctionName[541]="action_sprite_set"
		actionIdArgumentKinds[541]=[5,0,0]
		actionIdFunctionName[542]="action_sprite_transform"
		actionIdArgumentKinds[542]=[0,0,0,4]
		actionIdFunctionName[543]="action_sprite_color"
		actionIdArgumentKinds[543]=[13,0]
		actionIdFunctionName[601]="action_execute_script"
		actionIdArgumentKinds[601]=[9,0,0,0,0,0]
		actionIdFunctionName[603]=""#code
		actionIdArgumentKinds[603]=[1]
		actionIdKind[603]=7
		actionIdType[603]=2
		actionIdFunctionName[604]="action_inherited"
		actionIdArgumentKinds[604]=[]
		actionIdFunctionName[605]=""#comment
		actionIdArgumentKinds[605]=[1]
		actionIdKind[605]=0
		actionIdType[605]=0
		actionIdFunctionName[611]=""#set var x
		actionIdArgumentKinds[611]=[1]
		#actionIdArgumentKinds[611]=[1,0]#from gmx
		actionIdMayBeRelative[611]=True
		actionIdKind[611]=6
		actionIdType[611]=2
		actionIdFunctionName[612]="action_if_variable"
		actionIdArgumentKinds[612]=[0,0,4]
		actionIdQuestion[612]=True
		actionIdFunctionName[613]="action_draw_variable"
		actionIdArgumentKinds[613]=[0,0,0]
		actionIdMayBeRelative[613]=True
		actionIdFunctionName[701]="action_set_score"
		actionIdArgumentKinds[701]=[0]
		actionIdMayBeRelative[701]=True
		actionIdFunctionName[702]="action_if_score"
		actionIdArgumentKinds[702]=[0,4]
		actionIdQuestion[702]=True
		actionIdFunctionName[703]="action_draw_score"
		actionIdArgumentKinds[703]=[0,0,1]
		actionIdMayBeRelative[703]=True
		actionIdFunctionName[707]="action_highscore_clear"
		actionIdArgumentKinds[707]=[]
		actionIdFunctionName[709]="action_highscore_show"#not in gmx
		actionIdArgumentKinds[709]=[7,4,13,13,15]
		actionIdFunctionName[711]="action_set_life"
		actionIdArgumentKinds[711]=[0]
		actionIdMayBeRelative[711]=True
		actionIdFunctionName[712]="action_if_life"
		actionIdArgumentKinds[712]=[0,4]
		actionIdQuestion[712]=True
		actionIdFunctionName[713]="action_draw_life"
		actionIdArgumentKinds[713]=[0,0,1]
		actionIdMayBeRelative[713]=True
		actionIdFunctionName[714]="action_draw_life_images"
		actionIdArgumentKinds[714]=[0,0,5]
		actionIdMayBeRelative[714]=True
		actionIdFunctionName[721]="action_set_health"
		actionIdArgumentKinds[721]=[0]
		actionIdMayBeRelative[721]=True
		actionIdFunctionName[722]="action_if_health"
		actionIdArgumentKinds[722]=[0,4]
		actionIdQuestion[722]=True
		actionIdFunctionName[723]="action_draw_health"
		actionIdArgumentKinds[723]=[0,0,0,0,4,4]
		actionIdMayBeRelative[723]=True
		actionIdFunctionName[731]="action_set_caption"
		actionIdArgumentKinds[731]=[4,1,4,1,4,1]
		actionIdFunctionName[801]="action_set_cursor"
		actionIdArgumentKinds[801]=[5,4]
		actionIdFunctionName[802]="action_snapshot"
		actionIdArgumentKinds[802]=[2]
		actionIdFunctionName[803]="action_replace_sprite"
		actionIdArgumentKinds[803]=[5,2,0]
		actionIdFunctionName[804]="action_replace_sound"
		actionIdArgumentKinds[804]=[6,2]
		actionIdFunctionName[805]="action_replace_background"
		actionIdArgumentKinds[805]=[7,2]
		actionIdFunctionName[807]="action_webpage"
		actionIdArgumentKinds[807]=[2]
		actionIdFunctionName[808]="action_cd_play"#not in gmx
		actionIdArgumentKinds[808]=[0,0]
		actionIdFunctionName[809]="action_cd_stop"#not in gmx
		actionIdArgumentKinds[809]=[]
		actionIdFunctionName[810]="action_cd_pause"#not in gmx
		actionIdArgumentKinds[810]=[]
		actionIdFunctionName[811]="action_cd_resume"#not in gmx
		actionIdArgumentKinds[811]=[]
		actionIdFunctionName[812]="action_cd_present"#not in gmx
		actionIdArgumentKinds[812]=[]
		actionIdQuestion[812]=True
		actionIdFunctionName[813]="action_cd_playing"#not in gmx
		actionIdArgumentKinds[813]=[]
		actionIdQuestion[813]=True
		actionIdFunctionName[820]="action_partsyst_create"
		actionIdArgumentKinds[820]=[0]
		actionIdFunctionName[821]="action_partsyst_destroy"
		actionIdArgumentKinds[821]=[]
		actionIdFunctionName[822]="action_partsyst_clear"
		actionIdArgumentKinds[822]=[]
		actionIdFunctionName[823]="action_parttype_create"
		actionIdArgumentKinds[823]=[4,4,5,0,0,0]
		actionIdFunctionName[824]="action_parttype_color"
		actionIdArgumentKinds[824]=[4,4,13,13,0,0]
		actionIdFunctionName[826]="action_parttype_life"
		actionIdArgumentKinds[826]=[4,0,0]
		actionIdFunctionName[827]="action_parttype_speed"
		actionIdArgumentKinds[827]=[4,0,0,0,0,0]
		actionIdFunctionName[828]="action_parttype_gravity"
		actionIdArgumentKinds[828]=[4,0,0]
		actionIdFunctionName[829]="action_parttype_secondary"
		actionIdArgumentKinds[829]=[4,4,0,4,0]
		actionIdFunctionName[831]="action_partemit_create"
		actionIdArgumentKinds[831]=[4,4,0,0,0,0]
		actionIdFunctionName[832]="action_partemit_destroy"
		actionIdArgumentKinds[832]=[4]
		actionIdFunctionName[833]="action_partemit_burst"
		actionIdArgumentKinds[833]=[4,4,0]
		actionIdFunctionName[834]="action_partemit_stream"
		actionIdArgumentKinds[834]=[4,4,0]

	defaults={"functionName":"","functionCode":"","libraryId":0,"actionId":0,"kind":0,"type":0,
		  "argumentsUsed":0,"appliesToObject":ApSelf,"relative":False,"appliesToSomething":False,
		  "question":False,"mayBeRelative":False,"notFlag":False}

	def __init__(self, gameFile):
		GameResource.__init__(self, gameFile, -1)
		self.argumentLink=[None,None,None,None,None,None,None,None]
		self.argumentValue=["","","","","","","",""]
		self.argumentKind=[0,0,0,0,0,0,0,0]
		self.appliesObject=None

	def setActionCode(self, code):
		self.setMember("libraryId",1)
		self.setMember("actionId",603)
		self.setMember("kind",7)
		self.setMember("type",2)
		self.argumentValue[0]=code
		self.argumentKind[0]=1
		self.setMember("argumentsUsed",1)

	def ifActionCode(self):
		return self.getMember("libraryId") == 1 and self.getMember("actionId") == 603

	def WriteGGG(self, nactions):
		ml=False
		singleaction=False
		for a in self.argumentValue:
			if "\n" in a:
				ml=True
		v=[]
		for a,k in zip(self.argumentValue,self.argumentKind):
			if a.isdigit():
				v.append(a)
			elif ifWordArgumentValue(a):
				v.append(a)
			elif "\n" in a:
				v.append(a+"\n")
			else:
				v.append(a)
		v=v[:self.getMember("argumentsUsed")]
		stri="@action "+str(self.getMember("libraryId"))+" "+str(self.getMember("actionId"))+"{\n"
		if self.getMember("libraryId")==1:
			if self.getMember("actionId") in self.actionIdFunctionName:
				f=self.actionIdFunctionName[self.getMember("actionId")]
				if self.getMember("functionName")==f:
					if f=="" and self.getMember("libraryId")==1:
						if self.getMember("actionId")==421:
							stri="@else "+",".join(v)+"\n"
							return stri
						elif self.getMember("actionId")==422:
							stri="@start "+",".join(v)+"\n"
							return stri
						elif self.getMember("actionId")==423:
							stri="@repeat "+",".join(v)+"\n"
							return stri
						elif self.getMember("actionId")==424:
							stri="@end "+",".join(v)+"\n"
							return stri
						elif self.getMember("actionId")==425:
							stri="@exitevent "+",".join(v)+"\n"
							return stri
						elif self.getMember("actionId")==611:
							stri="@set "+",".join(v)+"\n"
							return stri
						if self.getMember("actionId")==603:
							if nactions==1:
								stri=""
								singleaction=True
							else:
								stri="@code {\n"
						elif self.getMember("actionId")==605:
							if ml:
								stri="@comment {\n"
							else:
								stri="@comment "+",".join(v)+"\n"
								return stri
					if f!="":
						if f.startswith("action"):
							stri="@"+f
						else:
							print_error("unsupported action "+f)
							stri="@action "+f
						if ml:
							stri+="\n"
						else:
							stri+="("+",".join(v)+")\n"
							#for key in self.members:
							#	if not self.ifDefault(key):
							#		stri+="\t"+key+"="+str(self.getMember(key))+"\n"
							return stri
		else:
			print_error("unsupported libraryId "+str(self.getMember("libraryId")))
		if self.getMember("actionId")==603:
			if len(v)>1:
				print_error("603 more than 1 argument")
			stri+=tabStringLines(v[0],tab="\t")
		else:
			stri+=",".join(v)+"\n"
			if ml:
				print_error("unsupported newline in action arguments "+f)
		if not singleaction:
			stri+="}\n"
		return stri

	@staticmethod
	def actionNameId(name):
		for a in GameAction.actionIdFunctionName.keys():
			if GameAction.actionIdFunctionName[a]==name:
				return a

	def ReadGmk(self, stream):
		# Skip version
		stream.ReadDword()
		self.setMember("libraryId",stream.ReadDword())
		self.setMember("actionId",stream.ReadDword())
		self.setMember("kind",stream.ReadDword())
		#if self.kind == ACT_CODE:
		self.setMember("mayBeRelative",stream.ReadBoolean())
		self.setMember("question",stream.ReadBoolean())
		self.setMember("appliesToSomething",stream.ReadBoolean())
		self.setMember("type",stream.ReadDword())
		#if (la.execType == Action.EXEC_FUNCTION) la.execInfo=
		self.setMember("functionName",stream.ReadString())
		#if (la.execType == Action.EXEC_CODE) la.execInfo=
		self.setMember("functionCode",stream.ReadString())
		self.setMember("argumentsUsed",stream.ReadDword())
		count = stream.ReadDword()
		for i in range(count):
			self.argumentKind[i]=stream.ReadDword()
		self.setMember("appliesToObject",stream.readInt32())
		self.setMember("relative",stream.ReadBoolean())
		count = stream.ReadDword()
		for i in range(count):
			self.argumentValue[i]=stream.ReadString()
		self.setMember("notFlag",stream.ReadBoolean())

	def WriteGmx(self, root):
		gmxCreateTag(root, "libid", str(self.getMember("libraryId")))
		gmxCreateTag(root, "id", str(self.getMember("actionId")))
		gmxCreateTag(root, "kind", str(self.getMember("kind")))
		gmxCreateTag(root, "userelative", str(boolToGmxIntbool(self.getMember("mayBeRelative"))))
		gmxCreateTag(root, "isquestion", str(boolToGmxIntbool(self.getMember("question"))))
		gmxCreateTag(root, "useapplyto", str(boolToGmxIntbool(self.getMember("appliesToSomething"))))
		gmxCreateTag(root, "exetype", str(self.getMember("type")))
		gmxCreateTag(root, "functionname", self.getMember("functionName"))
		gmxCreateTag(root, "codestring", self.getMember("functionCode"))
		id=self.getMember("appliesToObject")
		if id==-1:
			whoName="self"
		elif id==-2:
			whoName="other"
		else:
			whoName=None
			for o in self.gameFile.objects:
				if o.getMember("id")==id:
					whoName==o.getMember("name")
					break
			if not whoName:
				raise 4
		gmxCreateTag(root, "whoName", whoName)
		gmxCreateTag(root, "relative", str(boolToGmxIntbool(self.getMember("relative"))))
		gmxCreateTag(root, "isnot", str(boolToGmxIntbool(self.getMember("notFlag"))))
		arguments=xml.etree.ElementTree.Element("arguments")
		arguments.tail="\n"
		root.append(arguments)
		for c in range(self.getMember("argumentsUsed")):
			kind=self.argumentKind[c]
			value=self.argumentValue[c]
			argument=xml.etree.ElementTree.Element("argument")
			argument.tail="\n"
			arguments.append(argument)
			gmxCreateTag(argument, "kind", str(kind))
			if kind in [GameAction.ArgumentKindExpression,GameAction.ArgumentKindString,GameAction.ArgumentKindBoth,GameAction.ArgumentKindBoolean,GameAction.ArgumentKindMenu,GameAction.ArgumentKindColor,GameAction.ArgumentKindFontString]:
				gmxCreateTag(argument, "string", value)
			elif kind == GameAction.ArgumentKindSprite:
				gmxCreateTag(argument, "sprite", value)
			elif kind == GameAction.ArgumentKindSound:
				gmxCreateTag(argument, "sound", value)
			elif kind == GameAction.ArgumentKindBackground:
				gmxCreateTag(argument, "background", value)
			elif kind == GameAction.ArgumentKindPath:
				gmxCreateTag(argument, "path", value)
			elif kind == GameAction.ArgumentKindScript:
				gmxCreateTag(argument, "script", value)
			elif kind == GameAction.ArgumentKindObject:
				gmxCreateTag(argument, "object", value)
			elif kind == GameAction.ArgumentKindRoom:
				gmxCreateTag(argument, "room", value)
			elif kind == GameAction.ArgumentKindFont:
				gmxCreateTag(argument, "font", value)
			elif kind == GameAction.ArgumentKindTimeline:
				gmxCreateTag(argument, "timeline", value)
			else:
				print_error("unsupported argument kind "+str(kind))

	def WriteGmk(self, stream):
		stream.WriteDword(440)
		stream.WriteDword(self.getMember("libraryId"))
		stream.WriteDword(self.getMember("actionId"))
		stream.WriteDword(self.getMember("kind"))
		stream.WriteBoolean(self.getMember("mayBeRelative"))
		stream.WriteBoolean(self.getMember("question"))
		stream.WriteBoolean(self.getMember("appliesToSomething"))
		stream.WriteDword(self.getMember("type"))
		stream.WriteString(self.getMember("functionName"))
		stream.WriteString(self.getMember("functionCode"))
		stream.WriteDword(self.getMember("argumentsUsed"))
		stream.WriteDword(GameAction.ARGUMENT_COUNT)
		for i in range(GameAction.ARGUMENT_COUNT):
			stream.WriteDword(self.argumentKind[i])
		if self.appliesObject == None:
			stream.WriteDword(self.getMember("appliesToObject"))
		else:
			stream.WriteDword(self.appliesObject.getMember("id"))
		stream.WriteBoolean(self.getMember("relative"))
		stream.WriteDword(GameAction.ARGUMENT_COUNT)
		for i in range(GameAction.ARGUMENT_COUNT):
			if self.argumentLink[i]:
				stream.WriteString(str(self.argumentLink[i].getMember("id")))
			else:
				stream.WriteString(self.argumentValue[i])
		stream.WriteBoolean(self.getMember("notFlag"))

	def GetArgumentReference(self, index):
		akKinds = [RtUnknown,
			RtUnknown,
			RtUnknown,
			RtUnknown,
			RtUnknown,
			GameSprite,
			GameSound,
			GameBackground,
			GamePath,
			GameScript,
			GameObject,
			GameRoom,
			GameFont,
			RtUnknown,
			GameTimeline]
		if index < GameAction.ARGUMENT_COUNT:
			#self.argumentValue[index] and 
			#if akKinds[self.argumentKind[index]] != RtUnknown:
			if self.argumentValue[index].isdigit():
				return self.gameFile.GetResource(akKinds[self.argumentKind[index]], int(self.argumentValue[index]))
			return None
		else:
			return None

	def GetArgumentReferenceName(self, index):
		akKinds = [RtUnknown,
			RtUnknown,
			RtUnknown,
			RtUnknown,
			RtUnknown,
			GameSprite,
			GameSound,
			GameBackground,
			GamePath,
			GameScript,
			GameObject,
			GameRoom,
			GameFont,
			RtUnknown,
			GameTimeline]
		if index < GameAction.ARGUMENT_COUNT:
			#if akKinds[self.argumentKind[index]] != RtUnknown:
			if self.argumentValue[index]:
				return self.gameFile.GetResourceName(akKinds[self.argumentKind[index]], self.argumentValue[index])
			return None
		else:
			return None

	def Finalize(self):
		if self.getMember("appliesToObject") >= GameAction.ApObject:
			self.appliesObject = self.gameFile.GetResource(GameObject, self.getMember("appliesToObject"))
		else:
			self.appliesObject = None

		for i in range(GameAction.ARGUMENT_COUNT):
			self.argumentLink[i] = self.GetArgumentReference(i)

class GameObject(GameResource):
	if Class:
		OBJECT_SELF = -1
		OBJECT_OTHER = -2
		
		SpriteIndexNone		= -1
		ParentIndexNone		= -100
		MaskIndexNone			= -1

	defaults={"id":-1,"name":"noname","spriteIndex":SpriteIndexNone,"sprite":None,
	"solid":False,"visible":True,"depth":0,"persistent":False,"parentIndex":ParentIndexNone,"parent":None,"maskIndex":MaskIndexNone,"mask":None,
	"PhysicsObject":0,"PhysicsObjectSensor":0,"PhysicsObjectShape":0,"PhysicsObjectDensity":0.0,
	"PhysicsObjectRestitution":0.0,"PhysicsObjectGroup":0,"PhysicsObjectLinearDamping":0.0,"PhysicsObjectAngularDamping":0.0,
	"PhysicsObjectFriction":0.0,"PhysicsObjectAwake":0,"PhysicsObjectKinematic":0,"PhysicsShapePoints":0}

	def __init__(self, gameFile, id):
		GameResource.__init__(self, gameFile, id)
		self.setMember("name","object_"+str(id))
		self.events=[]

	def setMember(self, member, value):
		GameResource.setMember(self, member, value)
		if not self.gameFile.ifReadingFile:
			if member=="spriteIndex":
				if value != GameObject.SpriteIndexNone:
					self.setMember("sprite", self.gameFile.GetResource(GameSprite, value))
			elif member=="parentIndex":
				if value not in [GameObject.ParentIndexNone, -1]:
					self.setMember("parent", self.gameFile.GetResource(GameObject, value))
			elif member=="maskIndex":
				if value != GameObject.SpriteIndexNone:
					self.setMember("mask", self.gameFile.GetResource(GameSprite, value))

	def addEvent(self, event):
		self.events.append(event)
		for callBack in self.listeners:
			callBack("subresource","events",None,None)

	def ReadEgm(self, entry, z):
		stream=z.open(entry+".ey", "r")
		y=YamlParser()
		r=y.parseStream(stream)
		self.setMember("name",os.path.split(entry)[1])
		self.setMember("spriteIndex",r.getMid("SPRITE",self.gameFile.egmNameId))
		self.setMember("solid",r.getMbool("SOLID"))
		self.setMember("visible",r.getMbool("VISIBLE"))
		self.setMember("depth",r.getMint("DEPTH"))
		self.setMember("persistent",r.getMbool("PERSISTENT"))
		self.setMember("parentIndex",r.getMid("PARENT",self.gameFile.egmNameId))
		self.setMember("maskIndex",r.getMid("MASK",self.gameFile.egmNameId))
		data=r.getMstr("Data")
		eef = z.open(os.path.split(entry)[0]+"/"+data, "r")
		e=EEFReader()
		r = e.parseStream(eef)
		r=r.children[0]
		if r.blockName != "Events":
			print_error("block isn't Events "+r.blockName)
		for mevent in r.children:
			event = GameEvent(self.gameFile)
			event.eventNumber = int(mevent.id[1])
			eventKind = mevent.id[0]
			if event.eventNumber==4:
				event.setMember("eventKind", self.gameFile.egmNameId[eventKind])
			else:
				if not eventKind.isdigit():
					print_error("eventKind isn't a number "+eventKind)
				event.setMember("eventKind", int(eventKind))
			for eevent in mevent.children:
				actionId=int(eevent.id[0])
				libraryId=int(eevent.id[1])
				action = GameAction(self.gameFile)
				action.setMember("libraryId",libraryId)
				action.setMember("actionId",actionId)
				if libraryId==1:
					if actionId in GameAction.actionIdFunctionName:
						action.setMember("type",GameAction.EXEC_FUNCTION)
						action.setMember("functionName",GameAction.actionIdFunctionName[actionId])
						i=0
						for a in GameAction.actionIdArgumentKinds[actionId]:
							action.argumentKind[i]=a
							i+=1
						action.setMember("argumentsUsed",len(GameAction.actionIdArgumentKinds[actionId]))
						if actionId in GameAction.actionIdKind:
							action.setMember("kind",GameAction.actionIdKind[actionId])
						if actionId in GameAction.actionIdQuestion:
							action.setMember("question",GameAction.actionIdQuestion[actionId])
						if actionId in GameAction.actionIdMayBeRelative:
							action.setMember("mayBeRelative",GameAction.actionIdMayBeRelative[actionId])
					else:
						print_error("unsupported actionId "+str(actionId))
				else:
					print_error("unsupported libraryId "+str(libraryId))
				event.actions.append(action)
				if libraryId==1 and actionId==603:
					action.argumentValue[0]="".join(eevent.lineAttribs)
				else:
					for i in range(len(eevent.lineAttribs)):
						action.argumentValue[i]=eevent.lineAttribs[i].strip()
						if GameAction.actionIdArgumentKinds[actionId][i] in [GameAction.ArgumentKindSprite,GameAction.ArgumentKindSound,GameAction.ArgumentKindBackground,GameAction.ArgumentKindPath,
						GameAction.ArgumentKindScript,GameAction.ArgumentKindObject,GameAction.ArgumentKindRoom,GameAction.ArgumentKindFont,GameAction.ArgumentKindTimeline]:
							action.argumentValue[i]=str(action.GetArgumentReferenceName(i).getMember("id"))
				if len(action.argumentValue) != len(action.argumentKind):
					if action.actionId==603:
						code="\n".join(action.argumentValue)
						action.argumentValue=[code]
					else:
						print_error("argument length")
				for na in eevent.namedAttributes:
					nea = na.strip()
					if nea=="relative":
						action.setMember("relative",True)
			self.addEvent(event)

	def ReadGmx(self, gmkfile, gmxdir, name):
		tree=xml.etree.ElementTree.parse(os.path.join(gmxdir,name)+".object.gmx")
		root=tree.getroot()
		if root.tag!="object":
			print_error("tag isn't object "+root.tag)
		seen={}
		for child in root:
			if seen.get(child.tag,0)>0:
				print_error("duplicated tag "+child.tag)
			seen[child.tag]=seen.get(child.tag,0)+1
			if child.tag=="spriteName":
				self.setMember("spriteIndex",gmkfile.egmNameId[emptyTextToString(child.text)])
			elif child.tag=="solid":
				self.setMember("solid",bool(int(child.text)))
			elif child.tag=="visible":
				self.setMember("visible",bool(int(child.text)))
			elif child.tag=="depth":
				self.setMember("depth",int(child.text))
			elif child.tag=="persistent":
				self.setMember("persistent",bool(int(child.text)))
			elif child.tag=="parentName":
				self.setMember("parentIndex",gmkfile.egmNameId[emptyTextToString(child.text)])
			elif child.tag=="maskName":
				self.setMember("maskIndex",gmkfile.egmNameId[emptyTextToString(child.text)])
			elif child.tag=="events":
				for chil in child:
					if chil.tag=="event":
						event = GameEvent(self.gameFile)
						event.eventNumber = int(chil.attrib["eventtype"])
						if event.eventNumber==4:
							event.setMember("eventKind", gmkfile.egmNameId[chil.attrib["ename"]])
						else:
							event.setMember("eventKind", int(chil.attrib["enumb"]))
						for chile in chil:
							if chile.tag=="action":
								action = GameAction(self.gameFile)
								for chila in chile:
									if chila.tag=="libid":
										action.setMember("libraryId",int(chila.text))
									elif chila.tag=="id":
										action.setMember("actionId",int(chila.text))
									elif chila.tag=="kind":
										action.setMember("kind",int(chila.text))
									elif chila.tag=="userelative":
										action.setMember("mayBeRelative",bool(int(chila.text)))
									elif chila.tag=="isquestion":
										action.setMember("question",bool(int(chila.text)))
									elif chila.tag=="useapplyto":
										action.setMember("appliesToSomething",bool(int(chila.text)))
									elif chila.tag=="exetype":
										action.setMember("type",int(chila.text))
									elif chila.tag=="functionname":
										action.setMember("functionName",emptyTextToString(chila.text))
									elif chila.tag=="codestring":
										action.setMember("functionCode",emptyTextToString(chila.text))
									elif chila.tag=="whoName":
										if chila.text=="self":
											action.setMember("appliesToObject",GameObject.OBJECT_SELF)
										elif chila.text=="other":
											action.setMember("appliesToObject",GameObject.OBJECT_OTHER)
										else:
											print_error("gmx object applies to")
										#action.appliesToObject=int(chila.text)
									elif chila.tag=="relative":
										action.setMember("relative",bool(int(chila.text)))
									elif chila.tag=="isnot":
										action.setMember("notFlag",bool(int(chila.text)))
									elif chila.tag=="arguments":
										#<argument><kind>1</kind><string>010000000</string></argument><argument>
										if action.getMember("actionId")<100:
											print_error("unsupported actionId "+str(action.actionId))
										i=0
										for chilaa in chila:
											if chilaa.tag=="argument":
												if chilaa[0].tag!="kind":
													print_error("tag isn't kind "+chilaa[0].tag)
												kind=int(chilaa[0].text)
												action.argumentKind[i]=kind
												value=emptyTextToString(chilaa[1].text).strip()
												action.argumentValue[i]=value
												if kind in [GameAction.ArgumentKindSprite,GameAction.ArgumentKindSound,GameAction.ArgumentKindBackground,GameAction.ArgumentKindPath,
												GameAction.ArgumentKindScript,GameAction.ArgumentKindObject,GameAction.ArgumentKindRoom,GameAction.ArgumentKindFont,GameAction.ArgumentKindTimeline]:
													action.argumentValue[i]=str(action.GetArgumentReferenceName(i).getMember("id"))
												i+=1
									else:
										print_error("unsupported actions "+chila.tag)
								action.setMember("argumentsUsed",len(GameAction.actionIdArgumentKinds[action.getMember("actionId")]))
								event.actions.append(action)
							else:
								print_error("tag isn't action "+chile.tag)
						self.addEvent(event)
					else:
						print_error("tag isn't event "+chil.tag)
			elif child.tag=="PhysicsObject":
				self.setMember("PhysicsObject",int(child.text))
			elif child.tag=="PhysicsObjectSensor":
				self.setMember("PhysicsObjectSensor",int(child.text))
			elif child.tag=="PhysicsObjectShape":
				self.setMember("PhysicsObjectShape",int(child.text))
			elif child.tag=="PhysicsObjectDensity":
				self.setMember("PhysicsObjectDensity",gmxFloat(child.text))
			elif child.tag=="PhysicsObjectRestitution":
				self.setMember("PhysicsObjectRestitution",gmxFloat(child.text))
			elif child.tag=="PhysicsObjectGroup":
				self.setMember("PhysicsObjectGroup",int(child.text))
			elif child.tag=="PhysicsObjectLinearDamping":
				self.setMember("PhysicsObjectLinearDamping",gmxFloat(child.text))
			elif child.tag=="PhysicsObjectAngularDamping":
				self.setMember("PhysicsObjectAngularDamping",gmxFloat(child.text))
			elif child.tag=="PhysicsObjectFriction":
				self.setMember("PhysicsObjectFriction",gmxFloat(child.text))
			elif child.tag=="PhysicsObjectAwake":
				self.setMember("PhysicsObjectAwake",int(child.text))
			elif child.tag=="PhysicsObjectKinematic":
				self.setMember("PhysicsObjectKinematic",int(child.text))
			elif child.tag=="PhysicsShapePoints":
				for chil in child:
					print_warning("PhysicsShapePoints")
			else:
				print_error("unsupported tag "+child.tag)

	def ReadGmk(self, stream):
		if self.gameFile.gmkVersion>=800:
			objectStream = stream.Deserialize()
		else:
			objectStream = stream
		if not objectStream.ReadBoolean():
			self.exists = False
			return

		self.setMember("name",objectStream.ReadString())
		if self.gameFile.gmkVersion>=800:
			#last changed
			objectStream.ReadTimestamp()
		#GM version needed for the following info
		objectStream.ReadDword()
		self.setMember("spriteIndex",objectStream.readInt32())
		self.setMember("solid",objectStream.ReadBoolean())
		self.setMember("visible",objectStream.ReadBoolean())
		self.setMember("depth",objectStream.readInt32())
		self.setMember("persistent",objectStream.ReadBoolean())
		self.setMember("parentIndex",objectStream.readInt32())
		self.setMember("maskIndex",objectStream.readInt32())
		count = objectStream.ReadDword() + 1
		for i in range(count):
			while 1:
				first = objectStream.readInt32()

				if first == -1:
					break

				#12 MainEvents
				event = GameEvent(self.gameFile)
				event.eventNumber = i
				event.setMember("eventKind", first)

				#clifix Event Numb
				objectStream.ReadDword()

				actionCount = objectStream.ReadDword()
				while actionCount>0:
					action = GameAction(self.gameFile)
					action.ReadGmk(objectStream)

					event.actions.append(action)
					actionCount=actionCount-1

				self.addEvent(event)

	def ReadGGG(self, value):
		self.events=[]
		eventNumber=None
		eventKind=None
		event=None
		action=None
		codei=False
		code=""
		tabs=0
		i=0
		c=0
		n=value.find("\n")
		if n>-1:
			l=value[:n]
		else:
			l=value
		while c<len(value):
			if codei:
				i,level,plevel,type=GMLLexer(value[c:],"")
				codel=value[c:c+i-1]
				code=""
				for codel in codel.split("\n"):
					if codel.startswith("\t"*(tabs+2)):
						codel=codel[tabs+2:]
					code+=codel+"\n"
				c=c+i-1
			n=value.find("\n",c)
			if n>-1:
				l=value[c:n]
				chil=c
				c=n+1
			else:
				l=value[c:]
				chil=c
				c=len(value)
			a=l.replace(" ","").split()
			if len(a)>0 and a[0].startswith("@ev_"):
				if a[0][-1] != "{":
					print_error("line "+str(i)+" need { after @event")
				a[0]=a[0][:-1]
				eventName = a[0][4:].split("(")[0]
				eventNumber=GameEvent.eventNameNumber(eventName)
				if eventNumber>1:
					eventKind=a[0][4+len(eventName):]
					if eventKind[0] != "(":
						print_error("line "+str(i)+" need ( before eventKind")
					if eventKind[-1] != ")":
						print_error("line "+str(i)+" need ) after eventKind")
					eventKind=eventKind[1:-1]
					if eventNumber==6:
						eventKind=int(eventKind)
					else:
						eventKind = GameEvent.eventKindNumber(eventNumber,eventKind,self.gameFile)
				else:
					eventKind=0
				event = GameEvent(self.gameFile)
				event.eventNumber = eventNumber
				event.setMember("eventKind", eventKind)
				self.addEvent(event)
				codei=False
				tabs=l.count("\t")
			elif len(a)>0 and a[0].startswith("@action_"):
				action = a[0][1:]
				actionName = action.split("(")[0].strip()
				arguments = action[len(actionName):]
				if arguments[0] != "(":
					print_error("line "+str(i)+" need ( before arguments")
				if arguments[-1] != ")":
					print_error("line "+str(i)+" need ) after arguments")
				argumentsi=arguments[1:-1]
				error,arguments=GMLSplitArguments(argumentsi)
				if error:
					print_error("line "+str(i)+" "+error)
				action = GameAction(self.gameFile)
				event.actions.append(action)
				action.setMember("libraryId",1)
				actionId=GameAction.actionNameId(actionName)
				action.setMember("actionId",actionId)
				#action.setMember("appliesToSomething",True)
				if actionId in GameAction.actionIdKind:
					action.setMember("kind",GameAction.actionIdKind[actionId])
				action.setMember("functionName",actionName)
				for i in range(len(GameAction.actionIdArgumentKinds[actionId])):
					action.argumentKind[i]=GameAction.actionIdArgumentKinds[actionId][i]
					action.argumentValue[i]=arguments[i]
				action.setMember("argumentsUsed",len(GameAction.actionIdArgumentKinds[actionId]))
				if actionId in GameAction.actionIdQuestion:
					action.setMember("question",GameAction.actionIdQuestion[actionId])
				if actionId in GameAction.actionIdMayBeRelative:
					action.setMember("mayBeRelative",GameAction.actionIdMayBeRelative[actionId])
				if actionId in GameAction.actionIdType:
					action.setMember("type",GameAction.actionIdType[actionId])
				else:
					action.setMember("type",1)
				codei=False
				tabs=l.count("\t")
			elif len(a)>0 and a[0].startswith("@comment"):
				print_error("comment")
				codei=False
			elif len(a)>0 and a[0]=="@code{":
				print_notice("line "+str(i)+" start code action")
				codei=True
				tabs=l.count("\t")
			elif len(a)>0 and a[0]=="}":
				if codei:
					codei=False
					print_notice("line "+str(i)+" done code action")
				else:
					print_notice("line "+str(i)+" done event")
					eventNumber=None
					eventKind=None
				if code!="":
					action = GameAction(self.gameFile)
					event.actions.append(action)
					action.setMember("libraryId",1)
					actionId=603
					action.setMember("actionId",actionId)
					if actionId in GameAction.actionIdKind:
						action.setMember("kind",GameAction.actionIdKind[actionId])
					action.argumentValue[0]=code
					action.setMember("argumentsUsed",len(GameAction.actionIdArgumentKinds[actionId]))
					code=""
			elif len(a)>0 and a[0]=="":
				print_notice("line "+str(i)+" empty")
				pass
			else:
				if codei:
					print_error("code outside of code block")
					print_notice("line "+str(i)+" code")
				else:
					#print_error("line "+str(i)+" new "+a[0])
					i,level,plevel,type=GMLLexer(value[chil:],"")
					codel=value[chil:chil+i-1]
					code=""
					for codel in codel.split("\n"):
						if codel.startswith("\t"*(tabs+2)):
							codel=codel[tabs+2:]
						code+=codel+"\n"
					c=chil+i-1
			i+=1

	def WriteGmx(self, root):
		if self.getMember("sprite"):
			gmxCreateTag(root, "spriteName", self.getMember("sprite").getMember("name"))
		else:
			gmxCreateTag(root, "spriteName", "<undefined>")
		gmxCreateTag(root, "solid", str(boolToGmxIntbool(self.getMember("solid"))))
		gmxCreateTag(root, "visible", str(boolToGmxIntbool(self.getMember("visible"))))
		gmxCreateTag(root, "depth", str(self.getMember("depth")))
		gmxCreateTag(root, "persistent", str(boolToGmxIntbool(self.getMember("persistent"))))
		if self.getMember("parent"):
			gmxCreateTag(root, "parentName", self.getMember("parent").getMember("name"))
		else:
			gmxCreateTag(root, "parentName", "<undefined>")
		if self.getMember("mask"):
			gmxCreateTag(root, "maskName", self.getMember("mask").getMember("name"))
		else:
			gmxCreateTag(root, "maskName", "<undefined>")
		events=xml.etree.ElementTree.Element("events")
		events.tail="\n"
		root.append(events)
		for e in self.events:
			event=xml.etree.ElementTree.Element("event")
			event.tail="\n"
			events.append(event)
			event.set("eventtype", str(e.eventNumber))
			if e.eventNumber==4:
				event.set("ename", e.eventCollisionObjectName())
			else:
				event.set("enumb", str(e.getMember("eventKind")))
			for a in e.actions:
				action=xml.etree.ElementTree.Element("action")
				action.tail="\n"
				event.append(action)
				a.WriteGmx(action)
		gmxCreateTag(root, "PhysicsObject", str(self.getMember("PhysicsObject")))
		gmxCreateTag(root, "PhysicsObjectSensor", str(self.getMember("PhysicsObjectSensor")))
		gmxCreateTag(root, "PhysicsObjectShape", str(self.getMember("PhysicsObjectShape")))
		gmxCreateTag(root, "PhysicsObjectDensity", str(self.getMember("PhysicsObjectDensity")))
		gmxCreateTag(root, "PhysicsObjectRestitution", str(self.getMember("PhysicsObjectRestitution")))
		gmxCreateTag(root, "PhysicsObjectGroup", str(self.getMember("PhysicsObjectGroup")))
		gmxCreateTag(root, "PhysicsObjectLinearDamping", str(self.getMember("PhysicsObjectLinearDamping")))
		gmxCreateTag(root, "PhysicsObjectAngularDamping", str(self.getMember("PhysicsObjectAngularDamping")))
		gmxCreateTag(root, "PhysicsObjectFriction", str(self.getMember("PhysicsObjectFriction")))
		gmxCreateTag(root, "PhysicsObjectAwake", str(self.getMember("PhysicsObjectAwake")))
		gmxCreateTag(root, "PhysicsObjectKinematic", str(self.getMember("PhysicsObjectKinematic")))
		tag=xml.etree.ElementTree.Element("PhysicsShapePoints")
		tag.tail="\n"
		root.append(tag)

	def WriteGmk(self, stream):
		objectStream = BinaryStream()
		
		objectStream.WriteBoolean(self.exists)
		if self.exists:
			objectStream.WriteString(self.getMember("name"))
			objectStream.WriteTimestamp()
			objectStream.WriteDword(430)
			if self.getMember("sprite"):
				objectStream.WriteDword(self.getMember("sprite").getMember("id"))
			else:
				objectStream.WriteDword(GameObject.SpriteIndexNone)
			objectStream.WriteBoolean(self.getMember("solid"))
			objectStream.WriteBoolean(self.getMember("visible"))
			objectStream.WriteDword(self.getMember("depth"))
			objectStream.WriteBoolean(self.getMember("persistent"))
			if self.getMember("parent"):
				objectStream.WriteDword(self.getMember("parent").getMember("id"))
			else:
				objectStream.WriteDword(GameObject.ParentIndexNone)
			if self.getMember("mask"):
				objectStream.WriteDword(self.getMember("mask").getMember("id"))
			else:
				objectStream.WriteDword(GameObject.MaskIndexNone)

			objectStream.WriteDword(11)
			for i in range(12):
				for j in range(len(self.events)):
					if self.events[j].eventNumber == i:
						objectStream.WriteDword(self.events[j].getMember("eventKind"))
						objectStream.WriteDword(400)

						objectStream.WriteDword(len(self.events[j].actions))
						for k in range(len(self.events[j].actions)):
							self.events[j].actions[k].WriteGmk(objectStream)

				objectStream.WriteDword(-1)

		stream.Serialize(objectStream)
		
	def Finalize(self):
		if self.getMember("spriteIndex") != GameObject.SpriteIndexNone:
			self.setMember("sprite", self.gameFile.GetResource(GameSprite, self.getMember("spriteIndex")))
		if self.getMember("parentIndex") not in [GameObject.ParentIndexNone, -1]:
			self.setMember("parent", self.gameFile.GetResource(GameObject, self.getMember("parentIndex")))
		if self.getMember("maskIndex") != GameObject.MaskIndexNone:
			self.setMember("mask", self.gameFile.GetResource(GameSprite, self.getMember("maskIndex")))

		for i in range(len(self.events)):
			self.events[i].Finalize()
			for j in range(len(self.events[i].actions)):
				self.events[i].actions[j].Finalize()

	def WriteGGG(self, ful=True):
		stri=""
		if ful:
			stri="@object "+self.getMember("name")+" {\n"
		tab=""
		if ful:
			tab="\t"
			for key in self.members:
				if not self.ifDefault(key):
					stri+=tab+key+"="+str(self.getMember(key))+"\n"
		for o in self.events:
			stri=stri+tabStringLines(o.WriteGGG(),tab)
		if ful:
			stri+="}\n"
		return stri

	def WriteESObject(self):
		obj=ESObject()
		obj.name=self.getMember("name").encode()
		obj.id=self.getMember("id")
		obj.spriteId=self.getMemberId("sprite")
		obj.solid=self.getMember("solid")
		obj.visible=self.getMember("visible")
		obj.depth=self.getMember("depth")
		obj.persistent=self.getMember("persistent")
		obj.parentId=self.getMemberId("parent")
		obj.maskId=self.getMemberId("mask")
		obj.mainEventCount=12
		if obj.mainEventCount==0:
			return
		ot=(ESMainEvent*obj.mainEventCount)()
		mes={}
		for ec in self.events:
			if not ec.eventNumber in mes:
				mes[ec.eventNumber]=[]
			ev=ESEvent()
			ev.code = getActionsCode(ec.actions).encode()
			ev.id = ec.getMember("eventKind")
			mes[ec.eventNumber].append(ev)
		for count in range(obj.mainEventCount):
			es=mes.get(count,[])
			me=ESMainEvent()
			me.id=count
			me.eventCount=len(es)
			ote=(ESEvent*me.eventCount)()
			for counte in range(me.eventCount):
				ote[counte]=es[counte]
			me.events=cast(pointer(ote),POINTER(ESEvent))
			ot[count]=me
		obj.mainEvents=cast(ot,POINTER(ESMainEvent))
		return obj
