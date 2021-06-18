import discountpy.shift_scanner as s
from discountpy.motif import *
from discountpy import encode

class MotifSpace:
    """ MotifSpace: create the priority lookup table from which
        priority/rank of each Motif can be accessed easily
    """
    __slots__ = ('width', '_maxMotifs', 'scanner', 'byPriority', 'priorityLookUp')
    width: int
    byPriority: list
    scanner: s.ShiftScanner
    _maxMotifs: int
    priorityLookUp: list

    def __init__(self, byPriority: list):
        self.byPriority = list(byPriority)
        self.width = len(self.byPriority[0]) 
        self.scanner = s.ShiftScanner(self)
        self._maxMotifs = 4 << (self.width * 2 - 2)
        self.priorityLookUp = [-1]*self._maxMotifs
        
        for pri, motif in enumerate(self.byPriority):
            self.priorityLookUp[self.motifToInt(motif)] = pri

    def motifToInt(self, m: str) -> int:
        return encode(m)
   
    def priorityOf(self, mk):
        return self.priorityLookUp[self.motifToInt(mk)]

    def create(self, pattern, pos):
        return Motif(pos, Features(pattern, self.priorityOf(pattern), True))


class _MotifSpace:
    all1mersDNA = ("A", "C", "G", "T")
    all1mersRNA = ("A", "C", "G", "U")
    
    def motifsOfLength(self, width: int, rna: bool = False) -> iter:
        bases = self.all1mersRNA if rna else self.all1mersDNA

        def generate(prefix, length):
            if (length == 0):
                yield prefix
                return

            for base in bases:
                yield from generate(prefix + base, length-1)

        return generate("", width)

    def fromTemplateWithValidSet(self, template: MotifSpace, validMers: iter) -> MotifSpace:
        validSet = set(validMers)
        return MotifSpace(filter(lambda _: _ in validSet, template.byPriority))

