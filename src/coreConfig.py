import os
from .color import Col
from src.counting import countKmers
from discountpy.motif_space import MotifSpace, _MotifSpace

class DiscountCustomError(Exception):
    def __init__(self, msg, arg, req):
        super().__init__(msg, arg, req)
        self.msg = msg
        self.req = req
        self.has = arg
        
    def __str__(self):
        return Col.B + Col.R + self.msg + Col.G + " | " + Col.C\
                             + self.has + Col.V + u" \u2550"u"\u2550> " + Col.C\
                             + self.req + Col.W

def verify(args):
    print(Col.G, 'Verifying the input...', Col.W)
    """ Check whether file exist and whether format is txt/fasta file format """
    
    if not os.path.isfile(args.f):
        raise DiscountCustomError('File or directory not found', '', args.f)

    if args.count:
        if not args.f.endswith('.txt'):
            raise DiscountCustomError("FileFormatError : required .txt file", args.f.rsplit('/', 1)[1], "XXX.txt")
        else:
            try:
                p = args.count.rsplit('/', 1)[0]
                os.mkdir(p)
            except OSError:
                pass
    else:
        if not args.f.endswith('.fasta'):
            raise DiscountCustomError("FileFormatError : required .fasta file", args.f, "XXX.fasta")

    """ Check for ordering : if universal frequency minimizer must be entered """
    if args.o == 'ufreq' and not args.minimizers:
        raise DiscountCustomError("UniversalFrequencyOrdering : required -minimizers", args.o, "-minimizers")

    """ Check if the given output dir exist or not """
    if args.output:
        try:
            p = args.output.rsplit('/', 1)[0]
            os.mkdir(p)
        except OSError:
            pass

class CoreConf:
    __slots__ = ['K','WIDTH','MINIMIZERS','DATASET','ORDER','TEMPLATESPACE', 'OUTPUT','COUNT']
    K: int
    WIDTH: int
    MINIMIZERS: str
    DATASET: str
    ORDER: str
    TEMPLATESPACE: MotifSpace
    OUTPUT: str
    COUNT: str
    
    def __init__(self, args):
        verify(args)
        print(Col.Y, 'Verification done successfully')
        
        self.K = args.k
        self.DATASET = args.f
        self.COUNT = args.count

        if self.COUNT:
            print(Col.V, 'Counting...', Col.W)
            countKmers(self.K, self.DATASET, self.COUNT)
            print(Col.V, 'Counting finished.', Col.W)
            exit()
        
        self.WIDTH = args.m if args.m else 10
        self.MINIMIZERS = args.minimizers
        self.ORDER = args.o
        self.OUTPUT = args.output  
        print(Col.V, 'Executing...', Col.W)      
        self.TEMPLATESPACE = MotifSpace(_MotifSpace().motifsOfLength(width=self.WIDTH))
        
        # print(self.K, self.WIDTH, self.DATASET, self.MINIMIZERS, self.ORDER)
