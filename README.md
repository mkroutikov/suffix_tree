# suffix_tree

Python implementation of SuffixTree

Supports standard and generalized SuffixTree use.

Can accept non-textual sequences (for example, lists of numbers, or lists of tokens).

Code is based on Mark Nelson's code and blog post: http://marknelson.us/1996/08/01/suffix-trees/

## Usage

```python
from suffix_tree import SuffixTree

st = SuffixTree.build('abracadabra')  # note the absence of terminator!

st.match('abra')
> True  # because "abra" is a valid suffix

st.match('abraca')
> False  # because "abraca" is not a valid suffix

st.match('abracadabra', exact=True)
> True  # because "abracadabra matches the indexed string exactly

st.match('bracadabra', exact=True)
> False  # because "bracadabra does not match the indexed string exactly
```

```python
from suffix_tree import SuffixTree

st = SuffixTree()

st.add_string('abracadabra')
st.add_string('said')

stream_search = st.stream_search()
for offset,c in enumerate('Who said "abracadabra"?'):
	for string_index in stream_search.feed(c):
		print('String with index %s found at end offset %s" % (string_index, offset))

```

