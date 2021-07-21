import random

class DNAHelpers:
    """
    A collection of helper functions for DNA manipulation.
    """
    def __init__(self):
        pass

    def charComplement(self, bp):
        """
        Returns the complement of the input character.
        :param char: A DNA character.
        :return: The complement of the input character.
        """
        # Return the complement of the input character.
        if bp == 'A':
            return 'T'
        elif bp == 'C':
            return 'G'
        elif bp == 'G':
            return 'C'
        elif bp == 'T':
            return 'A'
        else:
            raise ValueError("Error: " + bp + " is not a nucleotide")

    def complement(self, data: str) -> str:
        """
        Returns the complement of a DNA string.
        :param dna: A DNA string.
        :return: The complement of the DNA string.
        """
        # Return the complement of the dna string.
        return ''.join(map(self.charComplement, data))

    def reverseComplement(self, dna):
        """
        Returns the reverse complement of a DNA string.
        :param dna: A DNA string.
        :return: The reverse complement of the DNA string.
        """
        # Return the reverse complement of the dna string.
        return self.complement(dna)[::-1]
    
    def extendSeq(seq, steps):
        """
        Extends a DNA sequence by a given number of steps.
        :param seq: The DNA sequence to extend.
        :param steps: The number of steps to extend.
        :param generator: The generator to use to generate the new DNA sequence.
        :return: The extended DNA sequence.
        """
        # Return the extended DNA sequence.
        return seq + ''.join([random.choice(['A','C','G','T']) for i in range(steps)])

    def randomSequence(self, length):
        """
        Returns a random DNA sequence of the given length.
        :param length: The length of the DNA sequence.
        :return: The random DNA sequence.
        """
        return self.extendSeq('', length)

    def kmerPrefix(self, seq, k):
        """
        Returns the k-mer prefix of a DNA sequence.
        :param seq: The DNA sequence.
        :param k: The length of the k-mer.
        :return: The k-mer prefix.
        """
        return seq[:k]
    def kmerSuffix(self, seq, k):
        """
        Returns the k-mer suffix of a DNA sequence.
        :param seq: The DNA sequence.
        :param k: The length of the k-mer.
        :return: The k-mer suffix.
        """
        return seq[-k:]

    def withoutPrefix(self, seq, k):
        """
        Returns the DNA sequence without the k-mer prefix.
        :param seq: The DNA sequence.
        :param k: The length of the k-mer.
        :return: The DNA sequence without the k-mer prefix.
        """
        return seq[k:]
    
    def withoutSuffix(self, seq, k):  
        """
        Returns the DNA sequence without the k-mer suffix.
        :param seq: The DNA sequence.
        :param k: The length of the k-mer.
        :return: The DNA sequence without the k-mer suffix.
        """
        return seq[:-k]