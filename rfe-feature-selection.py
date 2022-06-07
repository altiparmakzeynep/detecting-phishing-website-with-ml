#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 22:03:04 2022

@author: zeynep
"""

import pandas as pd
import numpy as np
from sklearn.feature_selection import RFE
#from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVR

final_dataset = pd.read_csv("deneme500.csv")

X = final_dataset.iloc[:,0:17]  #independent columns
Y = final_dataset.iloc[:,-1]    #target column i.e price range

#model = LogisticRegression()
#rfe = RFE(model, 5)
#fit = rfe.fit(X, Y)

#print("Num Features: %s" % (fit.n_features_))
#print("Selected Features: %s" % (fit.support_))
#print("Feature Ranking: %s" % (fit.ranking_))


estimator = SVR(kernel="linear")
selector = RFE(estimator, n_features_to_select=3, step=1)
selector = selector.fit(X, Y)

print(selector.support_)
print(selector.ranking_)
print(selector._get_param_names)
print(final_dataset.iloc[:,2].name)
print(final_dataset.iloc[:,6].name)
print(final_dataset.iloc[:,8].name)
print(final_dataset.iloc[:,9].name)
print(final_dataset.iloc[:,16].name)