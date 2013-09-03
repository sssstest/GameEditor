#!/usr/bin/env python

#* converted to python from https://github.com/enigma-dev/enigma-dev/blob/master/pluginsource/org/enigma/file/ApngIO.java

#* Copyright (C) 2011,2012 IsmAvatar <IsmAvatar@gmail.com>
#* Copyright (C) 2011 Josh Ventura <JoshV10@gmail.com>
#* 
#* Enigma Plugin is free software and comes with ABSOLUTELY NO WARRANTY.
#* See LICENSE for details.

import zlib
import cStringIO

class ApngIO(object):
	PNG_SIGNATURE = "".join([ chr(0x89),'P','N','G',chr(0x0D),chr(0x0A),chr(0x1A),chr(0x0A) ])
	IO_FMT = "png"

	#Convenience byte[]/int methods
	@staticmethod
	def bite(i, p):
		return i >> p & 0xFF

	@staticmethod
	def i2b(i):
		return [ chr(ApngIO.bite(i,24)),chr(ApngIO.bite(i,16)),chr(ApngIO.bite(i,8)),chr(ApngIO.bite(i,0)) ]

	#* Convenience method to fully read a buffer, since in.read(buf) can fall short. */
	@staticmethod
	def readFully(inp, length):
		return ApngIO.readFully4(inp,0,length)

	@staticmethod
	def readFully4(inp, off, length):
		total = 0
		while True:
			buffer = inp.read(length)
			n=len(buffer)
			if n <= 0:
				if total == 0: total = n
				break
			total += n
			if total == length: break
		return buffer

	#Functionality
	def transferIDATs(dis, os, sn, ignoreOthers):
		chunk = Generic_Chunk()
		while chunk.read(dis) and not chunk.isType(IEND.type):
			if chunk.isType(IDAT.type):
				if sn == -1:
					os.write(chunk)
				else:
					os.write(fdAT(chunk,sn).getBytes())
			elif not ignoreOthers:
				os.write(chunk.getBytes())

	def imagesToApng(self, imgs, fullFile):
		baos = ByteArrayOutputStream()
		ImageIO.write(imgs.get(0),IO_FMT,baos)
		buf = baos.toByteArray()
		myhdr = IHDR_Dummy(buf)
		myactl = acTL(imgs.size(),0)
		fctl = fcTL(0,imgs.get(0).getWidth(),imgs.get(0).getHeight(),0,0,1,30,
				fcTL.Dispose.BACKGROUND,fcTL.Blend.OVER)

		fullFile.write(PNG_SIGNATURE)
		fullFile.write(myhdr.getBytes())
		fullFile.write(myactl.getBytes())
		fullFile.write(fctl.getBytes())

		#Transfer the IDAT chunks
		bais = ByteArrayInputStream(buf)
		bais.skip(8)
		self.transferIDATs(bais,fullFile,-1,True)

		indx = -1
		for bi in imgs:
			if indx == -1: # Continues once to skip the first image;
				indx+=1
				continue # index will be 1 on first iteration
			indx+=1

			baos.reset() # Clear our buffer,
			ImageIO.write(bi,IO_FMT,baos) # Fetch new image.

			# Create the frame control. IDs will be 2, 4, 6, 8...
			fctl = fcTL(indx,bi.getWidth(),bi.getHeight(),0,0,1,30,
					fcTL.Dispose.BACKGROUND,fcTL.Blend.OVER)
			indx+=1
			fullFile.write(fctl.getBytes()) # Write it into the file

			# Now make our frame data. IDs will be 3, 5, 7, 9...
			buf= baos.toByteArray()
			bais = ByteArrayInputStream(buf)
			bais.skip(8)
			self.transferIDATs(bais,fullFile,indx,true)
		fullFile.write(IEND.instance.getBytes())

	def apngToBufferedImages(self, ist):
		genChunk = Generic_Chunk()
		png = cStringIO.StringIO()#ByteArrayOutputStream()
		ret = []
		imageHeader=[]

		png.write(ApngIO.PNG_SIGNATURE)

		pngBase=ist.read(8)
		if not pngBase==ApngIO.PNG_SIGNATURE: raise "Not APNG"

		hasData = False

		while genChunk.read(ist):
			if genChunk.isType(acTL.type):
				pass
			elif genChunk.isType(fcTL.type):
				if hasData:
					png.write(IEND.instance.getBytes())
					png.seek(0)
					bais = cStringIO.StringIO(png.read())
					ret.append(bais)

					png.reset()
					png.write(pngBase)
					png.write(imageHeader)
					hasData = False
			elif genChunk.isType(IDAT.type):
				png.write(genChunk.getBytes())
				hasData = True
			elif genChunk.isType(fdAT.type):
				a = fdAT(genChunk).toIDAT().getBytes()
				png.write(a)
				hasData = True
			elif genChunk.isType(IEND.type):
				png.write(genChunk.getBytes())
				png.seek(0)
				bais = cStringIO.StringIO(png.read())
				ret.append(bais)
				break
			elif genChunk.isType(IHDR_Dummy.type):
				#save the image header as it is used for all subimages
				imageHeader=genChunk.getBytes()
				png.write(imageHeader)
			else:
				png.write(genChunk.getBytes())
		return ret

