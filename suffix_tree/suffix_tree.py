'''
Created on Jan 10, 2017

@author: mike
'''
import collections
from types import SimpleNamespace


class Edge(collections.namedtuple('_Edge', ['id', 'offset', 'length', 'parent'])):
    """Represents edge in the suffix tree.
    It is "growing" from the parent edge
    Each edge has its unique id and stores the offset and length of substring it is representing
    """
    
    def updated(self, offset=None, length=None, parent=None):
        
        if offset is None:
            offset = self.offset
        
        if length is None:
            length = self.length
        
        if parent is None:
            parent = self.parent

        return Edge(self.id, offset, length, parent)


class Terminator(collections.namedtuple('_Terminator', ['offset', 'length'])):
    """Represents a terminator symbol.
    This class is a lightweight one, but equals only to the same instance.
    Each string put into the Suffix Tree will get its own unique terminator.
    """

    def __eq__(self, other):
        return self is other
    
    def __hash__(self):
        return hash(type(self)) + hash((self.offset, self.length))

    def __repr__(self):
        return '$(offset=%s, length=%s)' % (self.offset, self.telength)


class SuffixTree:
    
    def __init__(self):
        
        self._texts = []  # holds all indexed "strings"
        
        self._edges = collections.defaultdict(dict)  # children edges
        self._nodes = collections.defaultdict(int)   # fall-back links
        self._terminators = collections.defaultdict(set)  # terminators for the edge (we always store terminators separately from the main string))
        
        self._id_seq = 0   # unique id for the edges. Edge with id=0 does not exist, as node 0 is implicitly the root node of our tree
    
    def _get_id(self):
        self._id_seq += 1
        return self._id_seq
    
    def _register_edge(self, edge):
        self._edges[edge.parent][self.text[edge.offset]] = edge
    
    def _find_edge(self, node_id, token):
        return self._edges[node_id].get(token)

    def _split_edge(self, edge, length):
        assert 0 < length < edge.length
        
        new_edge = Edge(self._get_id(), edge.offset, length, edge.parent)
        self._register_edge(new_edge)  # this effectively removes the old edge as new_edge overrides edge
        
        edge = edge.updated(parent=new_edge.id, offset=edge.offset+length, length=edge.length-length)
        self._register_edge(edge)
        
        return new_edge.id

    def _canonize(self, suffix):
        """suffix represents current search state in the tree (edge id, offset, and length).
        """
        if suffix.length <= 0:
            return
        
        edge = self._find_edge(suffix.node, self.text[suffix.offset])
        while edge.length <= suffix.length:
            # need to move to the next edge
            suffix.length -= edge.length
            suffix.offset += edge.offset
            suffix.node = edge.id
            if suffix.length > 0:
                edge = self._find_edge(suffix.node, self.token[suffix.offset])
    
    def _extend(self, pos, suffix):
        
        last_parent_node = -1  # for suffix links
        
        while True:
            parent_node = suffix.node
            
            if suffix.length <= 0:  # explicit edge
                edge = self._find_edge(suffix.node, self.text[pos])
                if edge is not None:
                    break
            else:
                edge = self._find_edge(suffix.node, self.text[suffix.offset])
                if self.text[pos] == self.text[edge.offset + suffix.length]:
                    break
                parent_node = self._split_edge(edge, suffix.length)
            
            new_edge = Edge(self._get_id(), pos, len(self.text) - pos, parent_node)
            self._register_edge(new_edge)
            
            if last_parent_node > 0:
                self._nodes[last_parent_node] = parent_node  # add suffix link
            
            last_parent_node = parent_node
            
            if suffix.node == 0:  # already at root
                suffix.offset += 1
                suffix.length -= 1
            else:
                suffix.node = self._nodes[suffix.node]
            self._canonize(suffix)
        
        if last_parent_node > 0:
            self._nodes[last_parent_node] = parent_node
        
        suffix.length += 1
        self._canonize(suffix)
    
    def build(self, text):
        
        if self._edges[0]:
            raise RuntimeError('Already built')
        
        self.text = text
        
        suffix = SimpleNamespace(node=0, offset=0, length=0)

        for i in range(len(text)):
            self._extend(i, suffix)

        return self  # convenience, like this: tree = SuffixTree("abracadabra").build()

    def edge_text(self, edge):
        return self.text[edge.offset:edge.offset+edge.length]

    def pretty_print(self, root=0, level=0):
        for key in sorted(self._edges[root].keys()):
            edge = self._find_edge(root, key)
            print('\t' * level, self.edge_text(edge))
            self.pretty_print(edge.id, level+1)

    def search(self, stream):

        current = 0
        current_edge = None
        ii = 0

        for x in stream:
            if current_edge is None or ii >= current_edge.length:
                current_edge = self._find_edge(current, x)
                if current_edge is None:
                    return False  # nothing found
                ii = 0
                current = current_edge.id

            if x != self.text[current_edge.offset + ii]:
                return False
            elif x == '$':
                return True
            ii += 1

        return False
    
    def validate(self):
        """Validates tree by traversing it and checking that all suffixes are present in the tree exactly once"""
        
        suffixes = collections.defaultdict(int)
        def walk_tree(node=0, suffix=''):
            
            if len(self._edges[node]) == 0:  # leaf node
                assert self.text[-len(suffix):] == suffix, suffix
                suffixes[len(suffix)] += 1
                return
            
            for edge in self._edges[node].values():
                leg = self.edge_text(edge)
                assert len(leg) > 0, edge
                walk_tree(edge.id, suffix + leg)
        
        walk_tree()
        for i in range(1, len(self.text)):
            assert suffixes[i] == 1, i
