#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pickle

with open('data/name_id', 'rb') as f:
    data = pickle.load(f)

def binarySearch(arr, l, r, x): 
    while l <= r: 
        mid = l + (r - l)//2; 
        if arr[mid] == x: 
            return mid  
        elif arr[mid] < x: 
            l = mid + 1
        else: 
            r = mid - 1
    return -1

#test1
#x = 10
#arr = [1,2,3,4,10]
#a = binarySearch(arr,0,len(arr)-1,x)
    
def search(string):
    loc = binarySearch(data["id"],0,len(data["id"])-1, string)
    return data["name"][loc]