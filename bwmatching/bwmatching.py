# python3
import sys


def PreprocessBWT(bwt):
  """
  Preprocess the Burrows-Wheeler Transform bwt of some text
  and compute as a result:
    * starts - for each character C in bwt, starts[C] is the first position 
        of this character in the sorted array of 
        all characters of the text.
    * occ_count_before - for each character C in bwt and each position P in bwt,
        occ_count_before[C][P] is the number of occurrences of character C in bwt
        from position 0 to position P inclusive.
  """
  counts = {'A':0, 'C':0, 'G':0, 'T':0, '$':0}
  for ch in bwt:
    counts[ch] += 1
  starts = {}
  starts['A'] = 1
  starts['C'] = counts['A'] + starts['A']
  starts['G'] = counts['C'] + starts['C']
  starts['T'] = counts['G'] + starts['G']

  n = len(bwt) + 1
  occ_count_before = {'A':[0 for i in range(n)], 'C':[0 for i in range(n)], 'G':[0 for i in range(n)], 'T':[0 for i in range(n)], '$':[-1 for i in range(n)]}
  for ix,ch in enumerate(bwt):
    for cur in ['A','C','G','T']:
      if cur == ch:
        occ_count_before[cur][ix+1] = occ_count_before[cur][ix] + 1
      else:
        occ_count_before[cur][ix+1] = occ_count_before[cur][ix]

  return starts, occ_count_before

def CountOccurrences(pattern, bwt, starts, occ_counts_before):
  """
  Compute the number of occurrences of string pattern in the text
  given only Burrows-Wheeler Transform bwt of the text and additional
  information we get from the preprocessing stage - starts and occ_counts_before.
  """
  patternlst = list(pattern)
  top = 0
  bottom = len(bwt)-1
  while top <= bottom:
    if patternlst:
      symbol = patternlst.pop()
      if symbol in bwt[top:bottom+1]:
        top = starts[symbol] + occ_counts_before[symbol][top] 
        bottom = starts[symbol] + occ_counts_before[symbol][bottom+1] - 1
      else:
        return 0
    else:
      return bottom-top+1
     


if __name__ == '__main__':
  bwt = sys.stdin.readline().strip()
  pattern_count = int(sys.stdin.readline().strip())
  patterns = sys.stdin.readline().strip().split()
  # Preprocess the BWT once to get starts and occ_count_before.
  # For each pattern, we will then use these precomputed values and
  # spend only O(|pattern|) to find all occurrences of the pattern
  # in the text instead of O(|pattern| + |text|).  
  starts, occ_counts_before = PreprocessBWT(bwt)
  occurrence_counts = []
  for pattern in patterns:
    occurrence_counts.append(CountOccurrences(pattern, bwt, starts, occ_counts_before))
  print(' '.join(map(str, occurrence_counts)))
