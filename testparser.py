#!/usr/bin/env python

import dejavu.parser
import sys

if __name__=="__main__":
	if len(sys.argv)>1:
		for file in sys.argv[1:]:
			#print(file)
			code=open(file).read()
			print(dejavu.parser.parseGML(file, code))
