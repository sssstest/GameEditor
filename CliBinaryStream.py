#!/usr/bin/env python

from struct import *
import io
import zlib
import time
from CliPrintColors import *

class BinaryStream:
	def __init__(self, base_stream=None):
		if base_stream:
			self.base_stream = base_stream
		else:
			self.base_stream = io.BytesIO()

	def readByte(self):
		return self.base_stream.read(1)

	def readBytes(self, length):
		return self.base_stream.read(length)

	def readChar(self):
		return self.unpack('b')

	def readUChar(self):
		return self.unpack('B')

	def readBool(self):
		return self.unpack('?')

	def readInt16(self):
		return self.unpack('h', 2)

	def readUInt16(self):
		return self.unpack('H', 2)

	def readInt32(self):
		return self.unpack('i', 4)

	def readUInt32(self):
		return self.unpack('I', 4)

	def readInt64(self):
		return self.unpack('q', 8)

	def readUInt64(self):
		return self.unpack('Q', 8)

	def readFloat(self):
		return self.unpack('f', 4)

	def readDouble(self):
		return self.unpack('d', 8)

	def readString(self):
		length = self.readUInt16()
		if length>10000000:
			print_error("too big")
			sys.exit(1)
		return self.unpack(str(length) + 's', length).decode()

	def writeBytes(self, value):
		self.base_stream.write(value)

	def writeChar(self, value):
		self.pack('c', value)

	def writeUChar(self, value):
		self.pack('C', value)

	def writeBool(self, value):
		self.pack('?', value)

	def writeInt16(self, value):
		self.pack('h', value)

	def writeUInt16(self, value):
		self.pack('H', value)

	def writeInt32(self, value):
		self.pack('i', value)

	def writeUInt32(self, value):
		self.pack('I', value)

	def writeInt64(self, value):
		self.pack('q', value)

	def writeUInt64(self, value):
		self.pack('Q', value)

	def writeFloat(self, value):
		self.pack('f', value)

	def writeDouble(self, value):
		self.pack('d', value)

	def writeString(self, value):
		length = len(value)
		self.writeUInt16(length)
		self.pack(str(length) + 's', value)

	def pack(self, fmt, data):
		return self.writeBytes(pack(fmt, data))

	def unpack(self, fmt, length = 1):
		return unpack(fmt, self.readBytes(length))[0]

	def Read(self):
		value=self.base_stream.read()
		self.base_stream.seek(0)
		return value

	def Rewind(self):
		self.base_stream.seek(0)

	def Size(self):
		pos = self.base_stream.tell()
		self.base_stream.seek(0,2)
		length = self.base_stream.tell()
		self.base_stream.seek(pos)
		return length
	
	def EncodeBase64(self):
		import base64
		self.Rewind()
		return base64.encodestring(self.Read())

	def CompressBase64(self):
		import base64
		self.Rewind()
		return base64.encodestring(zlib.compress(self.Read()))

	def DecodeBase64(self):
		import base64
		self.Rewind()
		return base64.decodestring(self.Read())

	def DecompressBase64(self):
		import base64
		self.Rewind()
		return zlib.decompress(base64.decodestring(self.Read()))

	def Deflate(self):
		self.base_stream.seek(0)
		deflatedBuffer = zlib.compress(self.base_stream.read())
		self.base_stream = io.BytesIO()
		self.base_stream.write(deflatedBuffer)
		self.base_stream.seek(0)
		#self.position = 0

	def Inflate(self):
		inflatedBuffer = zlib.decompress(self.base_stream.read())
		self.base_stream = io.BytesIO()
		self.base_stream.write(inflatedBuffer)
		self.base_stream.seek(0)
		#self.position = 0

	def Deserialize(self, decompress=True):
		value = io.BytesIO()
		value = BinaryStream(value)

		length = self.readUInt32()

		tmpBuffer=self.readBytes(length)

		value.writeBytes(tmpBuffer)
		value.Rewind()
		if decompress:
			value.Inflate()
		return value

	def Serialize(self, stream, compress=True):
		if stream:
			if (compress):
				stream.Deflate()

			stream.base_stream.seek(0,2)
			length = stream.base_stream.tell()
			stream.base_stream.seek(0)

			self.WriteDword(length)
			self.writeBytes(stream.readBytes(length))
		else:
			self.WriteDword(0)

	def ReadDword(self):
		return self.readInt32()

	def ReadBoolean(self):
		return self.readUInt32()!=0

	def ReadString(self):
		length = self.readUInt32()
		return self.unpack(str(length) + 's', length).decode("iso8859-1")#windows-1252")

	def ReadTimestamp(self):
		GmTimestampEpoch = 0xFFFFFFFF7C5316BF
		return 86400.0 * self.readDouble() + GmTimestampEpoch

	def WriteDword(self, value):
		self.writeInt32(value)

	def WriteByte(self, value):
		self.writeChar(value)

	def WriteDouble(self, value):
		self.writeDouble(value)

	def WriteTimestamp(self):
		GmTimestampEpoch = 0xFFFFFFFF7C5316BF
		self.WriteDouble((time.time() - GmTimestampEpoch) / 86400.0)

	def WriteBoolean(self, value):
		self.WriteDword(int(bool(value)))

	def WriteString(self, value):
		length = len(value)
		self.WriteDword(length)
		self.pack(str(length) + 's', value)



