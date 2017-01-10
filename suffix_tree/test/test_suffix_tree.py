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
        print()
        st.validate()

        self.assertTrue(st.search('abc$'))
        self.assertTrue(st.search('bc$'))
        self.assertTrue(st.search('c$'))
        self.assertTrue(st.search('$'))

        self.assertFalse(st.search('b$'))

    def test02(self):
        text = 'abcabxabd$'

        st = SuffixTree.build(text)
        st.pretty_print()
        print()
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

        st = SuffixTree.build(text)
        st.pretty_print()
        print()
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

    def test04(self):
        text = 'ebebcbaebe'

        st = SuffixTree.build(text)
        st.pretty_print()
        print()
        st.validate()

        self.assertTrue(st.search('ebebcbaebe'))
        self.assertTrue(st.search('bebcbaebe'))
        self.assertTrue(st.search('ebcbaebe'))
        self.assertTrue(st.search('bcbaebe'))
        self.assertTrue(st.search('cbaebe'))
        self.assertTrue(st.search('baebe'))
        self.assertTrue(st.search('aebe'))
        self.assertTrue(st.search('be'))
        self.assertTrue(st.search('be'))
        self.assertTrue(st.search('e'))

        self.assertFalse(st.search('ce'))
    
    def test05(self):
        st = SuffixTree()
        st.add_string('abc')
        st.add_string('def')
        st.pretty_print()
        print()
        st.validate()

        self.assertTrue(st.search('abc'))
        self.assertTrue(st.search('bc'))
        self.assertTrue(st.search('c'))
        self.assertTrue(st.search('def'))
        self.assertTrue(st.search('ef'))
        self.assertTrue(st.search('f'))

        self.assertFalse(st.search('ce'))
    
    def test06(self):
        st = SuffixTree()
        st.add_string('abc')
        st.add_string('ab')
        st.pretty_print()
        print()
        st.validate()

        self.assertTrue(st.search('abc'))
        self.assertTrue(st.search('bc'))
        self.assertTrue(st.search('c'))
        self.assertTrue(st.search('ab'))
        self.assertTrue(st.search('b'))

        self.assertFalse(st.search('ce'))

    def test07(self):
        st = SuffixTree()
        st.add_string('abc')
        st.add_string('ab')
        st.pretty_print()
        print()
        st.validate()

        self.assertTrue(st.search('abc', exact=True))
        self.assertFalse(st.search('bc', exact=True))
        self.assertFalse(st.search('c', exact=True))
        self.assertTrue(st.search('ab', exact=True))
        self.assertFalse(st.search('b', exact=True))

        self.assertFalse(st.search('ce'))
