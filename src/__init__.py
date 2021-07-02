import argparse
from src.color import Col
from src.readSplitDemo import readSplitDemo
from discountpy import __version__


class CustomArgparser(argparse.ArgumentParser):
    def error(self, message):
        print(Col.R + Col.B + 'ERROR : %s\n' % message)
        print(Col.W + 'For more details run :' + Col.Y + ' discount ' + Col.GR + '-h' + Col.W)
        exit()


def main():
    # print(sys.argv)    
    parser = CustomArgparser(prog="discount", description="\n\tDiscountPy : A k-mer counting tool")
    count = parser.add_argument_group('Count k-mers')
    count.add_argument('--count', metavar='', type=str, help='Generate k-mers counted file. (Input file(.txt) shoud be sorted by minimizers with corresponding super-mers)')
    req = parser.add_argument_group('Required Arguments')
    parser.version = Col.G + 'DiscountPy version ' + Col.C + __version__ + Col.W
    
    req.add_argument("-k", metavar='', type=int, help="Length of the k-mers", required=True)
    parser.add_argument("-m", metavar='', type=int, help="Width of the minimizers (default 10)", default=10)
    req.add_argument("-f", metavar='', type=str, help="Dataset (.fasta)", required=True)
    parser.add_argument("-o", type=str, choices=["lex", "freq"], default="freq",
                              help="Ordering {lex | lexicographic, freq | frequency} (default freq)")
    parser.add_argument("--minimizers", metavar="", type=str, help="Valid minimizers sets")
    parser.add_argument('--output', metavar='', type=str, help='Generates output of Super-mers with minimizers')
    parser.add_argument("-v", '--version', action='version', help="Version of the tool")

    readSplitDemo(parser.parse_args())

