# suffix_tree

Python implementation of SuffixTree

Supports standard and generalized SuffixTree use.

Can accept non-textual sequences (for example, lists of numbers, or lists of tokens).

Code is based on Mark Nelson's code and blog post: http://marknelson.us/1996/08/01/suffix-trees/

## Usage

```python
from suffix_tree import SuffixTree

st = SuffixTree()

st.add_search_string('abracadabra')

for match in st.search_stream('Who said "abracadabra"?'):
	print('Matched at offset', match.offset)

```

