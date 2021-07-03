<div align="center">
 <h1>DiscountPy : <i>k-mer counting tool</i></h1>
 <img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=darkgreen" />
 <img alt="Jupyter" src="https://img.shields.io/badge/Jupyter-%23F37626.svg?style=for-the-badge&logo=Jupyter&logoColor=white" />
 <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/poetry?label=Python-poetry&style=for-the-badge">
</div>

<div align="center">
 
[![GitHub license](https://img.shields.io/github/license/Umesh-JNU/DiscountPy?color=orange&style=flat-square)](https://github.com/Umesh-JNU/DiscountPy)
[![GitHub release](https://img.shields.io/github/release/Umesh-JNU/DiscountPy?logo=GitHub&logoColor=FFFFFF&style=flat-square)](https://github.com/Umesh-JNU/DiscountPy/releases/)
[![GitHub tag](https://img.shields.io/github/tag/Umesh-JNU/DiscountPy?style=flat-square)](https://github.com/Umesh-JNU/DiscountPy/tags/)
[![GitHub commits](https://img.shields.io/github/commits-since/Umesh-JNU/DiscountPy/v0.1.0.svg?color=green&style=flat-square)](https://github.com/Umesh-JNU/DiscountPy/commit/)
[![Python 3.6+](https://img.shields.io/badge/python-3.9+-3776AB?logo=Python&logoColor=FFFFFF&style=flat-square)](https://www.python.org/)
<!-- [![Visitor count](https://shields-io-visitor-counter.herokuapp.com/badge?page=Umesh-JNU.Discount-In-Python.Discount&color=1D70B8&logo=GitHub&logoColor=FFFFFF&style=flat-square)](https://github.com/Umesh-JNU/Discount-In-Python) -->

<a href="https://github.com/Umesh-JNU/DiscountPy/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/Umesh-JNU/DiscountPy"></a>
<a href="https://github.com/Umesh-JNU/DiscountPy/network"><img alt="GitHub forks" src="https://img.shields.io/github/forks/Umesh-JNU/DiscountPy"></a>
<a href="https://github.com/Umesh-JNU/DiscountPy/pulls"><img src="https://img.shields.io/github/issues-pr/Umesh-JNU/DiscountPy" alt="Pull Requests Badge"/></a>
<a href="https://github.com/Umesh-JNU/DiscountPy/issues"><img alt="GitHub issues" src="https://img.shields.io/github/issues/Umesh-JNU/DiscountPy"></a>
</div>

# Contents:
  - [Requirements](#requirements)
  - [Setup](#setup)
  - [Some codes](#some-codes)
  

## Requirements
>   1. <strong><i>DiscountPy</i></strong> is completely Python based. To run it on your machine, ` python >= 3.9 ` is required.<br>
>   2. <strong><i>[Poetry](https://python-poetry.org/)</i></strong> is a tool for dependency management and packaging in Python. Make sure to install it.<br>
>   3. Try to run all the commands in ` Powershell `

## Setup
1. Installation: <i>You can download the zip file or clone it.</i>
2. Setting up: <i>First install all the dependencies and create ` virtual environment `. To do so, run the following commands in workspace terminal.</i>

       poetry install
       poetry update
3. Now configure python interpreter. For configuring, first get the ` env ` path. To get the ` env ` information, run the following command.

       poetry env info
       
      * Or to know only path, run
         
            poetry env info --path
      
>    To know more about poetry, follow [Poetry](https://python-poetry.org/)

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
