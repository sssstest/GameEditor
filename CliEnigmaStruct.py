#!/usr/bin/env python

#* converted to python from https://github.com/enigma-dev/enigma-dev/blob/master/CompilerSource/backend/EnigmaStruct.h

#* Copyright (C) 2010 IsmAvatar <IsmAvatar@gmail.com>, Josh Ventura
#*
#* Enigma Plugin is free software and comes with ABSOLUTELY NO WARRANTY.
#* See LICENSE for details.

from ctypes import *

c_intbool		= c_int
emode_run		= 0
emode_debug		= 1
emode_design		= 2
emode_compile	= 3
emode_rebuild		= 4

class ESSubImage(Structure):
	_fields_=[("width",c_int),
	("height",c_int),
	("data",c_char_p),
	("dataSize",c_int)]

class ESBackground(Structure):
	_fields_=[("name",c_char_p),
	("id",c_int),
	("transparent",c_intbool),
	("smoothEdges",c_intbool),
	("preload",c_intbool),
	("useAsTileset",c_intbool),
	("tileWidth",c_int),
	("tileHeight",c_int),
	("hOffset",c_int),
	("vOffset",c_int),
	("hSep",c_int),
	("vSep",c_int),
	("backgroundImage",ESSubImage)]

class ESPathPoint(Structure):
	_fields_=[("x",c_int),
	("y",c_int),
	("speed",c_int)]

class ESPath(Structure):
	_fields_=[("name",c_char_p),
	("id",c_int),
	("smooth",c_intbool),
	("closed",c_intbool),
	("precision",c_int),
	("snapX",c_int),
	("snapY",c_int),
	("points",POINTER(ESPathPoint)),
	("pointCount",c_int)]

class ESMoment(Structure):
	_fields_=[("stepNo",c_int),
	("code",c_char_p)]

class ESTimeline(Structure):
	_fields_=[("name",c_char_p),
	("id",c_int),
	("moments",POINTER(ESMoment)),
	("momentCount",c_int)]

class ESSound(Structure):
	_fields_=[("name",c_char_p),
	("id",c_int),
	("kind",c_int),
	("fileType",c_char_p),
	("fileName",c_char_p),
	("chorus",c_intbool),
	("echo",c_intbool),
	("flanger",c_intbool),
	("gargle",c_intbool),
	("reverb",c_intbool),
	("volume",c_double),
	("pan",c_double),
	("preload",c_intbool),
	("data",c_char_p),
	("size",c_int)]

class ESGlyph(Structure):
	_fields_=[("origin",c_double),
	("baseline",c_double),
	("advance",c_double),
	("width",c_int),
	("height",c_int),
	("data",c_char_p)]

class ESFont(Structure):
	_fields_=[("name",c_char_p),
	("id",c_int),
	("fontName",c_char_p),
	("size",c_int),
	("bold",c_intbool),
	("italic",c_intbool),
	("rangeMin",c_int),
	("rangeMax",c_int),
	("glyphs",POINTER(ESGlyph))]

class ESPoint(Structure):
	_fields_=[("x",c_int),
	("y",c_int)]

class ESPolygon(Structure):
	_fields_=[("points",POINTER(ESPoint)),
	("pointCount",c_int)]

class ESSprite(Structure):
	_fields_=[("name",c_char_p),
	("id",c_int),
	("transparent",c_intbool),
	("shape",c_int),
	("alphaTolerance",c_int),
	("separateMask",c_intbool),
	("smoothEdges",c_intbool),
	("preload",c_intbool),
	("originX",c_int),
	("originY",c_int),
	("bbMode",c_int),
	("bbLeft",c_int),
	("bbRight",c_int),
	("bbTop",c_int),
	("bbBottom",c_int),
	("subImages",POINTER(ESSubImage)),
	("subImageCount",c_int),
	("maskShapes",POINTER(ESPolygon)),
	("maskShapeCount",c_int)]

class ESScript(Structure):
	_fields_ = [("name", c_char_p),
	("id", c_int),
	("code", c_char_p)]

class ESShader(Structure):
	_fields_ = [("name", c_char_p),
	("id", c_int),
	("vertex", c_char_p),
	("fragment", c_char_p),
	("type", c_char_p),
	("precompile", c_intbool)]

