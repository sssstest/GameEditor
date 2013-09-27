#!/usr/bin/env python

#* @file printcolors.cpp
#* @brief Source file of various print functions with color.
#*
#* Write a description about the file here...
#*
#* @section License
#*
#* Copyright (C) 2013 Robert B. Colton
#*
#* This file is a part of the ENIGMA Development Environment.
#*
#* ENIGMA is free software: you can redistribute it and/or modify it under the
#* terms of the GNU General Public License as published by the Free Software
#* Foundation, version 3 of the license or any later version.
#*
#* This application and its source code is distributed AS-IS, WITHOUT ANY
#* WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#* FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
#* details.
#*
#* You should have received a copy of the GNU General Public License along
#* with this code. If not, see <http://www.gnu.org/licenses/>

from __future__ import print_function
import sys
import os
import traceback

RESET          = 0
BRIGHT         = 1
DIM            = 2
UNDERLINE      = 3
BLINK          = 4
REVERSE        = 7
HIDDEN         = 8

BLACK          = 0
RED            = 1
GREEN          = 2
YELLOW         = 3
BLUE           = 4
MAGENTA        = 5
CYAN           = 6
WHITE          = 7

def setRealStdout(stdout):
	global realStdout
	realStdout=stdout

def RGBA2DWORD(iR, iG, iB, iA):
	return (((((iR << 8) + iG) << 8) + iB) << 8) + iA

def textcolor(attr, fg, bg):
	if os.name!="nt":
		print("%c[%d;%d;%dm" % (0x1B, attr, fg + 30, bg + 40), end=" ", file=realStdout)

def textcolorbg(attr, bg):
	if os.name!="nt":
		print("%c[%d;%dm" % (0x1B, attr, bg + 40), end=" ", file=realStdout)

def textcolorfg(attr, fg):
	if os.name!="nt":
		print("%c[%d;%dm" % (0x1B, attr, fg + 30), end=" ", file=realStdout)

def textcolorreset():
	if os.name!="nt":
		print("%c[%dm" % (0x1B, colorCodes.RESET), end=" ", file=realStdout)

def printfln(msg):
	print(msg, file=realStdout)

def println():
	print("", file=realStdout)

def printcolor(msg, attr, fg):
	textcolorfg(attr, fg)
	print(msg, end=" ", file=realStdout)

def printfcln(msg, attr, fg):
	printcolor(msg, attr, fg)
	println()

def printfc(msg, attr, bg, fg):
	textcolor(attr, fg, bg)
	print(msg, file=realStdout)

def clearconsole():
	if os.name!="nt":
		print("\e[1;1H\e[2J", file=realStdout)

def print_error(msg):
	printcolor("ERROR ", BRIGHT, RED)
	printfcln(msg, RESET, WHITE)
	traceback.print_stack(file=sys.stdout)

def print_warning(msg):
	printcolor("WARNING ", BRIGHT, YELLOW)
	printfcln(msg, RESET, WHITE)

def print_notice(msg):
	printcolor("NOTICE ", BRIGHT, GREEN)
	printfcln(msg, RESET, WHITE)
