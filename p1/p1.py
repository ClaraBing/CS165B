import sys
from numpy import matrix
from numpy import linalg
from math import sqrt

def main():
  tmp, ftrain, ftest = sys.argv
  Cov, centroid = train(ftrain)
  test(ftest, Cov, centroid)
  return

def train(fname):
  f = open(fname, 'r')
  n, dim = [int(each) for each in f.readline().split() if each != '']
  X = []
  for i in range(n):
    X.append([float(each) for each in f.readline().split() if each != ''])
  centroid = matrix([[xi/n for xi in [sum(each) for each in zip(*X)]]])
  X = matrix(X)
  Cov = (X.T * X)/n - centroid.T * centroid
  return Cov, centroid

def test(fname, Cov, centroid):
  f = open(fname, 'r')
  n, dim = [int(each) for each in f.readline().split() if each != '']
  if dim != len(centroid.A1):
    print "Dimension doesn't match. Aborting."
    exit()
  print "Centroid:"
  print '\t'.join([str(each) for each in centroid.A1])
  print 'Covariance matrix:'
  for row in Cov.A:
    print '\t'.join([str(elem) for elem in row])
  print 'Distances:'
  invCov = Cov.I
  for i in range(n):
    x = matrix([float(each) for each in f.readline().split() if each != ''])
    mahadist = sqrt((x-centroid) * invCov * (x-centroid).T)
    print '{}. '.format(i+1) + '\t'.join([str(elem) for elem in x.A1]) + ' -- ' + str(mahadist)
  return

if __name__ == '__main__':
  main()
