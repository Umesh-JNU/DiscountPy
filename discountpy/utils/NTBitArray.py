import numpy as np
from discountpy.utils.BitRepresentation import _quadToByte

def longBuffer(size: int) -> np.array([], dtype=np.int64):
	numLongs = (size >> 5) if(size % 32 == 0) else (size >> 5) + 1
	return np.zeros(numLongs, dtype=np.int64)

def encode(data: str) -> np.array([], dtype=np.int64):
	buf = longBuffer(len(data))
	longIdx = 0
	quadOffset = 0
	while longIdx < len(buf):
		quadIdx = 0
		qshift = 56
		x = 0
		while quadIdx < 8 and quadOffset < len(data):
			quad = _quadToByte(data, quadOffset)
			x |= (quad & 255) << qshift

			quadIdx += 1
			qshift -= 8
			quadOffset += 4

		buf[longIdx] = x
		longIdx += 1
	
	return buf

if __name__ == '__main__':
	print(encode('AACacdfdfdf'))