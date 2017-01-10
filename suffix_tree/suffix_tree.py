'''
Created on Jan 10, 2017

@author: mike
'''
import collections
from types import SimpleNamespace


class Edge(collections.namedtuple('_Edge', ['id', 'offset', 'length', 'text_index', 'parent'])):
    """Represents edge in the suffix tree.
    It is "growing" from the parent edge
    Each edge has its unique id and stores the offset and length of substring it is representing
    """
    
    def updated(self, offset=None, length=None, text_index=None, parent=None):
        
        if offset is None:
            offset = self.offset
        
        if length is None:
            length = self.length
        
        if parent is None:
            parent = self.parent
        
        if text_index is None:
            text_index = self.text_index

        return Edge(self.id, offset, length, text_index, parent)


class Terminator(collections.namedtuple('_Terminator', ['text_index', 'length'])):
    """Represents a terminator symbol.
    This class is a lightweight one, but equals only to the same instance.
    Each string put into the Suffix Tree will get its own unique terminator.
    """

    def __eq__(self, other):
        return self is other
    
    def __hash__(self):
        return hash(type(self)) + hash((self.text_index, self.length))

    def __repr__(self):
        return '$(offset=%s, length=%s)' % (self.text_index, self.length)


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
        self._edges[edge.parent][self._texts[edge.text_index][edge.offset]] = edge
    
    def _find_edge(self, node_id, token):
        return self._edges[node_id].get(token)

    def _split_edge(self, edge, length):
        assert 0 < length < edge.length
        
        new_edge = Edge(self._get_id(), edge.offset, length, edge.text_index, edge.parent)
        self._register_edge(new_edge)  # this effectively removes the old edge as new_edge overrides edge
        
        edge = edge.updated(parent=new_edge.id, offset=edge.offset+length, length=edge.length-length)
        self._register_edge(edge)
        
        return new_edge.id

    def _canonize(self, cursor):
        """suffix represents current search state in the tree (edge id, offset, and length).
        """
        if cursor.length <= 0:
            return
        
        edge = self._find_edge(cursor.node, self._texts[cursor.text_index][cursor.offset])
        while edge.length < cursor.length:
            # need to move to the next edge
            cursor.length -= edge.length
            cursor.offset += edge.length
            cursor.node = edge.id
            edge = self._find_edge(cursor.node, self.token[cursor.offset])

        if edge.length == cursor.length:
            cursor.length -= edge.length
            cursor.offset += edge.length
            cursor.node = edge.id
            
    def _extend(self, cursor):
        
        last_parent_node = -1  # for suffix links
        
        while True:
            
            if cursor.length <= 0:  # explicit edge
                assert cursor.length >= -1
                edge = self._find_edge(cursor.node, self._texts[cursor.text_index][cursor.offset + cursor.length])
                if edge is not None:
                    break
                parent_node = cursor.node
            else:
                edge = self._find_edge(cursor.node, self._texts[cursor.text_index][cursor.offset])
                if self._texts[cursor.text_index][cursor.offset + cursor.length] == self._texts[edge.text_index][edge.offset + cursor.length]:
                    break
                parent_node = self._split_edge(edge, cursor.length)

            new_edge = Edge(self._get_id(), cursor.offset + cursor.length, len(self._texts[cursor.text_index]) - cursor.offset - cursor.length, cursor.text_index, parent_node)  # length=None means "leaf node - till the end..."
            self._register_edge(new_edge)
            self._terminators[new_edge.id].add(cursor.terminator)
            
            if last_parent_node > 0:
                self._nodes[last_parent_node] = parent_node  # add suffix link
            
            last_parent_node = parent_node
            
            if cursor.node == 0:  # already at root
                cursor.offset += 1
                cursor.length -= 1
            else:
                cursor.node = self._nodes[cursor.node]
            self._canonize(cursor)
        
        if last_parent_node > 0:
            self._nodes[last_parent_node] = parent_node

        cursor.length += 1
        self._canonize(cursor)

    def _terminate(self, cursor):
        
        last_parent_node = -1  # for suffix links
        
        while True:
            
            if cursor.length <= 0:  # explicit edge
                if cursor.node > 0:
                    self._terminators[cursor.node].add(cursor.terminator)
                break

            edge = self._find_edge(cursor.node, self._texts[cursor.text_index][cursor.offset])
            parent_node = self._split_edge(edge, cursor.length)
            assert parent_node > 0
            self._terminators[parent_node].add(cursor.terminator)
            
            if last_parent_node > 0:
                self._nodes[last_parent_node] = parent_node  # add suffix link
            
            last_parent_node = parent_node
            
            if cursor.node == 0:  # already at root
                cursor.offset += 1
                cursor.length -= 1
            else:
                cursor.node = self._nodes[cursor.node]
            self._canonize(cursor)
        
        if last_parent_node > 0:
            self._nodes[last_parent_node] = parent_node

    def build(self, text):
        
        text_index = len(self._texts)
        self._texts.append(text)
        cursor = SimpleNamespace(node=0, offset=0, length=0, terminator=Terminator(text_index,0), text_index=text_index)

        for i in range(len(text)):
            assert cursor.offset + cursor.length == i, repr(i) + ' ' + repr(cursor)
            assert cursor.length >= 0
            self._extend(cursor)
        
        self._terminate(cursor)

        return self  # convenience, like this: tree = SuffixTree().build("abracadabra")

    def edge_text(self, edge):
        text = self._texts[edge.text_index]
        return text[edge.offset:edge.offset+edge.length]

    def pretty_print(self, root=0, level=0):
        for key in sorted(self._edges[root].keys()):
            edge = self._find_edge(root, key)
            print('\t' * level, self.edge_text(edge), self._terminators[edge.id] if self._terminators[edge.id] else  '')
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

            if x != self._texts[current_edge.text_index][current_edge.offset + ii]:
                return False
            ii += 1
        
        if current_edge is not None:
            if ii == current_edge.length:
                if self._terminators[current_edge.id]: 
                    return True

        return False
    
    def validate(self):
        """Validates tree by traversing it and checking that all suffixes are present in the tree exactly once"""
        
        suffixes = collections.defaultdict(int)
        def walk_tree(node=0, suffix=''):
            for term in self._terminators[node]:  # leaf node
                text = self._texts[term.text_index]
                assert text[-len(suffix):] == suffix, repr(suffix) + ' | ' + repr(text)
                suffixes[term.text_index, len(suffix)] += 1
            
            for edge in self._edges[node].values():
                leg = self.edge_text(edge)
                assert len(leg) > 0, edge
                walk_tree(edge.id, suffix+leg)
        
        walk_tree()
        for i in range(0, len(self._texts)):
            for j in range(1, len(self._texts[i])):
                assert suffixes[i, j] == 1, (i, j)
