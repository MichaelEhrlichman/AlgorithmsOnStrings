# python3
import sys
GRAPHICS = 0
if GRAPHICS:
  import graphics as gr
from math import cos,sin,pi
sys.setrecursionlimit(10000)

class Node():
  def __init__(self,edge,label=-1):
    self.edge = edge  # label on edge going into node
    self.label = label  # used at terminus.  holds start ix for that path
    self.children = {} # holds outgoing nodes, indexed by leading character
    self.poundString = False
    self.dollarString = False
  @staticmethod
  def myPrint(node,level=0):
    pad = '   '*level
    print(pad+node.edge)
    if len(node.children) > 0:
      print(pad+' - '.join([s for s in node.children.keys()]))
      for child in node.children.values():
        node.myPrint(child,level+1)

winx,winy = 1700,1300
csize = 5
height = 35
twopi = 2*pi

if GRAPHICS:
  def center_pt(point):
    return gr.Point(point.x+winx/2, point.y+winy/2)

  def draw_node(win,node,hite,angle,parentloc,text):

    loc = gr.Point(hite*cos(angle),hite*sin(angle)) + parentloc
    cir = gr.Circle(center_pt(loc),csize)

    edge = gr.Line(center_pt(parentloc), center_pt(loc))

    midpt = (loc+parentloc)/2
    edgelabel = text[node.edge[0]:node.edge[1]]
    if '#' in edgelabel:
      endix = edgelabel.index('#')+1
    else:
      endix = len(edgelabel)
    edge_txt = gr.Text(center_pt(midpt),str(edgelabel[:endix])+'\n'+str(node.label))
    edge_txt = gr.Text(center_pt(midpt),str(edgelabel[:endix]))
    edge_txt.setSize(10)
    edge_txt.setStyle('bold')
    if node.poundString and node.dollarString:
      edge_txt.setFill('green')
    elif node.poundString:
      edge_txt.setFill('blue')
    elif node.dollarString:
      edge_txt.setFill('red')

    edge.draw(win)
    cir.setFill('white')
    cir.draw(win)
    edge_txt.draw(win)

    nchild = len(node.children)
    for i,child in enumerate(node.children.values()):
      if hite == 0:
        draw_node(win, child, 7*height, twopi*i/nchild,loc,text)
      else:
        draw_node(win, child, hite-height, (angle+pi/2) - pi*i/(nchild-1), loc, text)

  def gr_tree(root,title,text):
    win = gr.GraphWin(title,winx,winy)
    draw_node(win,root,0,0,gr.Point(0,0),text)
    win.getMouse()

# testnode = Node( (0,1) )
# testnode.children['1'] = Node((0,1))
# testnode.children['1'].children['a'] = Node((0,1))
# testnode.children['1'].children['b'] = Node((0,1))
# testnode.children['1'].children['c'] = Node((0,1))
# testnode.children['1'].children['c'].children['x'] = Node((0,1))
# testnode.children['1'].children['c'].children['y'] = Node((0,1))
# testnode.children['1'].children['c'].children['z'] = Node((0,1))
# testnode.children['1'].children['d'] = Node((0,1))
# testnode.children['2'] = Node((0,1))
# testnode.children['2'].children['a'] = Node((0,1))
# testnode.children['2'].children['b'] = Node((0,1))
# testnode.children['2'].children['c'] = Node((0,1))
# testnode.children['2'].children['d'] = Node((0,1))
# testnode.children['3'] = Node((0,1))

