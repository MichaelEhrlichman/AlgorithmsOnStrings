# python3
import sys
import copy as cp

class Node():
    def __init__(self,edge,label=-1):
        self.edge = edge  # label on edge going into node
        self.label = label  # used at terminus.  holds start ix for that path
        self.children = {} # holds outgoing nodes, indexed by leading character
    @staticmethod
    def myPrint(node,level=0):
        pad = '   '*level
        print(pad+node.edge)
        if len(node.children) > 0:
            print(pad+' - '.join([s for s in node.children.keys()]))
            for child in node.children.values():
                node.myPrint(child,level+1)

def build_trie(text):
    root = Node('*')
    for ix in range(len(text)-1,-1,-1):
        suffix = text[ix:]
        node = root
        #walk as far as we can along the edge
        suix = 0
        while suix < len(suffix):
            edgeix = 0
            while suffix[suix] == node.edge[edgeix]:
                suix += 1
                edgeix += 1
                if edgeix == len(node.edge) or suix == len(suffix):
                    break
            if suix == len(suffix):
                # reached end of suffix
                break
            elif edgeix == len(node.edge):
                # reached the end of an edge
                if suffix[suix] in node.children:
                    node = node.children[suffix[suix]]
                else:
                    node.children[suffix[suix]] = Node( suffix[suix:], ix )
                    break
            elif node.edge == "*":
                #node is root
                if suffix[0] in node.children.keys():
                    node = node.children[suffix[0]]
                else:
                    node.children[suffix[0]] = Node( suffix, ix)
                    break
            else:
                # need to break edge
                # make a new node with a dummy key
                node.children['@'] = Node( node.edge[edgeix:], node.label )
                # move all children to the new node
                for child_key in [k for k in node.children.keys() if k != '@']:
                    node.children['@'].children[child_key] = node.children.pop(child_key)
                # replace dummy key with proper key
                node.children[node.edge[edgeix]] = node.children.pop('@')

                node.children[suffix[suix]] = Node( suffix[suix:], ix)
                node.edge = node.edge[:edgeix]
                node.label = -1  # internal nodes do not have labels
                # hang new node off freshly broken node
                #node.children[]
                break

    return root

import sys
sys.setrecursionlimit(10000)
def get_edges(node):
    result = [node.edge]
    if len(node.children) == 0:
        return result
    else:
        for n in node.children.values():
            result.extend(get_edges(n))
        return result

def build_suffix_tree(text):
    suffixes = []
    trie = build_trie(text)
    result = get_edges(trie)[1:]
    return result

if __name__ == '__main__':
  text = sys.stdin.readline().strip()
  # text = "CCGGTAAACG$"
  # text = 'A$'
  result = build_suffix_tree(text)
  print("\n".join(result))
