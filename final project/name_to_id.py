#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pickle import load
import os, sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)



with open(resource_path('id_name'), 'rb') as f:
    data = load(f)

def company(string):
    l = list(filter(lambda x: x!=None, list(data[""+string+""])))
    return l

#def spl(l):
#    for i in range(len(l)):
#        l[i][1] = l[i][1].rstrip()
#    return l

def fund_name(string, l):
    for i in range(len(l)):
        if string == l[i][1].rstrip():
            return l[i][0]
        
#test   
#a = company("瀚亞")
#b = fund_name('瀚亞策略印度傘型基金之印度策略收益平衡基金S類型-人民幣', a)