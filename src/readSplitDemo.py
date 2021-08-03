import re
from .color import Col
from src.coreConfig import CoreConf
from discountpy import (motif_space as ms,
                        motif_counter as mc,
                        motif_extracter as me,
                        motif_count_scanner as mcs)


class ReadSplitConf(CoreConf):
    def __init__(self, args):
        super().__init__(args)

    def getInputSequences(self) -> iter:
        with open(self.DATASET) as f:
            return map(lambda _: re.split(r"[^ACGTU]+", _.rstrip()), 
                filter(lambda _: not _.startswith('>'), f.readlines()))
        
    def getFrequencySpace(self, validMotifs) -> ms.MotifSpace:
        inputdata = self.getInputSequences()
        template = ms._MotifSpace().fromTemplateWithValidSet(self.TEMPLATESPACE, validMotifs)
        counter = mc.MotifCounter(template)
        scanner = mcs.MotifCountingScanner(template)
        scanner.scanGroup(counter, inputdata)
        return counter.toSpaceByFrequency(template)
  
    def getSplitter(self) -> me.MotifExtractor:
        def use():
            with open(self.MINIMIZERS) as f:
                return (_.rstrip() for _ in f.readlines())

        template = self.TEMPLATESPACE
        validMotifs = use() if self.MINIMIZERS else template.byPriority
        
        useSpace = template if (self.ORDER == 'lex') else self.getFrequencySpace(validMotifs)
        
        return me.MotifExtractor(useSpace, self.K)

def printSup(s, k):
    print(f'{s[0].feature.pattern} (pos {s[0].position}, rank {s[0].feature.rank}, len {len(s[1])-k+1} k-mers)', end=' ')
    before, after = s[1].split(s[0].feature.pattern, 1)
    print(f'{before}{Col.C}{s[0].feature.pattern}{Col.W}{after}')


def readSplitDemo(args):
    print(Col.C, 'Running Discount...')
    
    conf = ReadSplitConf(args)
    
    spl = conf.getSplitter()
    if conf.OUTPUT:
        with open(conf.OUTPUT, 'w+') as f:
            for r in conf.getInputSequences():
                # print('Read:', r)
                for s in spl.splitRead(r):
                    f.write('{0}\t{1}\n'.format(s[0].feature.pattern, s[1]))
                    # printSup(s, spl.K)
    else:
        for r in conf.getInputSequences():
            print('Read :', r)
            for s in spl.splitRead(r):
                printSup(s, spl.K)

    