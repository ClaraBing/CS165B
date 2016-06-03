#from __future__ import print_function
import sys
from random import randint
from operator import add, sub, mul
from numpy import random

def main():
    verbose = True if (len(sys.argv) == 6) else False
    T, size, ftrain, ftest = sys.argv[-4:]
    # read in data
    trainDim, trainN1, trainN2, trainData = readData(ftrain)
    testDim, testN1, testN2, testData = readData(ftest)
    if trainDim != testDim:
        print "training dim = {} / testing dim = {}".format(trainDim, testDim)
        print "Error: dimensions do not match. Aborting."
        exit(-1)
    # bagging
    samples, models = bagging(int(T), int(size), trainData, trainDim, trainN1, trainN2)
    result = maxVote(T, models, testData)
    fp = len(filter(lambda x: x==1, result[testN1:]))
    fn = len(filter(lambda x: x==-1, result[:testN1]))
    # output
    print "Positive examples: {}".format(testN1)
    print "Negative examples: {}".format(testN2)
    print "False positives: {}".format(fp)
    print "False negatives: {}".format(fn)
    if verbose:
        print
        # the composition of the T bootstrap sample sets
        for i,(pos,neg) in enumerate(samples):
            print 'Bootstrap sample set {}:'.format(i)
            for each in pos:
                print ' '.join(map(str, each)) + ' - True'
            for each in neg:
                print ' '.join(map(str, each)) + ' - False'
            print
        # the classification results
        print "\nClassification:"
        for i in range(testN1):
            print ' '.join(map(str, testData[i])) + (' - True (correct)' if result[i]>0 else ' - False (incorrect)')
        for i in range(testN1, testN1+testN2):
            print ' '.join(map(str, testData[i])) + (' - True (incorrect)' if result[i]>0 else ' - False (correct)')
    return

def bagging(T, size, data, dim, n1, n2):
#    bags = [[randint(0, n1+n2-1) for _ in range(size)] for _ in range(T)]
    random.seed(0xE3A8)
    bags = random.randint(0,high=n1+n2, size=(T,size)).tolist()
    print "bags:" + str(bags)
    models = []
    samples = []
    for bag in bags:
        posSample = [data[i] for i in bag if i<n1]
        negSample = [data[i] for i in bag if i>=n1]
        models.append(train(posSample, negSample))
        samples.append((posSample, negSample))
    return samples, models

def maxVote(T, models, data):
    # get the classification results from each model and take the max vote
    return [1 if sum([classify(each, m) for m in models]) >= 0 else -1 for each in data]

def train(posSample, negSample):
    # if there's no positive data in the sample, everything is classified as negative
    if not posSample:
        return (-1, 0)
    # if there's no negative data in the sample, everything is classified as positive
    if not negSample:
        return (1, 0)
    n1, n2 = float(len(posSample)), float(len(negSample))
    # the centroid of the positive class
    pos = map(lambda x: x/n1, reduce(lambda x, y: map(add, x, y), posSample))
    # the centroid of the negative class
    neg = map(lambda x: x/n2, reduce(lambda x, y: map(add, x, y), negSample))
    # the midpoint of the two centroid
    mid = map(lambda x, y: (x+y)/2.0, pos, neg)
    # the normal vector pointing from the negative centroid to the positive centroid
    nv = map(sub, pos, neg)
    return (mid, nv)

def classify(pos, model):
    mid, nv = model
    # if one of the classes is empty, classify as the other class
    if nv == 0:
        return mid
    val = sum(map(mul, map(sub, pos, mid), nv))
    return 1 if val > 0 else -1

# utility function
def readData(fname):
    f = open(fname, 'r')
    dim, n1, n2 = [int(each) for each in f.readline().split(' ') if each]
#    data = []
    data = [[float(each) for each in f.readline().split(' ') if each] for i in range(n1+n2)]
#     for _ in range(n1+n2):
#         line = [each for each in f.readline().split(' ') if each]
#         print "line: " + str(line)
#         try:
#             data.append([float(each) for each in line if each])
#         except ValueError as e:
#             print "ValueError: " + str(line)
#             raise
    return dim, n1, n2, data

if __name__ == '__main__':
    main()
