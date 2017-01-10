'''
Created on Jan 9, 2017

@author: mkroutikov
'''
import unittest
from suffix_tree.suffix_tree import SuffixTree



class TestCst(unittest.TestCase):

    def test01(self):
        text = 'abc$'

        st = SuffixTree().build(text)
        st.pretty_print()
        st.validate()

        self.assertTrue(st.search('abc$'))
        self.assertTrue(st.search('bc$'))
        self.assertTrue(st.search('c$'))
        self.assertTrue(st.search('$'))

        self.assertFalse(st.search('b$'))

    def test02(self):
        text = 'abcabxabd$'

        st = SuffixTree().build(text)
        st.validate()

        self.assertTrue(st.search('abcabxabd$'))
        self.assertTrue(st.search('bcabxabd$'))
        self.assertTrue(st.search('cabxabd$'))
        self.assertTrue(st.search('abxabd$'))
        self.assertTrue(st.search('bxabd$'))
        self.assertTrue(st.search('xabd$'))
        self.assertTrue(st.search('abd$'))
        self.assertTrue(st.search('bd$'))
        self.assertTrue(st.search('d$'))
        self.assertTrue(st.search('$'))

        self.assertFalse(st.search('b$'))

    def test03(self):
        text = 'ebebcbae$'

        st = SuffixTree().build(text)
        st.validate()

        self.assertTrue(st.search('ebebcbae$'))
        self.assertTrue(st.search('bebcbae$'))
        self.assertTrue(st.search('ebcbae$'))
        self.assertTrue(st.search('bcbae$'))
        self.assertTrue(st.search('cbae$'))
        self.assertTrue(st.search('bae$'))
        self.assertTrue(st.search('ae$'))
        self.assertTrue(st.search('e$'))
        self.assertTrue(st.search('$'))

        self.assertFalse(st.search('b$'))
