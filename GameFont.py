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

class GameFont(GameResource):
	if Class:
		#AntiAliasingLevel
		AaOff = 1
		Aa1 = 2
		Aa2 = 3
		Aa3 = 4

		#CharacterSet
		ANSI_CHARSET		= 0x00
		DEFAULT_CHARSET		= 0x00
		EASTEUROPE_CHARSET	= 0xEE
		RUSSIAN_CHARSET		= 0xCC
		SYMBOL_CHARSET		= 0x02
		SHIFTJIS_CHARSET	= 0x80
		HANGEUL_CHARSET		= 0x81
		GB2312_CHARSET		= 0x86
		CHINESEBIG5_CHARSET	= 0x88
		JOHAB_CHARSET		= 0x82
		HEWBREW_CHARSET		= 0xB1
		ARABIC_CHARSET		= 0xB2
		GREEK_CHARSET		= 0xA1
		TURKISH_CHARSET		= 0xA2
		VIETNAMESE_CHARSET	= 0xA3
		THAI_CHARSET		= 0xDE
		MAC_CHARSET			= 0x4D
		BALTIC_CHARSET		= 0xBA
		OEM_CHARSET			= 0xFF

	defaults={"id":-1,"name":"noname","fontName":"","size":12,"bold":False,"italic":False,
	"characterRangeBegin":32,"characterRangeEnd":127,"characterSet":DEFAULT_CHARSET,"antiAliasing":Aa3}

	def __init__(self, gameFile, id):
		GameResource.__init__(self, gameFile, id)
		self.setMember("name","font_"+str(id))

	def ReadEgm(self, entry, z):
		stream=z.open(entry+".ey", "r")
		y=YamlParser()
		r=y.parseStream(stream)
		self.setMember("name",os.path.split(entry)[1])
		self.setMember("fontName",r.getMstr("font_name"))
		self.setMember("bold",r.getMbool("bold"))
		self.setMember("italic",r.getMbool("italic"))
		self.setMember("size",r.getMint("size"))
		self.setMember("characterRangeBegin",r.getMint("range_min"))
		self.setMember("characterRangeEnd",r.getMint("range_max"))
		self.setMember("characterSet",r.getMint("charset"))
		self.setMember("antiAliasing",r.getMint("antialias"))

	def ReadGmx(self, gmkfile, gmxdir, name):
		tree=xml.etree.ElementTree.parse(os.path.join(gmxdir, name)+".font.gmx")
		root=tree.getroot()
		if root.tag!="font":
			print_error("tag isn't font "+root.tag)
		seen={}
		for child in root:
			if seen.get(child.tag,0)>0:
				print_error("duplicated tag "+child.tag)
			seen[child.tag]=seen.get(child.tag, 0)+1
			if child.tag=="name":
				self.setMember("fontName", emptyTextToString(child.text))
			elif child.tag=="size":
				self.setMember("size", int(child.text))
			elif child.tag=="bold":
				self.setMember("bold", bool(int(child.text)))
			elif child.tag=="italic":
				self.setMember("italic", bool(int(child.text)))
			elif child.tag=="charset":
				self.setMember("characterSet", int(child.text))
			elif child.tag=="aa":
				self.setMember("antiAliasing", int(child.text))
			elif child.tag=="texgroups":
				#<texgroup0>0</texgroup0>
				pass
			elif child.tag=="first":
				self.setMember("characterRangeBegin", int(child.text))
			elif child.tag=="last":
				self.setMember("characterRangeEnd", int(child.text))
			elif child.tag=="texgroup":
				pass
			elif child.tag=="ranges":
				#<range0>32,127</range0>
				child=child[0]
				b,e=child.text.split(",")
				self.setMember("characterRangeBegin", int(b))
				self.setMember("characterRangeEnd", int(e))
			elif child.tag=="glyphs":
				#<glyph character="113" x="11" y="54" w="7" h="17" shift="9" offset="1"/>
				pass
			elif child.tag=="kerningPairs":
				pass
			elif child.tag=="image":
				pass
			else:
				print_error("unsupported tag "+child.tag)

	def ReadGmk(self, stream):
		fontStream = stream.Deserialize()
		if not fontStream.ReadBoolean():
			self.exists = False
			return
		self.setMember("name",fontStream.ReadString())
		fontStream.ReadTimestamp()
		fontStream.ReadDword()
		self.setMember("fontName",fontStream.ReadString())
		self.setMember("size",fontStream.ReadDword())
		self.setMember("bold",fontStream.ReadBoolean())
		self.setMember("italic",fontStream.ReadBoolean())
		value=fontStream.ReadDword()
		self.setMember("characterSet",(value >> 16) & 0xFF)
		self.setMember("antiAliasing",(value >> 24) & 0xFF)
		self.setMember("characterRangeBegin",value & 0xFFFF)
		self.setMember("characterRangeEnd",fontStream.ReadDword())

	def WriteGmx(self, root):
		gmxCreateTag(root, "name", self.getMember("fontName"))
		gmxCreateTag(root, "size", str(self.getMember("size")))
		gmxCreateTag(root, "bold", str(boolToGmxIntbool(self.getMember("bold"))))
		gmxCreateTag(root, "italic", str(boolToGmxIntbool(self.getMember("italic"))))
		gmxCreateTag(root, "charset", str(self.getMember("characterSet")))
		gmxCreateTag(root, "aa", str(self.getMember("antiAliasing")))
		tag=xml.etree.ElementTree.Element("texgroups")
		tag.tail="\n"
		root.append(tag)
		tag=xml.etree.ElementTree.Element("ranges")
		tag.tail="\n"
		root.append(tag)
		gmxCreateTag(tag, "range0", str(self.getMember("characterRangeBegin"))+","+str(self.getMember("characterRangeEnd")))
		tag=xml.etree.ElementTree.Element("glyphs")
		tag.tail="\n"
		root.append(tag)
		tag=xml.etree.ElementTree.Element("kerningPairs")
		tag.tail="\n"
		root.append(tag)
		gmxCreateTag(root, "image", "")

	def WriteGmk(self, stream):
		fontStream = BinaryStream()
		fontStream.WriteBoolean(self.exists)
		fontStream.WriteString(self.getMember("name"))
		fontStream.WriteTimestamp()
		fontStream.WriteDword(800)
		fontStream.WriteString(self.getMember("fontName"))
		fontStream.WriteDword(self.getMember("size"))
		fontStream.WriteBoolean(self.getMember("bold"))
		fontStream.WriteBoolean(self.getMember("italic"))
		value = 0
		value |= (self.getMember("characterSet") & 0xFF) << 16
		value |= (self.getMember("antiAliasing") & 0xFF) << 24
		value |= self.getMember("characterRangeBegin") & 0xFFFF
		fontStream.WriteDword(value)
		fontStream.WriteDword(self.getMember("characterRangeEnd"))
		stream.Serialize(fontStream)

	def WriteGGG(self):
		stri="@font "+self.getMember("name")+" {\n"
		for key in self.members:
			if not self.ifDefault(key):
				stri+="\t"+key+"="+str(self.getMember(key))+"\n"
		stri+="}\n"
		return stri