class ESEvent(Structure):
	_fields_ = [("id", c_int),
	("code", c_char_p)]

	# mouse event types
	EV_LEFT_BUTTON = 0
	EV_RIGHT_BUTTON = 1
	EV_MIDDLE_BUTTON = 2
	EV_NO_BUTTON = 3
	EV_LEFT_PRESS = 4
	EV_RIGHT_PRESS = 5
	EV_MIDDLE_PRESS = 6
	EV_LEFT_RELEASE = 7
	EV_RIGHT_RELEASE = 8
	EV_MIDDLE_RELEASE = 9
	EV_MOUSE_ENTER = 10
	EV_MOUSE_LEAVE = 11
	EV_MOUSE_WHEEL_UP = 60
	EV_MOUSE_WHEEL_DOWN = 61
	EV_GLOBAL_LEFT_BUTTON = 50
	EV_GLOBAL_RIGHT_BUTTON = 51
	EV_GLOBAL_MIDDLE_BUTTON = 52
	EV_GLOBAL_LEFT_PRESS = 53
	EV_GLOBAL_RIGHT_PRESS = 54
	EV_GLOBAL_MIDDLE_PRESS = 55
	EV_GLOBAL_LEFT_RELEASE = 56
	EV_GLOBAL_RIGHT_RELEASE = 57
	EV_GLOBAL_MIDDLE_RELEASE = 58
	EV_JOYSTICK1_LEFT = 16
	EV_JOYSTICK1_RIGHT = 17
	EV_JOYSTICK1_UP = 18
	EV_JOYSTICK1_DOWN = 19
	EV_JOYSTICK1_BUTTON1 = 21
	EV_JOYSTICK1_BUTTON2 = 22
	EV_JOYSTICK1_BUTTON3 = 23
	EV_JOYSTICK1_BUTTON4 = 24
	EV_JOYSTICK1_BUTTON5 = 25
	EV_JOYSTICK1_BUTTON6 = 26
	EV_JOYSTICK1_BUTTON7 = 27
	EV_JOYSTICK1_BUTTON8 = 28
	EV_JOYSTICK2_LEFT = 31
	EV_JOYSTICK2_RIGHT = 32
	EV_JOYSTICK2_UP = 33
	EV_JOYSTICK2_DOWN = 34
	EV_JOYSTICK2_BUTTON1 = 36
	EV_JOYSTICK2_BUTTON2 = 37
	EV_JOYSTICK2_BUTTON3 = 38
	EV_JOYSTICK2_BUTTON4 = 39
	EV_JOYSTICK2_BUTTON5 = 40
	EV_JOYSTICK2_BUTTON6 = 41
	EV_JOYSTICK2_BUTTON7 = 42
	EV_JOYSTICK2_BUTTON8 = 43

	# other event types
	EV_OUTSIDE = 0
	EV_BOUNDARY = 1
	EV_GAME_START = 2
	EV_GAME_END = 3
	EV_ROOM_START = 4
	EV_ROOM_END = 5
	EV_NO_MORE_LIVES = 6
	EV_NO_MORE_HEALTH = 9
	EV_ANIMATION_END = 7
	EV_END_OF_PATH = 8
	EV_USER0 = 10
	EV_USER1 = 11
	EV_USER2 = 12
	EV_USER3 = 13
	EV_USER4 = 14
	EV_USER5 = 15
	EV_USER6 = 16
	EV_USER7 = 17
	EV_USER8 = 18
	EV_USER9 = 19
	EV_USER10 = 20
	EV_USER11 = 21
	EV_USER12 = 22
	EV_USER13 = 23
	EV_USER14 = 24
	EV_USER15 = 25

	# step event types
	EV_STEP_NORMAL = 0
	EV_STEP_BEGIN = 1
	EV_STEP_END = 2

	#alarm event types
	EV_ALARM0 = 0
	EV_ALARM1 = 1
	EV_ALARM2 = 2
	EV_ALARM3 = 3
	EV_ALARM4 = 4
	EV_ALARM5 = 5
	EV_ALARM6 = 6
	EV_ALARM7 = 7
	EV_ALARM8 = 8
	EV_ALARM9 = 9
	EV_ALARM10 = 10
	EV_ALARM11 = 11

class ESMainEvent(Structure):
	_fields_ = [("id", c_int),
	("events", POINTER(ESEvent)),
	("eventCount", c_int)]

	EV_CREATE = 0
	EV_DESTROY = 1
	EV_ALARM = 2
	EV_STEP = 3
	EV_COLLISION = 4
	EV_KEYBOARD = 5
	EV_MOUSE = 6
	EV_OTHER = 7
	EV_DRAW = 8
	EV_KEYPRESS = 9
	EV_KEYRELEASE = 10
	EV_TRIGGER = 11

