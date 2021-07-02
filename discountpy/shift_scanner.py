from discountpy.motif import *

class ShiftScanner:
    def __init__(self, space):
        assert(space.width <= 15)
        self.space = space

        global width
        width = space.width
        # mask = int('11'*width, 2)

        # self.featuresByPriority = (Features(p, i, True) for p, i in enumerate(space.motifsOfLength()))

    """ Find all matches in the string.
        Returns an array with the matches in order, or Motif.Empty for positions
        where no valid matches were found.
    """

    def allMatches(self, read: str, tolist: bool = False):
        def getMatches(pos, motif: str):
            priority = self.space.priorityOf(motif)
            if(priority != -1):
                return Motif(pos, Features(motif, priority, True))
            return __Empty__

        if tolist:
            return [(read[pos:pos+width], pos) for pos in range(len(read) - (width-1))]

        return (getMatches(pos, read[pos:pos+width]) for pos in range(len(read) - (width-1)))
