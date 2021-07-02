from typing import Any
from discountpy.motif import *


class PositionNode:
    """ PosiitonNode: to track and find the best Motifs
        lesser the rank higher is the priority
    """
    __slots__ = ['prevPos', 'nextPos']
    prevPos: Any
    nextPos: Any
    
    def __init__(self, p = '_', n = '_'):
        self.prevPos = p
        self.nextPos = n
        
    def removeNode(self):
        temp = self.nextPos
        self.prevPos.nextPos = self.nextPos
        self.nextPos.prevPos = self.prevPos
        
        del self
        return temp
        
    def linkPos(self, before, after):
        before.nextPos = self
        self.prevPos = before
        self.nextPos = after
        after.prevPos = self


class MotifContainer(PositionNode):
    """ MotifContainer: Store the Motif and is the Node in PosRankWindow (doubly linked-list)
        pos - position of the Motif in the read
        motif - Motif 
        rank - rank of the Motif
    """
    __slots__ = ['pos', 'motif', 'rank']
    pos: int
    motif: Motif
    rank: int
    
    def __init__(self, motif: Motif):
        self.pos = motif.position
        self.rank = motif.feature.rank
        self.motif = motif
    
    def dropUntilPosition(self, pos: int):
        if self.pos < pos:
            self = self.removeNode()
            self.dropUntilPosition(pos)
            
    def __repr__(self):
        return '[%s, %s]' % (self.pos, self.motif)


class PosRankWindow:
    """ PosRankWindow: A doubly linked-list that makes easier to find the best Motif within a
                         window of k-length
    """
    start: PositionNode = PositionNode()
    end: PositionNode = PositionNode()
    
    def __init__(self):
        # None <= start <=> end => None
        self.start.nextPos = self.end
        self.start.prevPos = None
        self.end.prevPos = self.start
        self.end.nextPos = None
    
    """ Moves the window and insert the new Node to the right and removes from the left 
    """
    def moveWindowAndInsert(self, pos: int, insertRight):
        new_node = MotifContainer(insertRight)
        if new_node.motif.feature.valid:
            self.appendMonotonic(new_node, self.end)
        
        if self.start.nextPos != self.end and self.end.prevPos != self.start:
            self.start.nextPos.dropUntilPosition(pos)
    
    """ Potentially insert the Motifs to the correct location
    """
    def appendMonotonic(self, insertNode, search):
        # if this(start <=> end) is not the case
        if search.prevPos != self.start:
            if insertNode.rank < search.prevPos.rank:
                self.appendMonotonic(insertNode,search.prevPos)
            else:
                insertNode.linkPos(search.prevPos, self.end)
        else:
            insertNode.linkPos(self.start, self.end)
    
    """ Return the best motif in each k-length window
    """
    def top(self):
        return __Empty__ if self.start.nextPos==self.end else self.start.nextPos.motif 
    

    """ For the testing purpose to check what is happening in the window
    """
    def showWindow(self):
        temp = self.start.nextPos
        while temp != self.end:
            print('window-pos=',temp.pos, temp.motif)
            temp = temp.nextPos