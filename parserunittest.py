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

import unittest
from dejavu.parser import *

def parseGML(code):
	tokens = token_stream(code+" ")
	parser2 = parser(tokens, error_printer(build_log()))
	return parser2.getprogram()

class TestCase(unittest.TestCase):
	def testDeclarationAssignment(self):
		p = parseGML("var x=2;")
		self.assertEqual(type(p.stmts[0].stmts[0]), declaration)
		self.assertEqual(type(p.stmts[0].stmts[1]), assignment)

	def testForMissingSemicolons(self):
		p = parseGML("for (a=0 b<10 c++) d=e;")
		self.assertEqual(p.stmts[0].cond.op, less)

	def testForMissingSemicolons2(self):
		p = parseGML("for (a=0 a=10 a=7) b. /* Comment for no reason */ room_speed = c;")
		self.assertEqual(p.stmts[0].cond.op, is_equals)

	def testForMissingSemicolons3(self):
		p = parseGML("for (int i = 0 i < lives; i += 1) {}")
		self.assertEqual(p.stmts[0].cond.op, less)

	def testEmptyFor(self):
		p = parseGML("for (;;) {}")
		self.assertEqual(len(p.stmts[0].stmt.stmts), 0)

	def testEmptyFor2(self):
		p = parseGML("for (;;;) {}")
		self.assertEqual(len(p.stmts[0].stmt.stmts), 0)

	def nottestForMissingSemicolonsInvalidGML(self):
		p = parseGML("for a=0 a<10 a++ b=c;")
		self.assertEqual(p.stmts[0].cond.op, less)

	def testNotEquals(self):
		p = parseGML("if (x<>y) then {}")
		self.assertEqual(p.stmts[0].cond.op, not_equals)

	def test2Blocks(self):
		p = parseGML("{x=1;}{x=2;}")
		self.assertEqual(p.stmts[1].stmts[0].rvalue.t.real, 2)

	def testDeclarationNoSemicolon(self):
		p = parseGML("int x = (y+z)\ns(t);")
		self.assertEqual(type(p.stmts[1]), invocation)

	def testElse(self):
		p = parseGML("if(sound_isplaying(argument0)) sound_seek(argument0,0) else sound_play(argument0);")
		self.assertEqual(type(p.stmts[0].branch_false), invocation)

	def testMultidimensionalArray(self):
		p = parseGML("x=y[10,20];")
		self.assertEqual(p.stmts[0].rvalue.indices[1].t.real, 20)

	def testIfCall(self):
		p = parseGML("if (keyboard_check(vk_space)) {}")
		self.assertEqual(p.stmts[0].cond.args[0].t.namekey, "vk_space")

	def testGlobalDeclaration(self):
		p = parseGML("global int z=2;")
		self.assertEqual(p.stmts[0].stmts[1].rvalue.t.real, 2)

	def testGlobalExpression(self):
		p = parseGML("global.x=2;")
		self.assertEqual(p.stmts[0].lvalue.op, dot)

	def testGlobalvarIllegalAssignment(self):
		p = parseGML("globalvar x=2;")

	def testAssignments(self):
		p = parseGML("a=2/*test*/z=2;")

	def testTernary(self):
		p = parseGML("x = (y == 0) ? 1 : 2;")
		self.assertEqual(p.stmts[0].rvalue.cond.op, is_equals)

	def testHex(self):
		p = parseGML("x = 0xa;")
		self.assertEqual(p.stmts[0].rvalue.t.real, 10)

	def testHex2(self):
		p = parseGML("x = $a;")
		self.assertEqual(p.stmts[0].rvalue.t.real, 10)

#https://code.google.com/p/game-creator/source/browse/GameCreator.Test/GmlTest.cs
	def VerifyExpressionString(str, expected):
		self.assertEqual(expected, parseGML(str).toGML());

	def VerifyStatementString(str, expected):
		self.assertEqual(expected, parseGML(str).toGMLMinifier());

	def testParseEmptyExpression(self):
		p = parseGML("  /* Empty expression */  ")
		self.assertEqual(len(p.stmts), 0)

	def nottestParseIdentifier(self):
		p = parseGML("abc")
		self.assertEqual(p.stmts[0], "abc")

	def nottestBlockToString(self):
		p = parseGML(" { a=3; } ")
		generated = "{\r\n    a = 3;\r\n}\r\n";
		self.assertEqual(generated, p.toGML())

		minified = "{a=3;}";
		self.assertEqual(minified, p.toGMLMinifier())

	def nottestExpressionToString(self):
		self.VerifyExpressionString("a");
		self.VerifyExpressionString("a + 1");
		self.VerifyExpressionString("a + (3 * 2)");
		self.VerifyExpressionString("(a - 1) / t");
		self.VerifyExpressionString("a == 1");

		self.VerifyExpressionString("a <> 1", "a != 1");
		self.VerifyExpressionString("a mod 3");
		self.VerifyExpressionString("a and 1", "a && 1");
		self.VerifyExpressionString("a xor b", "a ^^ b");

	def nottestStatementToString(self):
		self.VerifyStatementString("a := 0",                                                 "a=0;");
		self.VerifyStatementString("if t then x = 3",                                        "if(t)x=3;");
		self.VerifyStatementString("if t then begin x := 3 y = 4 end",                       "if(t){x=3;y=4;}");
		self.VerifyStatementString("for ({case 2:};0;exit)t=3",                              "for({case 2:};0;exit)t=3;");
		self.VerifyStatementString("for (repeat 5 i = 0;;;;; i < 3; globalvar;;;;;)a=3",     "for(repeat(5)i=0;;i<3;globalvar)a=3;");
		self.VerifyStatementString("for (i := 0 i<3; {case 3:exit};;;)string(4);",           "for(i=0;i<3;{case 3:exit;})string(4);");

if __name__ == "__main__":
	unittest.main()
