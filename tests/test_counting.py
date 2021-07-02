# version 4
import os
from more_itertools import peekable
from collections import Counter

def countKmers(k: int, inputFile: str, bucket: str):
    if not inputFile.endswith('.txt'):
        raise Exception("FileFormatError : required .txt file", inputFile.split('/')[-1], "XXX.txt")
    else:
        try:
            path = bucket.rsplit('/', 1)[0]
            print(path)
            os.mkdir(path)
        except OSError:
            pass
    
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

if __name__ == "__main__":
    file = input('Enter inputfile Path : ')
    bucket = input('Bucket path : ')
    k = int(input("Enter k : "))
    countKmers(k, file, bucket)