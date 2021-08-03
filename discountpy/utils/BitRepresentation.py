import numpy as np

A: bytes = 0x0
C: bytes = 0x1
G: bytes = 0x2
T: bytes = 0x3
U: bytes = 0x3 # In RNA
    
""" Convert a single BP from twobit representation to string representation. """
def twobitToChar(byte: bytes):
    switcher = {
        0 : 'A',
        1 : 'C',
        2 : 'G',
        3 : 'T'
    }

    return switcher.get(byte, "Invalid Value")

""" Convert a single nucleotide from string (char) representation to "twobit" representation. """
def charToTwobit(char: str) -> bytes:
    switcher = {
        'A' : A,
        'C' : C,
        'G' : G,
        'T' : T,
        'U' : U
    }

    return switcher.get(char, "Invalid Nucleotide")

twobits = (A, C, T, G)

""" Convert a single byte to the "ACTG" format (a 4 letter string) """
def byteToQuadCompute(byte: bytes):
    res = ""
    for i in range(4):
        ptn = (byte >> ((3 - i) * 2)) & 0x3
        char = twobitToChar(ptn)
        res += char

    return res

""" Map a single byte to a quad-string for unpacking.
    Precomputed lookup array."""
byteToQuadLookup = [byteToQuadCompute(i) for i in range(256)]

""" Complement of a single BP. """
def complementOne(byte: bytes) -> int:
    return complement(byte) & 0x3

""" Complement of a number of BPs packed in a byte. """
def complement(byte: bytes) -> bytes:
    return (byte ^ 0xff)

""" Map a quad-string (four letters) to an encoded byte """
def quadToByte(quad: str) -> bytes:
    return _quadToByte(quad, 0)


""" Unpack a byte to a 4-character string (quad). """
def byteToQuad(byte: bytes):
    return byteToQuadLookup[byte]

""" Convert an NT quad (string of length 4) to encoded byte form. 
    The string will be padded on the right with 'A' if it's too short. """
def _quadToByte(quad: str, offset: int) -> np.int64:
    res = 0
    i = offset
    end = offset + 4
    while (i < end):
        c = 'A' if(i >= len(quad)) else quad[i]
        twobits = charToTwobit(c)
        res = twobits if i==0 else (res << 2) | twobits
        # print(res, format(res, '064b'))
        i += 1
    
    return np.int64(res)
    
""" Convert a string to an array of quads. """
def stringToBytes(bps: str) -> list:
    rsize = (len(bps) - 1) // 4
    r = [_quadToByte(bps, i*4) for i in range(rsize+1)]
    
    return r

""" Convert a byte array of quads to a string. The length of the resulting string must be supplied. """
def bytesToString(byteArr: bytearray, builder: str, offset: int, size: int) -> str:
    # print(byteArr)
    startByte = offset // 4

    i = startByte
    while (i < len(byteArr)):
        if (len(builder) < size):
            if (i == startByte):
                of = offset % 4
                builder += byteToQuad(byteArr[i])[of : of + 4]
            else:
                builder += byteToQuad(byteArr[i])
        i += 1

    return builder[:size]