#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd

filename = 'funds_info.csv'
file = pd.read_csv(filename)

t = file["投資策略"]

trainfilename = 'train_data'
trainfile = open(trainfilename, 'w')

for i in range(1500):
    a = str(t[i])
    for words in t[i]:
        trainfile.write(words + "\t" + "O" + "\n")
    trainfile.write("\n")
trainfile.close()

testfilename = 'test_data'
testfile = open(testfilename, 'w')
        
for i in range(1500,2091):
    a = str(t[i])
    for words in t[i]:
        testfile.write(words + "\t" + "O" + "\n")
    testfile.write("\n")
testfile.close()