# Randomly select train entry
from G_features import *
import pickle
from multiprocessing import Pool
import gc
import numpy as np
import random

# Transform data into dict
global dic
def transform(data_parse):
    dics = {}
    for i in data_parse:
        dics.setdefault(int(i['id']), i)
    return dics
with open('data_parse.pkl', 'rb+') as fobj:
    data_parse = pickle.load(fobj)
with open('ip_list7.npy', 'rb+') as fobj:
    data = pickle.load(fobj)
with open("training_ground_truth.csv") as fobj:
    truth = fobj.readlines()
# Generate dict for ground truth
truths = {}
for i in truth:
    i = i.strip()
    truths.setdefault(tuple(sorted([int(i.split(',')[0]), int(i.split(',')[1])])), 1)
dic = transform(data_parse)
del data_parse
gc.collect()
y = []
for i in data:
    try:
        truths[i]
        y.append(1)
    except KeyError:
        y.append(0)
one_index = []
for i in xrange(len(y)):
    if y[i] == 1:
        one_index.append(i)
index = range(len(y))
print 'removing'
index = list(set(index) - set(one_index))
print 'sampling'
index = random.sample(index, len(one_index))
index_select = index + one_index
y = []
print 'reselecting'
y = [y[i] for i in index_select]
def f(i):
    return extract_feature(dic, i[0], i[1])

print 'generating'
p = Pool(8)
X = p.map(f, [data[i] for i in index_select])
p.close()
print 'saving'
with open('X.npy', 'wb+') as fobj:
    pickle.dump(X, fobj)
with open('y.npy', 'wb+') as fobj:
    pickle.dump(y, fobj)
with open('index.npy', 'wb+') as fobj:
    pickle.dump(index_select, fobj) 
