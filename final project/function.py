import sqlite3
import pandas as pd
from scipy.stats.stats import pearsonr
from datetime import datetime
import numpy as np

def downside_corr(a,b):
    i = a[1:]<a[:-1]
    corrab, _ = pearsonr(a[1:][i], b[1:][i])
    j = b[1:]<b[:-1]
    corrba, _ = pearsonr(a[1:][j], b[1:][j])
    return (corrab+corrba)/2

def recommend_funds(fund):
    cor_list = []
    id_list = []
    mean_list = []
    db = sqlite3.connect('data/fund.sqlite')
    cur = db.cursor()
    cur.execute('select * from week')
    r = cur.fetchall()
    for i in range(len(r)):
        id_list.append(r[i][0])

    # get rf
    df_rf  = pd.read_csv('data/rf.csv')
    time_list = df_rf['y/m'].tolist()
    rf_list = [float(x)/5200 for x in df_rf['rf'].tolist()]

    time_to_rf = dict()
    for i in range(len(time_list)):
        year, month = time_list[i].split('/')
        year = int(year) + 1911
        month = int(month)
        string = str(year) +'-%02d'%month #%Y-%m
        time_to_rf[string] = rf_list[i]
        
    cur.execute('PRAGMA  table_info([week])')
    rf_array = []
    r = cur.fetchall()
    for i in range(1, len(r)):
        date = r[i][1][:-3]
        rf_array.append( time_to_rf[date]  )
    rf_array = np.array(rf_array)
    fund_list = []
    mean_list = []
    cor1_list = []
    cor2_list = []
    
    cur.execute('select * from week')
    r = cur.fetchall()
    p = id_list.index(fund)
    x = np.array(r[p][1:], dtype= 'float64').reshape(1,-1)
    for i in range(len(r)):
        if i==p:
            continue
        fund_list.append(r[i][0])
        y = np.array(r[i][1:], dtype= 'float64').reshape(1,-1)
        z = np.concatenate((x,y), axis=0).T
        rf_new = rf_array[~np.isnan(z).any(axis=1)]
        z_new = z[~np.isnan(z).any(axis=1)].T
        x_new = z_new[0] - rf_new
        y_new = z_new[1] - rf_new
        y = y.reshape(-1,)
        y = y[~np.isnan(y)]
        mean_list.append(y.mean()*4)
        cor1,_ = pearsonr(x_new, y_new)
        cor1_list.append(cor1)
        cor2 = downside_corr(x_new, y_new)
        cor2_list.append(cor2)

    #一般相關性:
    cor1_list = np.array(cor1_list)
    indices = cor1_list.argsort()[:6]
    output1 = []
    for i in indices[0:3]: 
        output1.append( (mean_list[i], 'A+', id_list[i]) )
    for i in indices[3:]: 
        output1.append( (mean_list[i], 'A', id_list[i]) )

    output1.sort(reverse = True)
    '''
    print('{0:<3s} {1:<12s} {2:<5s} {3:<6s}'.format('排名','基金ID','平均獲利','分散風險程度'))
    for rank, (mean, degree, fund_id) in enumerate(output):
        print('{0:<5d} {1:<14s} {2:<.6f} {3:<6s}'.format(rank+1,fund_id,mean,degree))
    '''
        
    #下跌相關性
    cor2_list = np.array(cor2_list)
    indices = cor2_list.argsort()[:6]
    output2 = []
    for i in indices[0:3]: 
        output2.append( (mean_list[i], 'A+', id_list[i]) )
    for i in indices[3:]: 
        output2.append( (mean_list[i], 'A', id_list[i]) )

    output2.sort(reverse = True)
    '''
    print('{0:<3s} {1:<12s} {2:<5s} {3:<6s}'.format('排名','基金ID','平均獲利','分散風險程度'))
    for rank, (mean, degree, fund_id) in enumerate(output):
        print('{0:<5d} {1:<14s} {2:<.6f} {3:<6s}'.format(rank+1,fund_id,mean,degree))
    '''
    return output1,output2