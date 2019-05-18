import pandas as pd
from datetime import datetime
df_rf  = pd.read_csv('rf.csv')
time_list = df_rf['y/m'].tolist()
rf_list = df_rf['rf'].tolist()

time_to_rf = dict()
for i in range(len(time_list)):
    year, month = time_list[i].split('/')
    year = int(year) + 1911
    month = int(month)
    string = str(year) +'-%02d'%month #%Y-%m
    time_to_rf[string] = rf_list[i]
    
import sqlite3
with sqlite3.connect('fund.sqlite') as db:
    df_week = pd.read_sql('select * from week', con = db)
    df_week.set_index('index', inplace = True)
    df_week = df_week.T

    df_month = pd.read_sql('select * from month', con = db) 
    df_month.set_index('index', inplace = True)
    df_month = df_month.T
	
week_date = list(df_week.index)
month_date = list(df_month.index)
rf_d = dict()
rf_d['week'] = []#rf_list
rf_d['month'] = []#rf_list

for date in week_date:
    string = (date[0:-3])
    rf = float(time_to_rf[string])
    rf_d['week'].append(rf/5200)
	
for date in month_date:
    string = (date[0:-3])
    rf = float(time_to_rf[string])
    rf_d['month'].append(rf/1200)

df_month_ready = df_month.sub(pd.Series(rf_d['month'], index=month_date),  axis='index')
df_week_ready = df_week.sub(pd.Series(rf_d['week'], index=week_date),  axis='index')