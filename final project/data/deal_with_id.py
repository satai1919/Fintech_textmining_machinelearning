#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3

db = sqlite3.connect('fund.sqlite')
cur = db.cursor()
cur.execute("SELECT `index` FROM week;")
result = list(cur.fetchall())

non_nan = []
for funds in result:
    non_nan.append(str(funds[0]))

filename = "Fund_name_dictionary.txt"
file = open(filename,"r")

l = file.readlines()
lid = []
lna = []

for i in l:
    i = i.split(",")
    lid.append(i[0])
    lna.append(i[1].rstrip())
    
lid.pop(0)
lna.pop(0)

file.close()

k = int()
while k < len(lid):
    flag = False
    for j in range(len(non_nan)):
        if lid[k] == non_nan[j]:
            flag = True
    if flag == False:
        lid.pop(k)
        lna.pop(k)
        k -= 1
    k += 1
    print(k)
    
import pandas as pd


'''
for id to name
'''
idna = list(zip(lid, lna))
idna.sort()
idname = pd.DataFrame(idna, columns=["id","name"])
idname.to_pickle('name_id')

'''
for name to id
'''
#'''
##處理一些格式的問題
#
#name.append(["普信"])
#
#for i in range(119):
#    name[37].append([lid.pop(0),lna.pop(0)])
#
#name[65][0] = "GAM"
#'''
name1 = pd.DataFrame(name)
name = name1.transpose()
name.columns = name.iloc[0]
name = name.drop(name.index[0])

name.to_pickle('id_name') 
