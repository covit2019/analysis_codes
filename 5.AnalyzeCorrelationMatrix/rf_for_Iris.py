import sys
import os

import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt

from sklearn import datasets
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
#from tensorflow.keras.utils import to_categorical
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


def load_data():
  iris = datasets.load_iris()
  features = iris.data
  features = normalize_features(features)
  targets = iris.target
  targets = tf.keras.utils.to_categorical(targets)
  (x_train, x_test, y_train, y_test) = train_test_split(features, targets, test_size=0.2, random_state=0,)
  return (x_train, y_train), (x_test, y_test), iris.feature_names


def normalize_features(features):
  scaler = MinMaxScaler((0.,1.))
  scaler.fit( features )
  return scaler.transform(features)


if __name__ == '__main__':
  np.random.seed(42)
  tf.random.set_seed(42)

  (x_train, y_train), (x_test, y_test), feature_names = load_data()

  clf_rf = RandomForestClassifier()
  clf_rf.fit(x_train, y_train)
  y_pred = clf_rf.predict(x_test)
  accu = accuracy_score(y_test, y_pred)
  print('accuracy = {:>.4f}'.format(accu))

  fti = clf_rf.feature_importances_   
  print(fti)
  print('Feature Importances by random forest')
  for i, feat in enumerate(feature_names):
    print('\t{0:20s} : {1:>.6f}'.format(feat, fti[i]))
  