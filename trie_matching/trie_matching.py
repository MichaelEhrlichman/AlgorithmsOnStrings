# python3
import sys

def build_trie(patterns):
    tree = dict()
    tree[0] = dict()
    maxnode = 0
    for pattern in patterns:
        node = 0
        for ch in pattern:
            if ch in tree[node].keys():
                node = tree[node][ch]
            else:
                maxnode += 1
                tree[maxnode] = dict()
                tree[node][ch] = maxnode
                node = maxnode
    return tree

def solve (text, n, patterns):
    trie = build_trie(patterns)
    result = []
    for i in range(len(text)):
        node = 0
        for ch in text[i:]:
            if ch in trie[node]:
                node = trie[node][ch]
                if len(trie[node]) == 0:
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
