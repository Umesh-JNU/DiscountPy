import os
from  more_itertools import peekable
from collections import Counter

def countKmers(k: int, inputFile: str, bucket: str):
    def takeWhile(lines, m):
        _thisBin = Counter()

        while lines and lines.peek()[0] == m:
            _thisBin.update(next(lines)[1])

        return _thisBin

    def sliding(supermer):
        return [supermer[i : i + k] for i in range(len(supermer) - k + 1)]

    def kmer_fun(x):
        return x[0], sliding(x[1])
        
    with open(inputFile) as f:
        lines = peekable(map(lambda _: kmer_fun(_.rstrip('\n').split('\t')), f))
        
        with open(bucket, 'w+') as outfile:
            while lines:
                minimizer = lines.peek()[0]
                supermersThisBin = takeWhile(lines, minimizer)
                outfile.writelines(['%s\t%s\n'%(_, supermersThisBin[_]) for _ in supermersThisBin])

				