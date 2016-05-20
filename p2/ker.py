import sys
from numpy import matrix
from numpy import linalg
from math import sqrt,exp

DEBUG = True

def main():
  tmp, sigma, fpos, fneg, tpos, tneg = sys.argv
  n, a, data, y = train(float(sigma), fpos, fneg)
  test(n, a, data, y, tpos, tneg, float(sigma))
  return

def train(sigma, fpos, fneg):
  # get input data
  fpos, fneg = open(fpos, 'r'), open(fneg, 'r')
  pn, pdim = [int(each) for each in fpos.readline().split() if each != '']
  # append 1: homogeneous coordinates
  pdata = [[float(each) for each in fpos.readline().split() if each != ''] + [1] for i in range(pn)]
  nn, ndim = [int(each) for each in fneg.readline().split() if each != '']
  if pdim != ndim:
    print "pos/neg dimensions don't match. Aborting."
    exit(-1)
  # append 1: homogeneous coordinates
  ndata = [[float(each) for each in fneg.readline().split() if each != ''] + [1] for i in range(nn)]
  n = pn + nn
  data = pdata + ndata
  # compute the Gram matrix using RBF
  gram = [[rbf(matrix(data[i]), matrix(data[j]), sigma) for j in range(n)] for i in range(n)]
  # print for debugging
  for row in gram:
    if DEBUG: print row
  a = [0 for _ in range(n)]
  y = [1 for _ in range(pn)] + [-1 for _ in range(nn)]
  converged = False
  while not converged:
    converged = True
    for i in range(n):
      if y[i] * sum([a[j]*y[j]*gram[i][j] for j in range(n)]) <= 0:
        a[i] += 1
	converged = False
  print 'Alphas: ' + ' '.join([str(ai) for ai in a])
  return n, a, data, y
#  w = sum([a[i]*y[i]*matrix(data[i]) for i in range(n)])
#  return w

# the kernel function: radial basis function (Gaussian)
def rbf(x1, x2, sigma):
  return exp(int((x1-x2) * (x1-x2).T) / (-2.0 * sigma**2))

def test(n, a, data, y, tpos, tneg, sigma):
  tpos, tneg = open(tpos, 'r'), open(tneg, 'r')
  pn, pdim = [int(each) for each in tpos.readline().split() if each != '']
  if pdim+1 != len(data[0]):
    print "Dimension doesn't match. Aborting."
    exit(-1)
  # append 1: homogeneous coordinates
  pdata = [[float(each) for each in tpos.readline().split() if each != ''] + [1] for i in range(pn)]
  # number of False Negatives
  fn = sum([1 if sum([a[i]*y[i]*rbf(matrix(data[i]), x, sigma) for i in range(n)])<=0 else 0 for x in pdata])
  nn, ndim = [int(each) for each in tneg.readline().split() if each != '']
  if ndim != pdim:
    print "Dimension doesn't match. Aborting."
    exit(-1)
  # append 1: homogeneous coordinates
  ndata = [[float(each) for each in tneg.readline().split() if each != ''] + [1] for i in range(nn)]
  # number of False Positives
  fp = sum([1 if sum([a[i]*y[i]*rbf(matrix(data[i]), x, sigma) for i in range(n)])>=0 else 0 for x in ndata])
  print 'False positives: {}'.format(fp)
  print 'False negatives: {}'.format(fn)
  print 'Error rate: {}%'.format((fp+fn)*100 / (pn + nn))
  return

if __name__ == '__main__':
  main()