def build_trie(text):
  root = Node((-1,-1))
  m = len(text)
  for ix in range(len(text)-1,-1,-1):
    suffix = text[ix:]
    poundString = False
    dollarString = True
    if '#' in suffix:
      poundString = True
      dollarString = False
    node = root
    if node.edge[0] > -1:
      nodeEdge = text[node.edge[0]:node.edge[1]]
    else:
      nodeEdge = '*'
    #walk as far as we can along the edge
    suix = 0
    while suix < len(suffix):
      edgeix = 0
      stashPoundString = node.poundString
      stashDollarString = node.dollarString
      while suffix[suix] == nodeEdge[edgeix]:
        node.poundString = node.poundString or poundString
        node.dollarString = node.dollarString or dollarString
        suix += 1
        edgeix += 1
        if edgeix == len(nodeEdge) or suix == len(suffix):
          break
      if suix == len(suffix):
        # reached end of suffix
        break
      elif edgeix == len(nodeEdge):
        # reached the end of an edge
        if suffix[suix] in node.children:
          node = node.children[suffix[suix]]
          nodeEdge = text[node.edge[0]:node.edge[1]]
          continue
        else:
          node.children[suffix[suix]] = Node( (ix+suix,m), ix )
          node.children[suffix[suix]].poundString = poundString
          node.children[suffix[suix]].dollarString = dollarString
          break
      elif nodeEdge == "*":
        #node is root
        if suffix[0] in node.children.keys():
          node = node.children[suffix[0]]
          nodeEdge = text[node.edge[0]:node.edge[1]]
          continue
        else:
          node.children[suffix[0]] = Node( (ix,m), ix)
          node.children[suffix[0]].poundString = poundString
          node.children[suffix[0]].dollarString = dollarString
          break
      else:
        # need to break edge
        # make a new node with a dummy key and move all children to the new node, then rename
        node.children['@'] = Node( (node.edge[0]+edgeix,node.edge[1]), node.label ) # nodeEdge[edgeix:], node.label )
        node.children['@'].poundString = stashPoundString
        node.children['@'].dollarString = stashDollarString
        for child_key in [k for k in node.children.keys() if k != '@']:
          node.children['@'].children[child_key] = node.children.pop(child_key)
        node.children[nodeEdge[edgeix]] = node.children.pop('@')
        node.label = -1 # internal nodes do not have labels
        node.edge = (node.edge[0], node.edge[0] + edgeix)  # node.edge[:edgeix]

        # hang new node off freshly broken node
        node.children[suffix[suix]] = Node( (ix+suix,m), ix)
        node.children[suffix[suix]].poundString = poundString
        node.children[suffix[suix]].dollarString = dollarString
        break

  return root

def get_unique_substrings_recurs(node,text):
  nodeEdge = text[node.edge[0]:node.edge[1]]
  child_results = [nodeEdge for i in range(len(node.children))]
  for ix,child in enumerate(node.children.values()):
    #print('from ',nodeEdge,' entering ', text[child.edge[0]:child.edge[1]])
    if child.dollarString and child.poundString:
      s = get_unique_substrings_recurs(child,text)
      if len(s) > 0:
        child_results[ix] = child_results[ix] + s
    elif child.dollarString:
      childNodeEdge = text[child.edge[0]:child.edge[1]]
      if '$' in childNodeEdge:
        if len(childNodeEdge) > 1:
          child_results[ix] = child_results[ix] + childNodeEdge[0] + '!'
      else:
        child_results[ix] = child_results[ix] + childNodeEdge + '!'
    #print('      returning s: ',child_results[ix])
  #print('         child_results ', child_results)
  res = [st for st in child_results if (len(st)>0 and '!' in st)]
  #print('<<< res is >>> ', res)
  if len(res) > 0:
    lens = [len(st) for st in res]
    minix = lens.index(min(lens))
    return res[minix]
  else:
    return ''

    #dsEdges = []
    #for child in node.children.values():
    #  s = get_unique_substrings_recurs(child,text)
    #  if len(s) > 0:
    #    dsEdges.append(s)
    ##dsEdges = [x for x in dsEdges if 'X' not in x]
    #if len(dsEdges) > 0:
    #  lengths = [len(x) for x in dsEdges]
    #  minix = lengths.index(min(lengths))
    #  return nodeEdge + dsEdges[minix]
    #else:
    #  return nodeEdge

def get_unique_substrings(root,text):
  result = []
  for child in root.children.values():
    if child.dollarString and child.poundString:
      #print("from root entering ", text[child.edge[0]:child.edge[1]])
      s = get_unique_substrings_recurs(child,text)
      #print('   s: ', s)
      if len(s) > 0:
        result.append(s[:-1])  # -1 to strip off ending '!' indicator
    elif child.dollarString:
      childNodeEdge = text[child.edge[0]:child.edge[1]]
      if '$' in childNodeEdge:
        if len(childNodeEdge) > 1:
          result.append(childNodeEdge[0])
      else:
        result.append(childNodeEdge)
  if len(result) > 0:
    lengths = [len(x) for x in result]
    minix = lengths.index(min(lengths))
    return result[minix]
  else:
    return text[-2]

def solve (p, q):
  hybrid = q+"#"+p+"$"
  suffix_tree = build_trie(hybrid)
  result = get_unique_substrings(suffix_tree,hybrid)
  if GRAPHICS:
    gr_tree(suffix_tree,'suffix tree',hybrid)
  return result

p = sys.stdin.readline ().strip ()
q = sys.stdin.readline ().strip ()
#q = 'CTGAC'
#p = 'ACTGC'
# p = "ATGCGATGACCTGACTGA"
# q = "CTCAACGTATTGGCCAGA"
#p='AAAAC'
#q='ACAAA'

ans = solve (p, q)

sys.stdout.write (ans + '\n')
