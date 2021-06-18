import os
from .color import Col
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
    """ Check for the fasta file format """
    
    if not args.f.endswith('.fasta'):
        raise DiscountCustomError("FileFormatError : required .fasta file", args.f, "XXX.fasta")
    
    """ Check for ordering : if universal frequency minimizer must be entered """
    if args.o == 'ufreq' and not args.minimizers:
        raise DiscountCustomError("UniversalFrequencyOrdering : required -minimizers", args.o, "-minimizers")

    """ Check if the given output dir exist or not """
    if args.output and not os.path.isdir(args.output.split('/')[0]):
        raise DiscountCustomError("No such file or directory:", '', args.output)

class CoreConf:
    __slots__ = ['K','WIDTH','MINIMIZERS','DATASET','ORDER','TEMPLATESPACE', 'OUTPUT']
    K: int
    WIDTH: int
    MINIMIZERS: str
    DATASET: str
    ORDER: str
    TEMPLATESPACE: MotifSpace
    OUTPUT: str
    
    def __init__(self, args):
        verify(args)
        print(Col.Y, 'Verification done successfully')
        print(Col.V, 'Executing...', Col.W)
        
        self.K = args.k
        self.WIDTH = args.m if args.m else 10
        self.DATASET = args.f
        self.MINIMIZERS = args.minimizers
        self.ORDER = args.o
        self.OUTPUT = args.output
        self.TEMPLATESPACE = MotifSpace(_MotifSpace().motifsOfLength(width=self.WIDTH))
        
        # print(self.K, self.WIDTH, self.DATASET, self.MINIMIZERS, self.ORDER)
