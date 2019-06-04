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

def recommend_funds(picked_fund, picked_num):
    db = sqlite3.connect('data/fund.sqlite')
    cur = db.cursor()
    
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
    
    cur.execute('select * from week')
    r = cur.fetchall()

    id_list = []
    for i in range(len(r)):
        id_list.append(r[i][0])

    picked_id = []
    for fund_name in picked_fund:
        picked_id.append(id_list.index(fund_name))
    
    picked_array = []
    for p in picked_id:
        picked_array.append(np.array(r[p][1:], dtype='float64'))
    x = np.array(picked_array)
    total_weight = sum(picked_num)
    weight = np.array(picked_num).reshape(-1,1)

    fund_list = []
    mean_list = []
    cor1_list = []
    cor2_list = []
    for i in range(len(r)):
        if i in picked_id:
            continue
        fund_list.append(r[i][0])
        y = np.array(r[i][1:], dtype= 'float64').reshape(1,-1)
        z = np.concatenate((x,y), axis=0).T
        rf_new = rf_array[~np.isnan(z).any(axis=1)]
        z_new = z[~np.isnan(z).any(axis=1)].T
        x_new = z_new[:-1]*weight
        x_new = x_new.sum(axis=0)/total_weight - rf_new
        y_new = z_new[-1] - rf_new
        y = y.reshape(-1,)
        y = y[~np.isnan(y)]
        mean_list.append(y.mean()*4)
        cor1,_ = pearsonr(x_new, y_new)
        cor1_list.append(cor1)
        cor2 = downside_corr(x_new, y_new)
        cor2_list.append(cor2)
        
    #一般相關性
    cor1_list = np.array(cor1_list)
    indices = cor1_list.argsort()[:10]
    info_list = []
    for i in indices: 
        info_list.append( (cor1_list[i], mean_list[i], id_list[i]) )

    info_list.sort()
    output1 = []
    max_value = -1
    for info in info_list:
        if info[1] > max_value:
            max_value = info[1]
            output1.append( (info[2], info[1]) )

    #下跌相關性
    cor2_list = np.array(cor2_list)
    indices = cor2_list.argsort()[:10]
    info_list = []
    for i in indices: 
        info_list.append( (cor2_list[i], mean_list[i], id_list[i]) )

    info_list.sort()
    output2 = []
    max_value = -1
    for info in info_list:
        if info[1] > max_value:
            max_value = info[1]
            output2.append( (info[2], info[1]) )
    
    return output1, output2