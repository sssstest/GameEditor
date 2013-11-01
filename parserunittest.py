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
from dejavu.printer import *

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

#http://enigma-dev.org/docs/Wiki/Tutorial:Moving_from_GML_to_EDL
	def testStrings(self):
		#Inherit strings from GML ('A'="A") or from C++ ('A'=65)
		#In C++, individual characters ('A') are a native type that resolves directly to a number (their ordinal value), whereas strings ("A") conclude with an invisible null terminator (\0).
		#if you actually want the ordinal value of of character, you may simply name the character, and don't need to pass it through the ord() function.
		#On the downside, 'A' != "A", because char and string don't compare right. 
		p = parseGML("if 'A'=\"A\" {}")
		self.assertEqual(p.stmts[0].cond.left.t.type, "string")

	def testEscape(self):
		#Inherit escape sequences from GML (#) or from C++ (\n)
		#In GML, to create a newline, you simply insert a number sign (#) into your string. To draw a literal number sign, double it (##), thus # acts as a kind of escape character.
		p = parseGML('a="#";b="##";')

	def testPrefix(self):
		#Inherit ++/-- from GML (+) or from C++ (+=1/-=1)
		#In GML, this gets interpreted as <set b equal to> <whatever is before the -- (0)> <minus> <negative> <value of a (10)>.
		#b = 0 - -a;
		#The result is that a = 10; b = 10;
		#In C++, the results are a = 9; b = 9;
		#Note that if we had done postfix instead, the results would have been a = 9; b = 10;. 
		p = parseGML("a = 10;b = --a;")
		#self.assertEqual(p.stmts[0].rvalue.op, is_equals)

	def testEqualsLexical(self):
		#Inherit a=b=c from GML (a=b==c) or from C++ (b=c,a=c)
		p = parseGML("a=b=c;")
		self.assertEqual(p.stmts[0].rvalue.op, is_equals)

#http://enigma-dev.org/docs/Wiki/Discarded_behaviors
	def testEmptyFor(self):
		p = parseGML("for (;;) {}")
		self.assertEqual(len(p.stmts[0].stmt.stmts), 0)

	def testEmptyFor2(self):
		p = parseGML("for (;;;) {}")
		self.assertEqual(len(p.stmts[0].stmt.stmts), 0)

	def testValidFor1(self):
		p = parseGML("for (i = 0; i < 10; i += 1;) {}")

	def testInvalidFor(self):
		p = parseGML("for (i = 0; i < 10; i += 1);")

	def testValidFor2(self):
		p = parseGML("for ({statement1 = 0; statement2 = 0; statement3 = 0; i = 0;}; i < 10; {statement1 += 1; statement2 += 2; statement3 += 3; i += 1; }) {}")

	def nottestInvalidDo(self):
		p = parseGML("with(all) do { x += 1; } until (place_free(x,y));")

	def testStringRepeat(self):
		#In GM8, 5 * "tree" yields "treetreetreetreetree".
		p = parseGML('a = 5 * "tree"')

	def nottestDeclarationCommaFree(self):
		#GM doesn't care if you use commas in your declarations or not
		p = parseGML("var a b c, d e f, g h i\nif (j == k + l) {};")

	def testDeclarationSyntaxError(self):
		p = parseGML("var a b c\na = 10;")

	def testDelphiAssignmentInConditionals(self):
		p = parseGML("if (a := b) {};")
		self.assertEqual(p.stmts[0].cond.op, is_equals)

	def testSemicolonBetweenStatements(self):
		p = parseGML("if (a) { }; ; ; ; ; ; else {} ")
		self.assertEqual(len(p.stmts[0].branch_false.stmts), 0)

#https://code.google.com/p/game-creator/source/browse/GameCreator.Test/GmlTest.cs
	def VerifyExpressionString(self, str, expected):
		self.assertEqual("show("+expected+");\n", printer.toGML(parseGML("show("+str+");")))

	def VerifyStatementString(self, str, expected):
		self.assertEqual(expected, printer.toGMLMinifier(parseGML(str)))

	def VerifyExpressionString2(self, str):
		self.assertEqual("show("+str+");\n", printer.toGML(parseGML("show("+str+");")))

	def VerifyStatementString2(self, str):
		self.assertEqual(str, printer.toGMLMinifier(parseGML(str)))

	def testParseEmptyExpression(self):
		p = parseGML("  /* Empty expression */  ")
		self.assertEqual(len(p.stmts), 0)

	def nottestParseIdentifier(self):
		p = parseGML("abc")
		self.assertEqual(p.stmts[0], "abc")

	def testBlockToString(self):
		p = parseGML(" { a=3; } ")
		generated = "{\n    a = 3;\n}\n";
		self.assertEqual(generated, printer.toGML(p))

		#minified = "{a=3;}";
		#self.assertEqual(minified, printer.toGMLMinifier(p))

	def testExpressionToString(self):
		self.VerifyExpressionString2("a");
		self.VerifyExpressionString2("a + 1");
		#self.VerifyExpressionString2("a + (3 * 2)");
		self.VerifyExpressionString2("(a - 1) / t");
		self.VerifyExpressionString2("a == 1");

		self.VerifyExpressionString("a <> 1", "a != 1");
		self.VerifyExpressionString2("a mod 3");
		self.VerifyExpressionString("a and 1", "a && 1");
		self.VerifyExpressionString("a xor b", "a ^^ b");

	def testStatementToString(self):
		self.VerifyStatementString("a := 0",                                                 "a=0;");
		self.VerifyStatementString("if t then x = 3",                                        "if(t)x=3;");
		self.VerifyStatementString("if t then begin x := 3 y = 4 end",                       "if(t){x=3;y=4;}");
		#self.VerifyStatementString("for ({case 2:};0;exit)t=3",                              "for({case 2:};0;exit)t=3;");
		#self.VerifyStatementString("for (repeat 5 i = 0;;;;; i < 3; globalvar;;;;;)a=3",     "for(repeat(5)i=0;;i<3;globalvar)a=3;");
		self.VerifyStatementString("for (i := 0 i<3; {case 3:exit};;;)string(4);",           "for(i=0;i<3;{case 3:exit;})string(4);");

if __name__ == "__main__":
	unittest.main()
