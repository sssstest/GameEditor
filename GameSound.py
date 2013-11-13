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

class GameSound(GameResource):
	if Class:
		KindNormal=0
		KindBackground=1
		Kind3D=2
		KindMultimedia=3

		EffectNone				= 0x00
		EffectChorus			= 0x01
		EffectEcho				= 0x02
		EffectFlanger			= 0x04
		EffectGargle			= 0x08
		EffectReverb			= 0x10

	defaults={"id":-1,"name":"noname","kind":KindNormal,
	"extension":"","origname":"","effects":EffectNone,
	"volume":1.0,"pan":0.0,"mp3BitRate":0,"oggQuality":0,"preload":True,"data":None,
	"bitRate":192,"sampleRate":44100,"type":0,"bitDepth":16,"compressed":0,"streamed":0,"uncompressOnLoad":0}

	def __init__(self, gameFile, id):
		GameResource.__init__(self, gameFile, id)
		self.setMember("name","sound_"+str(id))

	def ReadEgm(self, entry, z):
		stream=z.open(entry+".ey", "r")
		y=YamlParser()
		r=y.parseStream(stream)
		self.setMember("name",os.path.split(entry)[1])
		self.setMember("kind",r.getMkind("KIND"))
		self.setMember("extension",r.getMstr("FILE_TYPE"))
		self.setMember("origname",r.getMstr("FILE_NAME"))
		#CHORUS: false
		#ECHO: false
		#FLANGER: false
		#GARGLE: false
		#REVERB: false
		#self.effects			= r.getMbool("START_FULLSCREEN")
		self.setMember("volume",r.getMreal("VOLUME"))
		self.setMember("pan",r.getMreal("PAN"))
		self.setMember("preload",r.getMbool("PRELOAD"))
		data=r.getMstr("Data")
		data=z.open(os.path.split(entry)[0]+"/"+data, "r")#.read()
		data=data.read()
		self.setMember("data",BinaryStream(io.BytesIO(data)))

	def ReadGmx(self, gmkfile, gmxdir, name):
		tree=xml.etree.ElementTree.parse(os.path.join(gmxdir,name)+".sound.gmx")
		root=tree.getroot()
		if root.tag!="sound":
			print_error("tag isn't sound "+root.tag)
		seen={}
		for child in root:
			if seen.get(child.tag,0)>0:
				print_error("duplicated tag "+child.tag)
			seen[child.tag]=seen.get(child.tag,0)+1
			if child.tag=="kind":
				self.setMember("kind",int(child.text))
			elif child.tag=="extension":
				self.setMember("extension",emptyTextToString(child.text))
			elif child.tag=="origname":
				self.setMember("origname",emptyTextToString(child.text))
			elif child.tag=="effects":
				self.setMember("effects",int(child.text))
			elif child.tag=="volume":
				if len(child)>0 and child[0].tag=="volume":
					child=child[0]
				self.setMember("volume",gmxFloat(child.text))
			elif child.tag=="pan":
				self.setMember("pan",gmxFloat(child.text))
			elif child.tag=="mp3BitRate":
				self.setMember("mp3BitRate",int(child.text))
			elif child.tag=="oggQuality":
				self.setMember("oggQuality",int(child.text))
			elif child.tag=="bitRates":
				if len(child)>0 and child[0].tag=="bitRate":
					child=child[0]
				self.setMember("bitRate",int(child.text))
			elif child.tag=="sampleRates":
				if len(child)>0 and child[0].tag=="sampleRate":
					child=child[0]
				self.setMember("sampleRate",int(child.text))
			elif child.tag=="types":
				if len(child)>0 and child[0].tag=="type":
					child=child[0]
				self.setMember("type",int(child.text))
			elif child.tag=="bitDepths":
				if len(child)>0 and child[0].tag=="bitDepth":
					child=child[0]
				self.setMember("bitDepth",int(child.text))
			elif child.tag=="preload":
				self.setMember("preload",bool(int(child.text)))
			elif child.tag=="compressed":
				self.setMember("compressed",int(child.text))
			elif child.tag=="streamed":
				self.setMember("streamed",int(child.text))
			elif child.tag=="uncompressOnLoad":
				self.setMember("uncompressOnLoad",int(child.text))
			elif child.tag=="data":#<data>snd_0.wav</data>
				name=emptyTextToString(child.text)
				data=open(os.path.join(gmxdir, "audio", name), "rb")
				data=data.read()
				self.setMember("data",BinaryStream(io.BytesIO(data)))
			else:
				print_error("unsupported tag "+child.tag)

	def ReadGmk(self, stream):
		if self.gameFile.gmkVersion>=800:
			soundStream = stream.Deserialize()
		else:
			soundStream = stream
		if not soundStream.ReadBoolean():
			self.exists = False
			return
		self.setMember("name",soundStream.ReadString())
		if self.gameFile.gmkVersion>=800:
			soundStream.ReadTimestamp()
		gmVersion=soundStream.ReadDword()
		self.setMember("kind",soundStream.ReadDword())
		self.setMember("extension",soundStream.ReadString())
		if self.gameFile.gmkVersion==440:
			print_error("440")
		else:
			self.setMember("origname",soundStream.ReadString())
			if soundStream.ReadBoolean():
				self.setMember("data",soundStream.Deserialize(False))
			self.setMember("effects",soundStream.ReadDword())
			self.setMember("volume",soundStream.readDouble())
			self.setMember("pan",soundStream.readDouble())
			self.setMember("preload",soundStream.ReadBoolean())

	def WriteGmx(self, root):
		gmxCreateTag(root, "kind", str(self.getMember("kind")))
		gmxCreateTag(root, "extension", self.getMember("extension"))
		gmxCreateTag(root, "origname", self.getMember("origname"))
		gmxCreateTag(root, "effects", str(self.getMember("effects")))
		tag=xml.etree.ElementTree.Element("volume")
		tag.tail="\n"
		root.append(tag)
		gmxCreateTag(tag, "volume", str(self.getMember("volume")))
		gmxCreateTag(root, "pan", str(self.getMember("pan")))
		tag=xml.etree.ElementTree.Element("bitRates")
		tag.tail="\n"
		root.append(tag)
		gmxCreateTag(tag, "bitRate", str(self.getMember("bitRate")))
		tag=xml.etree.ElementTree.Element("sampleRates")
		tag.tail="\n"
		root.append(tag)
		gmxCreateTag(tag, "sampleRate", str(self.getMember("sampleRate")))
		tag=xml.etree.ElementTree.Element("types")
		tag.tail="\n"
		root.append(tag)
		#0 Mono 1 Stereo 2 3D
		gmxCreateTag(tag, "type", str(self.getMember("type")))
		tag=xml.etree.ElementTree.Element("bitDepths")
		tag.tail="\n"
		root.append(tag)
		gmxCreateTag(tag, "bitDepth", str(self.getMember("bitDepth")))
		gmxCreateTag(root, "preload", str(boolToGmxIntbool(self.getMember("preload"))))
		gmxCreateTag(root, "compressed", str(self.getMember("compressed")))
		gmxCreateTag(root, "streamed", str(self.getMember("streamed")))
		gmxCreateTag(root, "uncompressOnLoad", str(self.getMember("uncompressOnLoad")))
		if self.getMember("data") and len(self.getMember("data"))>0:
			raise 4

	def WriteGmk(self, stream):
		soundStream = BinaryStream()
		soundStream.WriteBoolean(self.exists)
		if self.exists:
			soundStream.WriteString(self.getMember("name"))
			soundStream.WriteTimestamp()
			soundStream.WriteDword(800)
			soundStream.WriteDword(self.getMember("kind"))
			soundStream.WriteString(self.getMember("extension"))
			soundStream.WriteString(self.getMember("origname"))
			if self.getMember("data") and self.getMember("data").Size()>0:
				soundStream.WriteBoolean(True)
				soundStream.Serialize(self.getMember("data"), False)
			else:
				soundStream.WriteBoolean(False)
			soundStream.WriteDword(self.getMember("effects"))
			soundStream.WriteDouble(self.getMember("volume"))
			soundStream.WriteDouble(self.getMember("pan"))
			soundStream.WriteBoolean(self.getMember("preload"))
		stream.Serialize(soundStream)

	def WriteGGG(self):
		stri="@sound "+self.getMember("name")+" {\n"
		for key in self.members:
			if not self.ifDefault(key):
				if key != "data":
					stri+="\t"+key+"="+str(self.getMember(key))+"\n"
		stri+="\t@data {\n"+str(self.getMember("data").CompressBase64().decode())+"}\n"
		stri+="}\n"
		return stri

	def WriteESSound(self):
		os=ESSound()
		os.name = self.getMember("name").encode()
		os.id = self.getMember("id")
		os.kind = self.getMember("kind")
		os.fileType = self.getMember("extension").encode()
		os.fileName = self.getMember("origname").encode()
		os.chorus = False
		os.echo = False
		os.flanger = False
		os.gargle = False
		os.reverb = False
		os.volume = self.getMember("volume")
		os.pan = self.getMember("pan")
		os.preload = self.getMember("preload")
		if self.getMember("data") == None:
			os.size = 0
			return os
		self.getMember("data").base_stream.seek(0)
		data = self.getMember("data").base_stream.read()
		os.data = data
		os.size = len(data)
		return os
