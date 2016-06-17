import pickle
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import linear_model
from sklearn.svm import SVR
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.manifold import TSNE
import random
# Preparing data
with open('X.npy', 'rb+') as fobj:
    X = pickle.load(fobj)
with open('y.npy', 'rb+') as fobj:
    y = pickle.load(fobj)

X_select = random.sample(X[:101172], 500) + random.sample(X[101172:], 500)
X_select.__len__()
t = TSNE()
X_TSNE = t.fit_transform(X_select)