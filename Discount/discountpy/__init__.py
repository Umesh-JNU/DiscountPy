__version__ = '0.1.0'

__all__ = [
    'encode',
    'decode',
    'charToTwobit',
    'twobitToChar',
    'motif',
    'motif_counter',
    'motif_count_scanner',
    'motif_space',
    'pos_rank_window',
    'shift_scanner',
    '__version__',
]

import re

def charToTwobit(char: str):
    switcher = {
        'A': 0x0,
        'C': 0x1,
        'G': 0x2,
        'T': 0x3,
        'U': 0x3
    }
    return switcher.get(char, "Invalid Nucleotide")


def twobitToChar(byte: bytes):
    switcher = {
        '00': 'A',
        '01': 'C',
        '10': 'G',
        '11': 'T'
    }
    return switcher.get(byte, "Invalid Value")

# convert into bits and gives direct priority
def encode(motif):
    code = {'A': '00', 'C': '01', 'G': '10', 'T': '11'}
    byteCode = ''.join(map(lambda x: code[x], motif))
    return int(byteCode, 2)


def decode(rank):
    # print("rank = ", rank)
    s = bin(rank)[2:].zfill(20)
    # print('s=',s)
    x=re.findall('..',s)
    # print('re.findall = ', x)
    # print('decode = ', ''.join(map(twobitToChar, x)))
    return ''.join(map(twobitToChar, x))