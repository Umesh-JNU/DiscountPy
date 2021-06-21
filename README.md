<div align="center">
 <h1>DiscountPy : <i>k-mer counting tool</i></h1>
 <img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=darkgreen" />
 <img alt="Jupyter" src="https://img.shields.io/badge/Jupyter-%23F37626.svg?style=for-the-badge&logo=Jupyter&logoColor=white" />
 <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/poetry?label=Python-poetry&style=for-the-badge">
</div>

<div align="center">
 
[![MIT](https://img.shields.io/apm/l/vim-mode?color=orange&logo=orange&logoColor=yellow&style=flat-square)](https://github.com/Umesh-JNU/Discount-In-Python/LICENSE)
[![GitHub release](https://img.shields.io/github/v/release/Umesh-JNU/Discount-In-Python?logo=GitHub&logoColor=FFFFFF&style=flat-square)](https://github.com/Umesh-JNU/Discount-In-Python)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-3776AB?logo=Python&logoColor=FFFFFF&style=flat-square)](https://www.python.org/)
<!-- [![Visitor count](https://shields-io-visitor-counter.herokuapp.com/badge?page=Umesh-JNU.Discount-In-Python.Discount&color=1D70B8&logo=GitHub&logoColor=FFFFFF&style=flat-square)](https://github.com/Umesh-JNU/Discount-In-Python) -->

<a href="https://github.com/Umesh-JNU/Discount-In-Python/stargazers"><img src="https://img.shields.io/github/stars/Umesh-JNU/Discount-In-Python" alt="Stars Badge"/></a>
<a href="https://github.com/Umesh-JNU/Discount-In-Python/network/members"><img src="https://img.shields.io/github/forks/Umesh-JNU/Discount-In-Python" alt="Forks Badge"/></a>
<a href="https://github.com/Umesh-JNU/Discount-In-Python/pulls"><img src="https://img.shields.io/github/issues-pr/Umesh-JNU/Discount-In-Python" alt="Pull Requests Badge"/></a>
<a href="https://github.com/Umesh-JNU/Discount-In-Python/issues"><img src="https://img.shields.io/github/issues/Umesh-JNU/Discount-In-Python" alt="Issues Badge"/></a>
</div>

# Contents:
  - [Requirements](#requirements)
  - [Setup](#setup)
  - [Some codes](#some-codes)
  

## Requirements
<strong><i>DiscountPy</i></strong> is completely Python based. To run it on your machine, ` python >= 3.7 ` is required.

## Setup
1. Installation: <i>You can download the zip file or clone it.</i>
2. Setting up: <i>First install all the dependencies and create ` virtual environment `. To do so, run the following commands in workspace terminal.</i>

       poetry install
       poetry update
      
Now ` DiscountPy ` is ready to be run.

## Some codes
``` DiscountPy ``` is a k-mer counting tool, it gives you ` three orderings ` for counting the k-mers.
* ` -k ` : Length of the k-mer
* ` -m ` : Width of the minimizers
* ` -f ` : Input dataset (.fasta)
* ` -o ` : Order (lex | freq)
* ` --minimizers ` : Universal minimizer set 

#### How to use?
1. To get the hashed super-mers with minimizers
   * By lexicographically ordered

         discount -k 28 -o lex -f data/SRR094926.fasta 
     or
       
         discount -k 28 -m 10 lex -f data/SRR094926.fasta
         
   * By frequency ordering

         discount -k 28 -f data/SRR094926.fasta
         
     or you can skip the ` -o ` in frequency order as default value is ` -o freq `
      
         discount -k 28 -o freq -f data/SRR094926.fasta

   * By universal frequency ordering

         discount -k 28 -f data/SRR094926.fasta --minimizers PASHA/pasha_all_28_10.txt
         
       or
         
         discount -k 28 -o freq -f data/SRR094926.fasta --minimizers PASHA/pasha_all_28_10.txt
2. To generate file of the hashed super-mers:
      
       discount -k 28 -o freq -f data/SRR094926.fasta --minimizers PASHA/pasha_all_28_10.txt --output output/xxx.txt
 
 3. At finally getting the counts of the ` k-mers `:
     * You have to sort the [above](#to-generate-file-of-the-hashed-super-mers:) generated file externally and input that file.
         
           discount -k 28 -f sortedXYZ.txt --count directory/to/counted-kmer-file
      

## Query
[![Ask Me Anything !](https://img.shields.io/badge/Ask%20me-anything-1abc9c.svg)](https://GitHub.com/Umesh-JNU/Discount-In-Python)
