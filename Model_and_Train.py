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
from sklearn.preprocessing import label_binarize
from sklearn import metrics
from sklearn import cross_validation
import matplotlib.pyplot as plt

# Preparing data
with open('X.npy', 'rb+') as fobj:
    X = pickle.load(fobj)
with open('y.npy', 'rb+') as fobj:
    y = pickle.load(fobj)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

# Accuracy
cv_error = []
models = []
for i in ['RandomForest_small', 'RandomForest_big', 'Gradientboost_small', 'Gradientboost_big', 'LogisticRegression_l1', 'LogisticRegression_l2']:
    if i == 'RandomForest_small':
        model = RandomForestClassifier()
    elif i == 'RandomForest_big':
        model = RandomForestClassifier(n_estimators = 20)
    elif i == 'Gradientboost_small':
        model = GradientBoostingClassifier()
    elif i == 'Gradientboost_big':
        model = GradientBoostingClassifier(n_estimators=200)
    elif i == 'LogisticRegression_l1':
        model = LogisticRegression(penalty='l1')
    elif i == 'LogisticRegression_l2':
        model = LogisticRegression(penalty='l2')
    model.fit(X_train, y_train)
    models.append(model)
    error.append(1 - np.mean(model.predict(X_test) == y_test))

cv_error = []
for model in models:
    cv_error.append(1 - np.mean(cross_validation.cross_val_score(model, X, y, scoring="accuracy")))

#plot error
index = np.arange(6)
fig, ax = plt.subplots()
bar_width = 0.35
opacity = 0.4
error_config = {'ecolor': '0.3'}
rects1 = plt.bar(index, error, bar_width,
                 alpha=opacity,
                 color='b',
                 error_kw=error_config,
                 label='Validation _error')

rects2 = plt.bar(index + bar_width, cv_error, bar_width,
                 alpha=opacity,
                 color='r',
                 error_kw=error_config,
                 label='Cross_validation_error')
plt.xlabel('Model')
plt.ylabel('Error')
plt.title('Validation error and cv_error of different models')
plt.xticks(index + bar_width, ('RF_10', 'RF_20', 'GB_100', 'GB_200', 'LR_l1', 'LR_l2'))
plt.legend(loc=0)
plt.savefig('error.png')