class ApngChunkType(object):
		def __init__(self, bytes):
			self.data = bytes
			self.val = self.bytesToInt(bytes)

		def getBytes(self):
			return self.data

		def bytesToInt(self, b):
			if len(b) != 4: raise "ArrayIndexOutOfBoundsException"
			return ord(b[0]) << 24 | ord(b[1]) << 16 | ord(b[2]) << 8 | ord(b[3])

		def equals(self, other):
			return self.val == other.val

class PNG_Chunk(object):
	length = 0

	def __init__(self, type=None):
		self.chunkType = type

	def updateCRC(self):
		tcrc = zlib.crc32("".join(self.chunkType.getBytes())+"".join(self.data)) & 0xFFFFFFFF
		self.length = len(self.data)
		self.crc = ApngIO.i2b(tcrc)

	def getBytes(self):
		#Get the bytes of this chunk for writing
		baos = cStringIO.StringIO()

		baos.write("".join(ApngIO.i2b(self.length)))
		baos.write("".join(self.chunkType.getBytes()))
		baos.write("".join(self.data))
		baos.write("".join(self.crc))

		baos.seek(0)
		return baos.read()

	def isType(self, t):
		if self.chunkType == None:
			return False
		else:
			return self.chunkType.equals(t)

	def read(self, dis):
		b1=dis.read(1)
		if b1=="": return False
		b1 = ord(b1)
		if b1 == -1: return False
		self.length = (b1 << 24) | (ord(dis.read(1)) << 16) | (ord(dis.read(1)) << 8) | ord(dis.read(1))
		chunkTypeBytes=ApngIO.readFully(dis,4)
		self.chunkType = ApngChunkType(chunkTypeBytes)
		self.data=ApngIO.readFully(dis,self.length)
		self.crc=ApngIO.readFully(dis,4);
		return True

class Generic_Chunk(PNG_Chunk):
	def __init__(self):
		PNG_Chunk.__init__(self)

	def repopulate(self):
		print "Repopulate called on generic chunk."

class IHDR_Dummy(PNG_Chunk):
	type = ApngChunkType([ 'I','H','D','R' ])

	def __init__(self, png):
		PNG_Chunk.__init__(self)
		self.data = [0]*13
		System.arraycopy(png,16,data,0,data.length)
		self.repopulate()

	def repopulate(self):
		self.updateCRC()

class acTL(PNG_Chunk):
	type = ApngChunkType([ 'a','c','T','L' ])

	def __init__(self, nf, np):
		PNG_Chunk.__init__(self)
		self.numFrames = nf
		self.numPlays = np
		self.repopulate()

	def repopulate(self):
		self.data = [ self.bite(self.numFrames,24),self.bite(self.numFrames,16),self.bite(self.numFrames,8),
				self.bite(self.numFrames,0),self.bite(self.numPlays,24),self.bite(self.numPlays,16),self.bite(self.numPlays,8),self.bite(self.numPlays,0) ]
		self.updateCRC()

