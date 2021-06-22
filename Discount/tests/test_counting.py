from itertools import groupby, chain
from os import mkdir
# from numba import njit, parallel

def flatten(sm):
	return chain.from_iterable(sm)

def sliding(supermer: str, k: int):
	return (supermer[i : i + k] for i in range(len(supermer) - k + 1))

def countKmers(k: int, inputFile: str, bucket: str):
    if not inputFile.endswith('.txt'):
        raise Exception("FileFormatError : required .txt file", inputFile.split('/')[-1], "XXX.txt")
    else:
        try:
            mkdir(bucket)
        except OSError:
            pass
    
    with open(inputFile) as f:
        lines = map(lambda _: _.rstrip('\n').split('\t'), f)

        for minimizer, thisBin in groupby(lines, lambda _: _[0]):
            supermersThisBin = map(lambda _: _[1], thisBin)
            
            slide = map(lambda sm: sliding(sm, k), supermersThisBin)
            flat = flatten(slide)
            kmers = iter(sorted(flat))

            # kmers = sorted(flat)
            # print(minimizer, kmers)
            
            last = next(kmers)
            count = 1
            with open(bucket + '/' + str(minimizer) + '.txt', 'w+') as f:
                for _ in kmers:
                    if _ == last:
                        count += 1
                    else:
                        f.write(f'{last}\t{count}\n')
                        last = _
                        count = 1

                f.write(f'{last}\t{count}\n')

if __name__ == "__main__":
    file = 'C:/Users/umesh/Desktop/Discount-In-Python/Discount/output/sort_lex_10k.txt' 
    bucket = 'C:/Users/umesh/Desktop/Discount-In-Python/Discount/bucket'
    k = 28
    countKmers(k, file, bucket)