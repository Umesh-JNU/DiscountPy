from itertools import groupby, chain
# from numba import njit, parallel

def flatten(sm):
	return chain.from_iterable(sm)

def sliding(supermer: str, k: int):
	return (supermer[i : i + k] for i in range(len(supermer) - k + 1))

def countKmers(k: int, inputFile: str, bucket: str):
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
						f.write('{0}\t{1}\n'.format(last, count))
						last = _
						count = 1

				f.write('{0}\t{1}\n'.format(last, count))