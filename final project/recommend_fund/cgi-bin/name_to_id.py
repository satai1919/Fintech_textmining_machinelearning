#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pickle

with open('data/id_name', 'rb') as f:
    data = pickle.load(f)

def company(string):
    l = list(filter(lambda x: x!=None, list(data[""+string+""])))
    return l

def spl(l):
    for i in range(len(l)):
        l[i][1] = l[i][1].rstrip()
    return l

def fund_name(string, l):
    for i in range(len(l)):
        if string == l[i][1]:
            return l[i][0]
        
#test   
#a = spl(company("瀚亞"))
#b = fund_name("瀚亞電通網基金", a)