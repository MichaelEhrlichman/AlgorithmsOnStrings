# python3
import sys

def build_suffix_array(text):
    result = []
    result_ixs = []
    for six in range(len(text)):
        lo = 0
        hi = len(result)-1
        while hi >= lo:
            midix = lo+(hi-lo)//2
            if text[six:] == result[midix]:
                lo = midx
                break
            elif text[six:] < result[midix]:
                hi = midix-1
            else:
                lo = midix+1
        result.insert(lo,text[six:])
        result_ixs.insert(lo,six)
    return result_ixs

if __name__ == '__main__':
    text = sys.stdin.readline().strip()
    print(" ".join(map(str, build_suffix_array(text))))
