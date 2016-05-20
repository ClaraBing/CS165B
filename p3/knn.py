import sys
from math import sqrt
from collections import Counter

class Point:
  def __init__(self, ref, pos, label):
    self.dist = dist(ref, pos)
    self.label = label

  def __lt__(self, other):
    return self.dist < other.dist

  def __gt__(self, other):
    return self.dist > other.dist

def main():
  tmp, k, ftrain, ftest = sys.argv
  sample = train(ftrain)
  test(ftest, int(k), sample)
  return

def train(ftrain):
  f = open(ftrain, 'r')
  n, dim = [int(each) for each in f.readline().split() if each != ''] 
  sample = []
  for i in range(n):
    line = [float(each) for each in f.readline().split() if each != '']
    sample.append((line[:-1], int(line[-1])))
  return sample

def test(ftest, k, sample):
  f = open(ftest, 'r')
  n, dim = [int(each) for each in f.readline().split() if each != '']
  if dim != len(sample[0][0]):
    print "Dimension doesn't match. Aborting."
    exit(-1)
  for i in range(n):
    pos = [float(each) for each in f.readline().split() if each != '']
    points = [Point(pos, pair[0], pair[1]) for pair in sample]
    knn = sorted(points)[:k]
    counted = Counter([p.label for p in knn])
    cand = [each for each in counted if counted[each] == counted.most_common(1)[0][1]] # candidates: with max vote
    if len(cand) > 1: # a tie
      minDist = min([each.dist for each in knn if each.label in cand])
      byDist = [each for each in knn if each.dist <= minDist and each.label in cand]
      label = min([each.label for each in byDist]) if len(byDist) > 1 else byDist[0].label # check distance tie
    else:
      label = cand[0]
    print str(i+1) + '. ' + ' '.join([str(each) for each in pos]) + ' -- ' + str(label)
  return

def dist(x1, x2):
  return sqrt(sum([(x1[i]-x2[i])**2 for i in range(len(x1))]))

if __name__ == '__main__':
  main()
