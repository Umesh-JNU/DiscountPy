__all__ = [
    'Features',
    'Motif',
    '__Empty__'
]


class Features:
    """ Features: features of the motif -
        pattern - sequence
        rank - rank/priority/id (must be unique)
        valid - valid motif or not (only for universal frequency)
    """

    __slots__ = ('pattern', 'rank', 'valid')
    pattern: str
    rank: int
    valid: bool

    def __init__(self, pat: str, rank: int, valid: bool):
        self.pattern = pat
        self.rank = rank
        self.valid = valid

    def __repr__(self):
        return 'Features(%s,%d,%s)' % (self.pattern, self.rank, self.valid)


class Motif:
    """ Motif: m-length sequences in the reads.
        position - position in read
        feature - feature with (pattern, rank, valid)
    """

    __slots__ = ('position', 'feature')
    position: int
    feature: Features

    def __init__(self, pos: int, feature: Features):
        self.position = pos
        self.feature = feature

    def __repr__(self):
        return 'Position=%s, Feature=(%s)' % (self.position, self.feature)

__Empty__ = Motif(-1, Features('', -1, False))