class ESObject(Structure):
	_fields_ = [("name", c_char_p),
	("id", c_int),
	("spriteId", c_int),
	("solid", c_intbool),
	("visible", c_intbool),
	("depth", c_int),
	("persistent", c_intbool),
	("parentId", c_int),
	("maskId", c_int),
	("mainEvents", POINTER(ESMainEvent)),
	("mainEventCount", c_int)]

class ESRoomBackground(Structure):
	_fields_ = [("visible", c_intbool),
	("foreground", c_intbool),
	("x", c_int),
	("y", c_int),
	("tileHoriz", c_intbool),
	("tileVert", c_intbool),
	("hSpeed", c_int),
	("vSpeed", c_int),
	("stretch", c_intbool),
	("backgroundId", c_int)]

class ESRoomView(Structure):
	_fields_ = [("visible", c_intbool),
	("viewX", c_int),
	("viewY", c_int),
	("viewW", c_int),
	("viewH", c_int),
	("portX", c_int),
	("portY", c_int),
	("portW", c_int),
	("portH", c_int),
	("borderH", c_int),
	("borderV", c_int),
	("speedH", c_int),
	("speedV", c_int),
	("objectId", c_int)]

class ESRoomInstance(Structure):
	_fields_ = [("x", c_int),
	("y", c_int),
	("objectId", c_int),
	("id", c_int),
	("creationCode", c_char_p),
	("locked", c_intbool)]

class ESRoomTile(Structure):
	_fields_ = [("bgX", c_int),
	("bgY", c_int),
	("roomX", c_int),
	("roomY", c_int),
	("width", c_int),
	("height", c_int),
	("depth", c_int),
	("backgroundId", c_int),
	("id", c_int),
	("locked", c_intbool)]

class ESRoom(Structure):
	_fields_ = [("name", c_char_p),
	("id", c_int),
	("caption", c_char_p),
	("width", c_int),
	("height", c_int),

	("snapX", c_int),
	("snapY", c_int),
	("isometric", c_intbool),

	("speed", c_int),
	("persistent", c_intbool),
	("backgroundColor", c_int),
	("drawBackgroundColor", c_intbool),
	("creationCode", c_char_p),

	("rememberWindowSize", c_intbool),
	("editorWidth", c_int),
	("editorHeight", c_int),
	("showGrid", c_intbool),
	("showObjects", c_intbool),
	("showTiles", c_intbool),
	("showBackgrounds", c_intbool),
	("showViews", c_intbool),
	("deleteUnderlyingObjects", c_intbool),
	("deleteUnderlyingTiles", c_intbool),
	("currentTab", c_int),
	("scrollBarX", c_int),
	("scrollBarY", c_int),

	("enableViews", c_intbool),

	("backgroundDefs", POINTER(ESRoomBackground)),
	("backgroundDefCount", c_int),
	("views", POINTER(ESRoomView)),
	("viewCount", c_int),
	("instances", POINTER(ESRoomInstance)),
	("instanceCount", c_int),
	("tiles", POINTER(ESRoomTile)),
	("tileCount", c_int)]

class ESGameSettings(Structure):
	_fields_ = [("gameId", c_int),
	("startFullscreen", c_intbool),
	("interpolate", c_intbool),
	("dontDrawBorder", c_intbool),
	("displayCursor", c_intbool),
	("scaling", c_int),
	("allowWindowResize", c_intbool),
	("alwaysOnTop", c_intbool),
	("colorOutsideRoom", c_uint),
	("setResolution", c_intbool),
	("colorDepth", c_byte),
	("resolution", c_byte),
	("frequency", c_byte),
	("dontShowButtons", c_intbool),
	("useSynchronization", c_intbool),
	("disableScreensavers", c_intbool),
	("letF4SwitchFullscreen", c_intbool),
	("letF1ShowGameInfo", c_intbool),
	("letEscEndGame", c_intbool),
	("letF5SaveF6Load", c_intbool),
	("letF9Screenshot", c_intbool),
	("treatCloseAsEscape", c_intbool),
	("gamePriority", c_byte),
	("freezeOnLoseFocus", c_intbool),
	("loadBarMode", c_byte),
	("showCustomLoadImage", c_intbool),
	("imagePartiallyTransparent", c_intbool),
	("loadImageAlpha", c_int),
	("scaleProgressBar", c_intbool),
	("displayErrors", c_intbool),
	("writeToLog", c_intbool),
	("abortOnError", c_intbool),
	("treatUninitializedAs0", c_intbool),
	("author", c_char_p),
	("version", c_char_p),
	("lastChanged", c_double),
	("information", c_char_p),

	("includeFolder", c_int),
	("overwriteExisting", c_intbool),
	("removeAtGameEnd", c_intbool),

	("versionMajor", c_int),
	("versionMinor", c_int),
	("versionRelease", c_int),
	("versionBuild", c_int),
	("company", c_char_p),
	("product", c_char_p),
	("copyright", c_char_p),
	("description", c_char_p),

	("gameIcon", c_char_p)]

