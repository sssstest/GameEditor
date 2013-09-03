#!/usr/bin/env python

import sys
import subprocess

args=[]
for arg in sys.argv[1:]:
	if arg=="GMODE=Compile":
		args.append("GMODE=Debug")
	else:
		args.append(arg)
sys.exit(subprocess.check_call(["/usr/bin/make"]+args))
