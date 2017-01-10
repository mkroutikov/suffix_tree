'''
Created on Jan 10, 2017

@author: mike
'''
from suffix_tree.suffix_tree import SuffixTree
from memory_profiler import profile
from suffix_tree.test.bench import random_string

@profile
def build():
    text = random_string(1000000)
    st = SuffixTree.build(text)
    return st

if __name__ == '__main__':
    
    build()
        