class fcTL(PNG_Chunk):
	type = ApngChunkType([ 'f','c','T','L' ])

	def __init__(self, sn, w, h, xo, yo, dn, dd, dop, bop):
		PNG_Chunk.__init__(self)
		self.chunkType = ApngChunkType([ 'f','c','T','L' ])
		self.sequenceNumber = sn
		self.width = w
		self.height = h
		self.xOffset = xo
		self.yOffset = yo
		self.delayNum = dn
		self.delayDen = dd
		self.disposeOp = dop
		self.blendOp = bop
		self.repopulate()

	#enum Dispose
	#* No disposal is done on this frame before rendering the next;
	#* the contents of the output buffer are left as-is.
	NONE=0
	#* The frame's region of the output buffer is to be cleared
	#* to fully transparent black before rendering the next frame.
	BACKGROUND=1
	#* The frame's region of the output buffer is to be reverted
	#* to the previous contents before rendering the next frame.
	PREVIOUS=2

	#enum Blend
	#* All color components of the frame, including alpha, overwrite
	#* the current contents of the frame's output buffer region.
	SOURCE=0
	#* The frame should be composited onto the output buffer
	#* based on its alpha, using a simple OVER operation
	#* as described in the "Alpha Channel Processing" section
	#* of the PNG specification [PNG-1.2].
	OVER=1

	def repopulate(self):
		self.data = [ self.bite(self.sequenceNumber,24),self.bite(self.sequenceNumber,16),self.bite(self.sequenceNumber,8),
				self.bite(self.sequenceNumber,0),self.bite(self.width,24),self.bite(self.width,16),self.bite(self.width,8),self.bite(self.width,0),
				self.bite(self.height,24),self.bite(self.height,16),self.bite(self.height,8),self.bite(self.height,0),self.bite(self.xOffset,24),
				self.bite(self.xOffset,16),self.bite(self.xOffset,8),self.bite(self.xOffset,0),self.bite(self.yOffset,24),self.bite(self.yOffset,16),
				self.bite(self.yOffset,8),self.bite(self.yOffset,0),self.bite(self.delayNum,8),self.bite(self.delayNum,0),self.bite(self.delayDen,8),
				self.bite(self.delayDen,0),self.disposeOp.getValue(),self.blendOp.getValue() ]
		self.updateCRC()

class IDAT(PNG_Chunk):
	type = ApngChunkType([ 'I','D','A','T' ])

	#* Creates a new IDAT chunk with the given frame data. */
	def __init__(self, dat):
		PNG_Chunk.__init__(self)
		self.chunkType = ApngChunkType([ 'I','D','A','T' ])
		self.data = dat
		self.repopulate()

	def repopulate(self):
		self.updateCRC()

class fdAT(PNG_Chunk):
	type = ApngChunkType([ 'f','d','A','T' ])

	#* Creates an fdAT from a PNG_Chunk that is already in fdAT format.
	#* Namely, it extracts the sequence number from the frame data.
	def __init__(self, pc, sn=None):
		PNG_Chunk.__init__(self)
		self.chunkType = ApngChunkType([ 'f','d','A','T' ])
		self.length = pc.length
		if sn:
			#* Creates an fdAT from a PNG_Chunk that is in another format (converts it) */
			self.sequenceNumber = sn
			self.frameData = pc.data #will just be arraycopy'd anyways
			self.repopulate()
			return
		self.sequenceNumber = ord(pc.data[0]) << 24 | ord(pc.data[1]) << 16 | ord(pc.data[2]) << 8 | ord(pc.data[3])
		self.frameData = [0]*(len(pc.data) - 4)
		for i in xrange(len(self.frameData)):
			self.frameData[i]=pc.data[4+i]
		self.crc = pc.crc

	def repopulate(self):
		self.data = [0]*(len(self.frameData) + 4)
		for i in xrange(4):
			self.data[i]=ApngIO.i2b(self.sequenceNumber)[i]
		for i in xrange(len(self.frameData)):
			self.data[4+i]=self.frameData[i]
		self.updateCRC()

	def toIDAT(self):
		return IDAT(self.frameData)

class IEND(PNG_Chunk):
	type = ApngChunkType([ 'I','E','N','D' ])

	#* IEND is a singleton class and should not be instantiated.
	#* Use IEND.instance instead.
	def __init__(self):
		PNG_Chunk.__init__(self)
		self.chunkType = ApngChunkType([ 'I','E','N','D' ])
		self.repopulate()

	def repopulate(self):
		self.data = []
		self.updateCRC()

IEND.instance = IEND()