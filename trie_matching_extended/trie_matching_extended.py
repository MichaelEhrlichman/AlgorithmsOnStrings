# python3
import sys

def build_trie(patterns):
    trie = dict()
    trie[0] = dict()
    terms = set()
    maxnode = 0
    for pattern in patterns:
        node = 0
        for ix,ch in enumerate(pattern):
            if ch in trie[node].keys():
                node = trie[node][ch]
            else:
                maxnode += 1
                trie[maxnode] = dict()
                trie[node][ch] = maxnode
                node = maxnode
            if ix == len(pattern)-1:
                terms.add(node)
                    
    return trie, terms

def solve (text, n, patterns):
    trie, terms = build_trie(patterns)
    result = []
    for i in range(len(text)):
        node = 0
        for ch in text[i:]:
            if ch in trie[node]:
                node = trie[node][ch]
                if len(trie[node]) == 0 or node in terms:
                    result.append(i)
                    break
            else:
                break
    return result

text = sys.stdin.readline ().strip ()
n = int (sys.stdin.readline ().strip ())
patterns = []
for i in range (n):
	patterns += [sys.stdin.readline ().strip ()]

ans = solve (text, n, patterns)

sys.stdout.write (' '.join (map (str, ans)) + '\n')
