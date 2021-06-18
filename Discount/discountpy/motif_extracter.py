from discountpy.motif_space import MotifSpace
from discountpy.shift_scanner import ShiftScanner
from discountpy.pos_rank_window import PosRankWindow

class MotifExtractor:
    __slots__ = ('scanner', 'K', 'width')
    scanner: ShiftScanner
    K: int
    width: int

    """ Extract all the best motifs from the reads
    """
    def __init__(self, space: MotifSpace, k: int):
        self.scanner = space.scanner
        self.K = k
        self.width = space.width

    """ Find all the top (best Motifs within K-length window)
    """
    def slidingTopMotifs(self, read):
        matches = self.scanner.allMatches(read)
        windowMotifs = PosRankWindow()
        
        if (len(read) < self.K):
            return iter()
        else:
            pos = self.width - self.K
            for m in matches:
                windowMotifs.moveWindowAndInsert(pos, m)
                pos += 1
                yield windowMotifs.top()
                
    """ find the regions of the top motifs in reads
    """
    def regionsInRead(self, read):
        topMotifs = self.slidingTopMotifs(read)
        self.drop(topMotifs, self.K - self.width)
        
        lastMotif = next(topMotifs)

        consumed = 1
        startReg = 1
        for motif in topMotifs:
            if lastMotif == motif:
                consumed += 1
            else:
                yield lastMotif, startReg-consumed
                lastMotif = motif
                consumed = 1

            startReg += 1

        # for the last motif
        yield lastMotif, startReg - consumed

    """ Return all the Super-mers
    """
    def splitRead(self, read):
        readByReg = self.regionsInRead(read)

        prev = next(readByReg)
        while readByReg:
            b1 = prev
            b2 = next(readByReg, None)
            
            if b2:
                yield b1[0], read[b1[1]: b2[1] + (self.K - 1)]
                prev = b2
            else:
                yield b1[0], read[b1[1]:]
                break

    @staticmethod
    def drop(itr, n):
        j = 0
        try:
            while (j < n):
                next(itr)
                j += 1
        except StopIteration:
            return
