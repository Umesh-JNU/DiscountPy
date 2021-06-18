from discountpy.motif_space import MotifSpace
from discountpy.motif import Motif


class MotifCounter:
    """ Main frequency counter
    """
    def __init__(self, space: MotifSpace):
        sizeOfCounter = len(space.byPriority)
        self.countArr = [0]*sizeOfCounter

    """ Increment the count of the corresponding Motif
    """
    def increment(self, m: Motif):
        rank = m.feature.rank
        self.countArr[rank] += 1

    def motifsWithCounts(self, space: MotifSpace):
        return zip(space.byPriority, self.countArr)

    def _toSpaceByFrequency(self, counts: list((str, int))):
        # sorting first by frequency and then sorting by lexicographically
        c = map(lambda _: _[0], sorted(counts, key=lambda _: (_[1], _[0])))
        return MotifSpace(c)

    """ Make a new space to with priority based on frequency and lexicographically ordering
    """
    def toSpaceByFrequency(self, oldSpace: MotifSpace):
        pairs = self.motifsWithCounts(oldSpace)
        return self._toSpaceByFrequency(pairs)
        
