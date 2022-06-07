#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  1 12:26:14 2022

@author: zeynep
"""
import pandas as pd

benign_dataset = pd.read_csv("p500.csv")
phishing_dataset = pd.read_csv("b500.csv")

urldata = pd.concat([benign_dataset, phishing_dataset]).reset_index(drop=True)
urldata.head()
urldata.tail()

urldata.to_csv('final500.csv', index=False)