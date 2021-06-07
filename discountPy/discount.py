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

class Features:
    def __init__(self, pat: int, rank: int, valid: bool):
        self.pattern = pat
        self.rank = rank
        self.valid = valid

    def __repr__(self):
        return '[%s, %s, %s]' % (self.pattern, self.rank, self.valid)


class Motif:
    def __init__(self, pos, feature):
        self.position = pos
        self.feature = feature

    def __repr__(self):
        return '[%s, (%s, %s)]' % (self.position, self.feature.pattern, self.feature.rank)


class MotifSpace:
    all1mersDNA = ("A", "C", "G", "T")
    all1mersRNA = ("A", "C", "G", "U")

    def __init__(self, length, rna=False):
        self.width = length
        self.rna = rna

        maxMotifs = 4 << (length * 2 - 2)
        self.priorityLookUp = [-1 for i in range(maxMotifs)]
        self.byPriority(self.motifsOfLength())

    def byPriority(self, priorityArray):
        for i, m in enumerate(priorityArray):
            self.priorityLookUp[encode(m)] = i

    def byPriorityValidSet(self, validSet):
        for i, m in enumerate(self.motifsOfLength()):
            if m not in validSet:
                self.priorityLookUp[i] = -1
        
    def motifsOfLength(self):
        bases = self.all1mersRNA if self.rna else self.all1mersDNA

        def generate(prefix, length):
            if (length == 0):
                yield prefix
                return

            for base in bases:
                yield from generate(prefix + base, length-1)

        return generate("", self.width)

    def scanner(self):
        return ShiftScanner(self)

    def priorityOf(self, mk):
        return self.priorityLookUp[encode(mk)]

    def create(self, pattern, pos):
        return Motif(pos, Features(pattern, self.priorityOf(pattern), True))


class ShiftScanner:
    def __init__(self, space: MotifSpace):
        assert(space.width <= 15)
        self.space = space

        global width
        width = space.width
        mask = int('11'*width, 2)

        self.featuresByPriority = (Features(p, i, True)
                                   for p, i in enumerate(space.motifsOfLength()))

    """ Find all matches in the string.
        Returns an array with the matches in order, or Motif.Empty for positions
        where no valid matches were found.
    """

    def allMatches(self, read, tolist=False):
        def getMatches(pos, motif):
            priority = self.space.priorityOf(motif)
            if(priority != -1):
                return Motif(pos, Features(motif, priority, True))
            return Motif(0, Features("", 0, False))

        if tolist:
            return [(read[pos:pos+width], pos) for pos in range(len(read) - (width-1))]

        return (getMatches(pos, read[pos:pos+width]) for pos in range(len(read) - (width-1)))


class Node:
    def __init__(self, pos, motif: Motif):
        self.pos = pos
        self.rank = motif.feature.rank
        self.motif = motif
        self.next = None
        self.prev = None

    def __repr__(self):
        return '[%s, %s]' % (self.pos, self.motif)


class PosRankWindow:
    def __init__(self, size):
        self.head = None
        self.tail = None
        self.size = size

    def moveWindowAndInsert(self, pos: int, insertRight: Motif):
        new_node = Node(pos, insertRight)
        self.appendMonotonic(new_node, self.tail)
        self.dropUntilPosition(new_node)

        if pos - self.head.pos >= self.size:
            self.remove_head()

    def appendMonotonic(self, new_node, end):
        if end == None:
            self.insert_head(new_node)
        else:
            if new_node.rank < self.head.rank:
                self.insert_front(new_node)
            elif new_node.rank > end.rank:
                self.insert_after(new_node, end)
            else:
                self.appendMonotonic(new_node, end.prev)

    def insert_head(self, new_node):
        self.head = new_node
        self.head.next = None
        self.tail = new_node
        self.tail.prev = None

    def insert_front(self, new_node):
        new_node.prev = None
        new_node.next = self.head
        self.head.prev = new_node
        self.head = new_node

    def insert_after(self, new_node, end):
        if end.next == None:
            end.next = new_node
            new_node.next = None
            new_node.prev = end
            self.tail = new_node
        else:
            new_node.next = end.next
            new_node.next.prev = new_node
            new_node.prev = end
            end.next = new_node

    def dropUntilPosition(self, insertedNode):
        if insertedNode.next != None:
            self.removeNext(insertedNode)
            self.dropUntilPosition(insertedNode)

    def removeNext(self, insertedNode):
        temp = insertedNode.next
        if temp.next != None:
            insertedNode.next = temp.next
            temp.next.prev = insertedNode
        else:
            insertedNode.next = None
            self.tail = insertedNode
            temp.prev = None

        del temp

    def remove_head(self):
        if self.head == None:
            print("List is empty")
        else:
            temp = self.head
            temp.next.prev = None
            self.head = temp.next
            temp.next = None
            del temp

    def top(self):
        if self.head == None:
            print("Window is empty")
        else:
            return self.head

    def show_window(self):
        temp = self.head
        print(temp.pos, temp.motif)
        while temp != None:
            print([temp.pos, temp.motif])
            temp = temp.next

