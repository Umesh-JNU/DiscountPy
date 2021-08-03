def encode(self, data: str) -> list:
		buf = self.longBuffer(len(data))
		longIdx = 0
		qs = 0
		while longIdx < len(data):
			quadIdx = 0
			qshift = 56
			x = 0
			while quadIdx < 8 and qs < len(data):
				q = _quadToByte(data, qs)
				x = x | ((q & 255) << qshift)
				qs += 4
				qshift -= 8
				quadIdx += 1
			
			buf[longIdx] = x
			longIdx += 1
		
		return buf

	def longBuffer(self, size: int) -> list:
		numLongs = size >> 5 if (size % 32 == 0) else (size >> 5) + 1
		return [0]*numLongs

	""" Shift an array of two-bits one step to the left, dropping one bp, and inserting another on the right. """
	def shiftLongArrayKmerLeft(self, data: list, newBP: bytes, k: int) -> list:
		n = len(data)

		def r(i):
			if(i < n-1):
				return (data[i] << 2) | (data[i+1] >> 62)
			return (data[i] << 2) | (newBP << ((32 - (k%32)) * 2))
		
		return [r(i) for i in range(n)]

	def longsToString(self, data: list, offset: int, size: int) -> str:
		sb = ''
		byte = size//4 if(size % 32 == 0) else size//4 + 8

	def _longsToString(self, buffer, builder, data, offset, size):