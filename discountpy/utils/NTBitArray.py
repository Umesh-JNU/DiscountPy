import numpy as np
from discountpy.utils.BitRepresentation import _quadToByte, bytesToString, complementOne, G

class _NTBitArray:
	def encode(self, data: str) -> ...:
		buf = self.longBuffer(len(data))
		longIdx = 0
		quadOffset = 0
		while longIdx < len(buf):
			quadIdx = 0
			qshift = 56
			x = 0
			while quadIdx < 8 and quadOffset < len(data):
				quad = _quadToByte(data, quadOffset)
				x |= (quad & 255) << qshift

				qshift -= 8
				quadIdx += 1
				quadOffset += 4
			
			buf[longIdx] = x
			longIdx += 1
		
		return ZeroNTBitArray(buf, len(data))

	def longBuffer(self, size: int) -> np.array([], dtype=np.int64):
		numLongs = (size >> 5) if(size % 32 == 0) else (size >> 5) + 1
		return np.zeros(numLongs, dtype=np.int64)

#   /**
#	* Shift an array of two-bits one step to the left, dropping one bp, and inserting another on the right.
#	* @return
#	*/
#   def shiftLongArrayKmerLeft(data: Array[Long], newBP: Byte, k: Int): Array[Long] = {
#	 val n = data.length
#	 val r = new Array[Long](n)
#	 var i = 0
#	 while (i < n) {
#	   if (i < n - 1) {
#		 r(i) = (data(i) << 2) | (data(i + 1) >>> 62)
#	   } else {
#		 r(i) = (data(i) << 2) | (newBP.toLong << ((32 - (k % 32)) * 2))
#	   }
#	   i += 1
#	 }
#	 r
#   }

	def longsToString(self, data: np.array([], np.int64), offset: int, size: int) -> str:
		sb = ''
		byte = (size // 4) if (size % 32 == 0) else (size // 4 + 8)
		return self._longsToString(byte, sb, data, offset, size)

	"""
	Optimised version for repeated calls - avoids allocating a new buffer each time
	"""
	def _longsToString(self, byte: int, builder: str, data: np.array([], np.int64), offset: int, size: int) -> str:
		data.newbyteorder().byteswap(inplace=True)
		buffer = bytearray(data)
		data.newbyteorder().byteswap(inplace=True)
		return bytesToString(buffer, builder, offset, size)

	
	
class NTBitArray(_NTBitArray):
	"""
	A bit-packed array of nucleotides, where each letter is represented by two bits
	"""
	__slots__ = ['data', 'offset', 'size', 'toString']

	"""Array of longs, each storing up to 16 nts, with optional padding at the end."""
	data: np.array([], dtype=np.int64)

	"""Offset into the array where data starts (in NTs)"""
	offset: int

	"""Size of the data represented (in NTs)"""
	size: int

	toString: str

	def __init__(self, data: np.array([], dtype=np.int64), offset: int, size: int):
		self.data = data
		self.offset = offset
		self.size = size
		self.toString = self.longsToString(data, offset, size)

	"""Construct a new NTBitArray from a subsequence of this one."""
	def slice(self, start: int, length: int) -> ...:
		return self.OffsetNTBitArray(self.data, start, length)

	"""
	Obtain the (twobit) NT at a given offset.
	Only the lowest two bits of the byte are valid. The others will be zeroed out.
	"""
	def apply(self, pos: int) -> bytes:
		truePos = self.offset + pos
		lng = truePos // 32
		lval = self.data[lng]
		localOffset = truePos % 32

		return np.int64((lval >> (2 * (31 - localOffset))) & 0x3).tobytes()

	"""
	Test the orientation of a slice of this buffer.
	:param pos: Start position
	:param size: Length of slice (must be an odd number)
	:return: True iff this slice has forward orientation.
	"""
	def sliceIsForwardOrientation(self, pos: int, size: int) -> bool:
		st = pos
		end = pos + size - 1
		while (st < end):
			a = self.apply(st)
			b = complementOne(self.apply(end))
			if (a < b): return True
			if (a > b): return False

			st += 1
			end -= 1

		# Here, st == end
		# Resolve a nearly palindromic case, such as: AACTT whose r.c. is AAGTT
		return self.apply(st) < G

	"""
	Obtain all k-mers from this buffer.
	:param k: int
	:param onlyForwardOrientation: bool = If this flag is true, only k-mers with forward orientation will be returned.
	:return: forward orientation 
	"""
	def kmers(self, k: int, onlyForwardOrientation: bool = False) -> iter:
		return map(lambda i: slice(i, k), 
			filter(lambda i: (not onlyForwardOrientation) or self.sliceIsForwardOrientation(i, k), 
			(i for i in range(self.offset, self.size - k + 1))))

	"""
	Obtain all k-mers from this buffer, packed as Array[Long].
	:param k
	:param onlyForwardOrientation If this flag is true, only k-mers with forward orientation will be returned.
	:return
	"""
	def kmersAsLongArrays(self, k: int, onlyForwardOrientation: bool = False) -> iter:
		return filter(lambda _: _ != None, self.__kmersAsLongArraysOrientationMatch__(k, onlyForwardOrientation))

	# def __kmersAsLongArraysOrientationMatch__(self, k: int, onlyForwardOrientation: bool = False) -> iter: 
	#	 new Iterator[Array[Long]] {
	#	 var lastKmer = partAsLongArray(offset, k)
	#	 var i = offset

	#	 def hasNext: Boolean = i < (NTBitArray.this.size - k + 1)

	#	 def next: Array[Long] = {
	#		 if (i > offset) {
	#		 lastKmer = shiftLongArrayKmerLeft(lastKmer, apply(i - 1 + k), k)
	#		 }
	#		 i += 1
	#		 if (!onlyForwardOrientation || sliceIsForwardOrientation(i - 1, k)) {
	#		 lastKmer
	#		 } else {
	#		 null
	#		 }
	#	 }
	# }


	"""
	Create a long array representing a subsequence of this bpbuffer.
	:param offset
	:param size
	:return
	"""
	def partAsLongArray(self, offset: int, size: int) -> np.array([], dtype=np.int64):
		buf = self.longBuffer(size)
		self.copyPartAsLongArray(buf, offset, size)
		return buf

	def copyPartAsLongArray(self, writeTo: np.array([], dtype=np.int64), offset: int, size: int):
		shiftAmt = (offset % 32) * 2

		finalKeepBits = 64 if (size % 32 == 0) else (size % 32) * 2
		finalLongMask = np.int64(-1) << (64 - finalKeepBits)

		numLongs = (size >> 5) if (size % 32 == 0) else (size >> 5) + 1
		sourceLongs = len(self.data)
		i = 0
		read = offset // 32
		while (i < numLongs):
			x = self.data[read] << shiftAmt
			if (read < sourceLongs - 1 and shiftAmt > 0):
				x = x | (self.data[read + 1] >> (64 - shiftAmt))
		
			if (i == numLongs - 1):
				x = x & finalLongMask
		
			writeTo[i] = x
			read += 1
			i += 1


class OffsetNTBitArray(NTBitArray):
	def __init__(self, data: np.array([], dtype=np.int64), offset: int, size: int):
		self.data = data
		self.offset = offset
		self.size = size
		
class ZeroNTBitArray(NTBitArray):
	def __init__(self, data: np.array([], dtype=np.int64), size: int):
		super().__init__(data, 0, size)

if __name__ == '__main__':
	arr = _NTBitArray()
	print(arr.encode('AATC').toString)