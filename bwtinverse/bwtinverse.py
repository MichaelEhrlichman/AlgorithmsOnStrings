# python3
import sys

def InverseBWT(bwt):

  rightcol = bwt
  rightindexes = [-1 for i in rightcol]
  counter = [0,0,0,0,0]
  for ix,ch in enumerate(rightcol):
    if ch == 'A':
      counter[0] += 1
      rightindexes[ix] = counter[0]
    elif ch == 'C':
      counter[1] += 1
      rightindexes[ix] = counter[1]
    elif ch == 'G':
      counter[2] += 1
      rightindexes[ix] = counter[2]
    elif ch == 'T':
      counter[3] += 1
      rightindexes[ix] = counter[3]
    elif ch == '$':
      counter[4] += 1
      rightindexes[ix] = counter[4]

  def get_left_ix(ch,ix):
    if ch == '$':
      return 0
    if ch == 'A':
      return ix
    if ch == 'C':
      return counter[0] + ix
    if ch == 'G':
      return counter[0] + counter[1] + ix
    if ch == 'T':
      return counter[0] + counter[1] + counter[2] + ix

  ix1 = 0
  result = ['$']
  for i in range(len(rightcol)-1):
    rightchar = rightcol[ix1]
    result.append(rightcol[ix1])
    rightindex = rightindexes[ix1]
    ix1 = get_left_ix(rightchar,rightindex)
  return ''.join(result[::-1])


if __name__ == '__main__':
    bwt = sys.stdin.readline().strip()
    print(InverseBWT(bwt))