class MotifExtractor:
    def __init__(self, space: MotifSpace, k: int):
        self.scanner = space.scanner()
        self.K = k
        
        global width
        width = space.width

    def slidingTopMotifs(self, read):
        matches = self.scanner.allMatches(read)
        windowMotifs = PosRankWindow(self.K - (width - 1))

        if (len(read) < self.K):
            return iter()
        else:
            pos = width - self.K
            for m in matches:
                if m.feature.valid:
                    windowMotifs.moveWindowAndInsert(pos, m)
                    
                    if pos > 0: yield windowMotifs.top()
    
    def regionsInRead(self, read):
        topMotifs = self.slidingTopMotifs(read)
        print(list(self.slidingTopMotifs(read)))
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

    def splitRead(self, read):
        readByReg = self.regionsInRead(read)
        prev = next(readByReg)
        while readByReg:
            b1 = prev
            b2 = next(readByReg, None)
            # print(b1, b2)
            if b2:
                yield b1[0], read[ b1[1] : b2[1] + (self.K - 1) ]
                prev = b2
            else:
                yield b1[0], read[b1[1] : ]
                break;
            

class MotifCounter:
    def __init__(self, space: MotifSpace):
        sizeOfCounter = 4 << (space.width*2 - 2)
        self.countArr = [0 for i in range(sizeOfCounter)]
        self.space = space

    def increment(self, m: Motif):
        print("motif = ", m)
        rank = m.feature.rank
        self.countArr[rank] += 1

    def toSpaceByFrequency(self):
        # zipping with index
        self.motifsWithCount = list(
            zip(self.space.motifsOfLength(), self.countArr))

        # sorting first by frequency and then sorting by lexicographically
        self.motifsWithCount.sort(key=lambda m: (m[1], m[0]))
        self.motifsWithCount = (m[0] for m in self.motifsWithCount)

        # making new motif with different priority
        self.space.byPriority(self.motifsWithCount)


class MotifCountingScanner:
    def __init__(self, space: MotifSpace):
        self.scanner = space.scanner()
        self.motifCount = MotifCounter(space)

    def scanRead(self, read):
        print("read=", read)
        for m in self.scanner.allMatches(read):
            print("m=", m)
            self.motifCount.increment(m)

    def scanGroup(self, rs):
        print("rs =", rs)
        for r in rs:
            print(r)
            self.scanRead(r.strip('\n'))

    def makeNewSpace(self):
        self.motifCount.toSpaceByFrequency()


def main(f: str, k: int, m: int):
    validSet = open('miniPASHA.txt')
    valid = list(_.strip('\n') for _ in validSet.readlines())
    validSet.close()

    space = MotifSpace(m, False)

    def freq(f: str):
        file = open(f)
        rs = filter(lambda _: _[0] != '>', file.readlines())
        file.close()

        countScanner = MotifCountingScanner(space)
        countScanner.scanGroup(rs)
        countScanner.makeNewSpace()
        print(countScanner.motifCount.countArr)
        print(space.priorityLookUp)

    freq(f)
    space.byPriorityValidSet(valid)
    ex = MotifExtractor(space, k)
    file = open(f)
    for data in file.readlines():
        read = data.strip('\n')
        if read[0] != '>':
            print('Read :', read)
            for x in ex.splitRead(read):
                print(x)
            print('\n')
    file.close()

if __name__ == "__main__":
    # k, m = map(int, input('Enter k and m : ').split())
    # file = input('Enter file name : ')
    # main(file, k, m)
    main('data/small.fasta', 28, 10)