class ESConstant(Structure):
	_fields_ = [("name", c_char_p),
	("value", c_char_p)]

class ESExtension(Structure):
	_fields_ = [("name", c_char_p),
	("path", c_char_p)]

class ESInclude(Structure):
	_fields_ = [("filepath", c_char_p)]

class ESTrigger(Structure):
	_fields_ = [("name", c_char_p),
	("condition", c_char_p),
	("checkStep", c_int),
	("constant", c_char_p)]

class EnigmaStruct(Structure):
	_fields_ = [("fileVersion", c_int),
	("filename", c_char_p),
	("sprites", POINTER(ESSprite)),
	("spriteCount", c_int),
	("sounds", POINTER(ESSound)),
	("soundCount", c_int),
	("backgrounds", POINTER(ESBackground)),
	("backgroundCount", c_int),
	("paths", POINTER(ESPath)),
	("pathCount", c_int),
	("scripts", POINTER(ESScript)),
	("scriptCount", c_int),
	("shaders", POINTER(ESShader)),
	("shaderCount", c_int),
	("fonts", POINTER(ESFont)),
	("fontCount", c_int),
	("timelines", POINTER(ESTimeline)),
	("timelineCount", c_int),
	("gmObjects", POINTER(ESObject)),
	("gmObjectCount", c_int),
	("rooms", POINTER(ESRoom)),
	("roomCount", c_int),
	("triggers", POINTER(ESTrigger)),
	("triggerCount", c_int),
	("constants", POINTER(ESConstant)),
	("constantCount", c_int),
	("includes", POINTER(ESInclude)),
	("includeCount", c_int),
	("packages", POINTER(c_char_p)),
	("packageCount", c_int),
	("extensions", POINTER(ESExtension)),
	("extensionCount", c_int),

	("gameSettings", ESGameSettings),
	("lastInstanceId", c_int),
	("lastTileId", c_int)]

class EnigmaCallbacks(Structure):
	_fields_ = [
	#Opens the EnigmaFrame
	#void (*dia_open) ();
	("dia_open", CFUNCTYPE(c_voidp)),

	#Appends a given text to the frame log
	#void (*dia_add) (const char *);
	("dia_add", CFUNCTYPE(c_voidp, c_char_p)),

	#Clears the frame log
	#void (*dia_clear) ();
	("dia_clear", CFUNCTYPE(c_voidp)),

	#Sets the progress bar (0-100)
	#void (*dia_progress) (int);
	("dia_progress", CFUNCTYPE(c_voidp, c_int)),

	#Applies a given text to the progress bar
	#void (*dia_progress_text) (const char *);
	("dia_progress_text", CFUNCTYPE(c_voidp, c_char_p)),

	#Sets the file from which data is redirected to frame log
	#void (*output_redirect_file) (const char *);
	("output_redirect_file", CFUNCTYPE(c_voidp, c_char_p)),

	#Indicates file completion, dumps remainder to frame log
	#void (*output_redirect_reset) ();
	("output_redirect_reset", CFUNCTYPE(c_voidp)),

	#Executes a given command, returns errors or ret val
	#int (*ide_execute) (const char*, const char**, bool);
	("ide_execute", CFUNCTYPE(c_int, c_char_p, POINTER(c_char_p), c_intbool)),

	#Compresses data. Note image width/height unused
	#Image* (*ide_compress_data) (char *, int);
	("ide_compress_data", CFUNCTYPE(c_int, c_char_p, c_int))]

class syntax_error(Structure):
	_fields_ = [("err_str", c_char_p),#/< The text associated with the error.
	("line", c_int),#/< The line number on which the error occurred.
	("position", c_int),#/< The column number in the line at which the error occurred.
	("absolute_index", c_int)]#/< The zero-based position in the entire code at which the error occurred.



