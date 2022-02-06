# python3
import sys

def BWT(text):
  result = []
  for i in range(len(text)):
    result.append( text )
    text = text[1:] + text[0]
  result.sort()
  return ''.join([s[-1] for s in result])

if __name__ == '__main__':
  text = sys.stdin.readline().strip()
  print(BWT(text))
