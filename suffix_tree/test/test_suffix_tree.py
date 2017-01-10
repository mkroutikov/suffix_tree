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

        self.assertTrue(st.match('abc$'))
        self.assertTrue(st.match('bc$'))
        self.assertTrue(st.match('c$'))
        self.assertTrue(st.match('$'))

        self.assertFalse(st.match('b$'))

    def test02(self):
        text = 'abcabxabd$'

        st = SuffixTree.build(text)
        st.pretty_print()
        print()
        st.validate()

        self.assertTrue(st.match('abcabxabd$'))
        self.assertTrue(st.match('bcabxabd$'))
        self.assertTrue(st.match('cabxabd$'))
        self.assertTrue(st.match('abxabd$'))
        self.assertTrue(st.match('bxabd$'))
        self.assertTrue(st.match('xabd$'))
        self.assertTrue(st.match('abd$'))
        self.assertTrue(st.match('bd$'))
        self.assertTrue(st.match('d$'))
        self.assertTrue(st.match('$'))

        self.assertFalse(st.match('b$'))

    def test03(self):
        text = 'ebebcbae$'

        st = SuffixTree.build(text)
        st.pretty_print()
        print()
        st.validate()

        self.assertTrue(st.match('ebebcbae$'))
        self.assertTrue(st.match('bebcbae$'))
        self.assertTrue(st.match('ebcbae$'))
        self.assertTrue(st.match('bcbae$'))
        self.assertTrue(st.match('cbae$'))
        self.assertTrue(st.match('bae$'))
        self.assertTrue(st.match('ae$'))
        self.assertTrue(st.match('e$'))
        self.assertTrue(st.match('$'))

        self.assertFalse(st.match('b$'))

    def test04(self):
        text = 'ebebcbaebe'

        st = SuffixTree.build(text)
        st.pretty_print()
        print()
        st.validate()

        self.assertTrue(st.match('ebebcbaebe'))
        self.assertTrue(st.match('bebcbaebe'))
        self.assertTrue(st.match('ebcbaebe'))
        self.assertTrue(st.match('bcbaebe'))
        self.assertTrue(st.match('cbaebe'))
        self.assertTrue(st.match('baebe'))
        self.assertTrue(st.match('aebe'))
        self.assertTrue(st.match('be'))
        self.assertTrue(st.match('be'))
        self.assertTrue(st.match('e'))

        self.assertFalse(st.match('ce'))
    
    def test05(self):
        st = SuffixTree()
        st.add_string('abc')
        st.add_string('def')
        st.pretty_print()
        print()
        st.validate()

        self.assertTrue(st.match('abc'))
        self.assertTrue(st.match('bc'))
        self.assertTrue(st.match('c'))
        self.assertTrue(st.match('def'))
        self.assertTrue(st.match('ef'))
        self.assertTrue(st.match('f'))

        self.assertFalse(st.match('ce'))
    
    def test06(self):
        st = SuffixTree()
        st.add_string('abc')
        st.add_string('ab')
        st.pretty_print()
        print()
        st.validate()

        self.assertTrue(st.match('abc'))
        self.assertTrue(st.match('bc'))
        self.assertTrue(st.match('c'))
        self.assertTrue(st.match('ab'))
        self.assertTrue(st.match('b'))

        self.assertFalse(st.match('ce'))

    def test07(self):
        st = SuffixTree()
        st.add_string('abc')
        st.add_string('ab')
        st.pretty_print()
        print()
        st.validate()

        self.assertTrue(st.match('abc', exact=True))
        self.assertFalse(st.match('bc', exact=True))
        self.assertFalse(st.match('c', exact=True))
        self.assertTrue(st.match('ab', exact=True))
        self.assertFalse(st.match('b', exact=True))

        self.assertFalse(st.match('ce'))
