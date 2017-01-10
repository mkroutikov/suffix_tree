'''
Created on Jan 10, 2017

@author: mike
'''
import random
import time
from suffix_tree.suffix_tree import SuffixTree


ABC = 'abc'

def random_string(n):
    
    out = []
    for _ in range(n):
        out.append(ABC[random.randint(0, len(ABC)-1)])
    
    return ''.join(out)


if __name__ == '__main__':
    
    for n in [5, 5, 5, 5, 5, 5, 5, 10, 10, 10, 10, 100, 1000, 10000, 100000, 1000000, 10000000]:
        
        text = random_string(n)
        start = time.time()
        
        print(repr(text))
        st = SuffixTree.build(text)
        st.validate()
        
        elapsed = time.time() - start
        print(n, elapsed)
        