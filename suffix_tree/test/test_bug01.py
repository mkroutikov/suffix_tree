'''
Created on Jan 10, 2017

@author: mike
'''
import unittest
from suffix_tree.suffix_tree import SuffixTree



class TestBug01(unittest.TestCase):
    
    
    def test(self):
        text = 'bbacbaccba'
        
        st = SuffixTree.build(text)
        st.pretty_print()
        st.validate()