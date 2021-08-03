from discountpy.motif import *
from discountpy.utils.BitRepresentation import charToTwobit

class ShiftScanner:
    def __init__(self, space):
        assert(space.width <= 15)
        self.space = space

        global width, mask
        width = space.width
        mask = (1 << (width*2)) - 1

        self.featuresByPriority = [Features(m, p, True) for p, m in enumerate(space.byPriority)]

    """ Find all matches in the string.
        Returns an array with the matches in order, or Motif.Empty for positions
        where no valid matches were found.
    """

    def allMatches(self, read: str, tolist: bool = False):
        pos = 0
        window = 0
        while ((pos < width - 1) and pos < len(read)):
            window = ((window << 2) | charToTwobit(read[pos]))
            pos += 1

        def getMatches() -> iter:
            nonlocal pos, window
            while pos < len(read):
                window = ((window << 2) | charToTwobit(read[pos])) & mask 
                pos += 1

                priority = self.space.priorityLookUp[window]
                if(priority != -1):
                    motifPos = pos - width
                    features = self.featuresByPriority[priority]
                    yield Motif(motifPos, features)
                else:
                    yield __Empty__
    
        
        def _getMatches(pos, motif: str) -> iter:
            priority = self.space.priorityOf(motif)
            if(priority != -1):
                return Motif(pos, Features(motif, priority, True))
            return __Empty__

        if tolist:
            return [_getMatches()(read[pos:pos+width], pos) for pos in range(len(read) - (width-1))]

        # return (getMatches(pos, read[pos:pos+width]) for pos in range(len(read) - (width-1)))
        return getMatches()

if __name__ == '__main__':
    from discountpy.motif_space import MotifSpace, _MotifSpace
    space = _MotifSpace().ofLength(4, False)
    
    scanner = ShiftScanner(space)
    matches = scanner.allMatches('AAACCCGGGTTT')
    print(scanner.allMatches('AAACCCGGGTTT'), list(matches))