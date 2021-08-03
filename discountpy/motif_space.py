import numpy as np
import discountpy.shift_scanner as s
from itertools import product
from discountpy.motif import *
from discountpy.utils import NTBitArray as NT
import time

print('start =',time.time())
class MotifSpace:
    """ MotifSpace: create the priority lookup table from which
        priority/rank of each Motif can be accessed easily
    """
    __slots__ = ('width', '_maxMotifs', '_shift', 'scanner', 'byPriority', 'priorityLookUp')
    width: int
    byPriority: np.ndarray
    scanner: s.ShiftScanner
    _maxMotifs: int
    _shift: int
    priorityLookUp: np.ndarray

    def __init__(self, byPriority: np.ndarray):
        self.byPriority = list(byPriority)
        self.width = len(self.byPriority[0]) 
        self.scanner = s.ShiftScanner(self)
        self._maxMotifs = 4 << (self.width * 2 - 2)
        self._shift = 64 - (self.width * 2)
        self.priorityLookUp = np.ndarray(self._maxMotifs, dtype=np.int64)
        
        self.priorityLookUp.fill(-1)
        print('inti',time.time())
        for pri, motif in enumerate(self.byPriority):
            self.priorityLookUp[self.motifToInt(motif)] = pri
        print('end',time.time())
    def motifToInt(self, m: str) -> int:
        # print(m)
        wrapped = NT._NTBitArray().encode(m)
        # print(wrapped.data)
        x = wrapped.partAsLongArray(0, self.width)
        # print(x[0] , np.uint64(x[0]) >> np.uint64(self._shift), int.from_bytes(x[0] >> self._shift, 'little'))
        return np.uint64(x[0]) >> np.uint64(self._shift) 

    def priorityOf(self, mk):
        return self.priorityLookUp[self.motifToInt(mk)]

    def create(self, pattern: str, pos: int) -> Motif:
        return Motif(pos, Features(pattern, self.priorityOf(pattern), True))


class _MotifSpace:
    all1mersDNA = ("A", "C", "G", "T")
    all1mersRNA = ("A", "C", "G", "U")
    
    def motifsOfLength(self, width: int, rna: bool = False) -> iter:
        bases = self.all1mersRNA if rna else self.all1mersDNA

        # def generate(prefix, length):
        #     if (length == 0):
        #         yield prefix
        #         return

        #     for base in bases:
        #         yield from generate(prefix + base, length-1)

        return (''.join(p) for p in product(bases, repeat=width))

    def ofLength(self, w: int, rna: bool = False) -> MotifSpace:
        return self.using(self.motifsOfLength(w, rna))
    
    def using(self, mers: list) -> MotifSpace:
        return MotifSpace(list(mers))

    def fromTemplateWithValidSet(self, template: MotifSpace, validMers: iter) -> MotifSpace:
        validSet = set(validMers)
        return MotifSpace(filter(lambda _: _ in validSet, template.byPriority))


print('finish =', time.time())
def main():
    m = _MotifSpace().ofLength(4, False)
    # print(type(m), m.byPriority, m.priorityLookUp)
    # for _ in m.priorityLookUp:
    #     print(_)

if __name__ == '__main__':
    main()
    # import cProfile
    # cProfile.run("main()", "profile.dat")

    # import pstats
    # from pstats import SortKey

    # with open("profile.txt", "w") as f:
    #     p = pstats.Stats("profile.dat", stream=f)
    #     p.sort_stats("time").print_stats()

    # with open("profile.txt", "w") as f:
    #     p = pstats.Stats("profile.dat", stream=f)
    #     p.sort_stats("calls").print_stats()