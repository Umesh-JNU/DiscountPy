from discountpy.motif_space import MotifSpace
from discountpy.motif_counter import MotifCounter


class MotifCountingScanner:
    """ Looks for the motifs and find the it's occurences
        in the whole dataset
    """
    def __init__(self, space: MotifSpace):
        self.scanner = space.scanner
        
    def scanRead(self, counter: MotifCounter, read):
        for m in self.scanner.allMatches(read):
            if m.feature.valid:
                counter.increment(m)

    def scanGroup(self, counter: MotifCounter, rs):
        for r in rs:
            self.scanRead(counter, r)
