import pandas as pd 
import sqlite3, math
from datetime import datetime, timedelta
import numpy as np


# functions
def stock_return(price_now, price_past):
    try:
        ret =  (price_now-price_past) / price_past
    except:
        ret = np.nan
    return ret
        
def get_weekly_return(a_df, last_week, last_price):
    date_list = a_df['date'].tolist()
    price_list =a_df['nav'].tolist()
    
    index_list = []
    return_list = []
    today = -1
    yesterday = -1
    
    last_week_last_price = last_week
    
    tem_price_holer = [last_price]# 紀錄這周所有價格，為了判斷是否都是nan
    
    for date, price in zip(date_list, price_list):
        today = date.weekday()
        
        if today < yesterday: #由於monday 是0, sumday 是6 如果today的weekday比較小，代表換周了
            
            if len(tem_price_holer) != 0:
                this_week_last_price = tem_price_holer[-1]
                week_ret = stock_return(this_week_last_price, last_week_last_price)
                #append
                return_list.append(week_ret)
                index_list.append(date.date())
                #update
                last_week_last_price = this_week_last_price
            else:
                return_list.append(np.nan)
                index_list.append(date.date())
                last_week_last_price = np.nan
                
            tem_price_holer = [] #更新
            
        if not math.isnan(price): #price 不是nan
            tem_price_holer.append(price)
        
        yesterday = today
        
    if len(tem_price_holer) >0:
        this_week_last_price = tem_price_holer[-1]
    else:
        this_week_last_price= np.nan
    
    return return_list, index_list, last_week_last_price, this_week_last_price
    
    
    

    



# 用來表示是否有隔週
is_new_week = False





#取出price_holder sql file
with sqlite3.connect('fund.sqlite') as db:
    df_price_holder = pd.read_sql('select * from price_holder', con = db)
    df_price_holder.set_index('index', inplace = True)

    #取出資料庫上次日期即今日日期
    column_name =  df_price_holder.columns
    start = column_name[1] #'2019-05-09'格式
    start_datetime = datetime.strptime(start, '%Y-%m-%d').date()
    end_datetime = (datetime.now() + timedelta(days = -1)).date()
    end = end_datetime.strftime('%Y-%m-%d') #爬到昨天為止
    
    if end_datetime - start_datetime >= timedelta(days = 7) or end_datetime.weekday() < start_datetime.weekday():#如果隔週
        is_new_week = True

    
    if is_new_week:
        df_week = pd.read_sql('select * from week', con = db)
        df_week.set_index('index', inplace = True)
        df_week = df_week.T

    
    
#取出資料庫 fund id、last price
id_list = list(df_price_holder.index)
last_week_list = df_price_holder[u'上週價格'].tolist()
last_price_list = df_price_holder[start].tolist()

lenth = len(last_price_list)

#爬取到最新的NAV資料
count = 0


data_week = {}
index_list = []
for i in range(lenth):
    error = False
    id = id_list[i]
    last_week = last_week_list[i]
    
    last_price = last_price_list[i]
    count+=1        
    
    #爬取find nav    
    print(id, '處理df，第%i/%i個基金' %(count, len(id_list)))
    price_url = 'https://tw.money.yahoo.com/fund/download/' + id + '?startDate=' + start + '&endDate=' + end
    
    # to dataframe
    try:
        tem_df = pd.read_csv(price_url).iloc[:,0:2]
        tem_df.columns = ['date', 'nav']
        tem_df['date']= pd.to_datetime(tem_df['date']) 
    except:
        error = True
        
    if error or tem_df.shape[0] < 1:


        if is_new_week:
            last_week_list[i] =  last_week
        
        last_price_list[i] = last_price
        continue

    

    
    #就算不是隔週也要update this_week_last_price
    week_ret_list, week_index_list, last_week_last_price, this_week_last_price = get_weekly_return(tem_df, last_week,last_price)
    if is_new_week:
        
        data_week[id] = week_ret_list
        last_week_list[i] = last_week_last_price
        if len(week_index_list) == len(index_list) and week_index_list!=index_list : #確保是星期一
            for i in range(len(week_index_list)):
                if week_index_list[i]< index_list[i]:
                    index_list[i] = week_index_list[i]
        elif len(week_index_list) > len(index_list):
            index_list = week_index_list
    last_price_list[i] = this_week_last_price
    
# update the price_holder dataframe
if is_new_week:
    df_price_holder[u'上週價格'] = np.array(last_week_list)
    for key, value in zip( list(data_week.keys()), list(data_week.values()) ) :
        if len(value) == 0:
            del data_week[key]
    to_appended_df = pd.DataFrame(data = data_week, index = index_list)
    df_week = df_week.append(to_appended_df)


#update last price column
df_price_holder[start] = np.array(last_price_list)
column_name = list(column_name)
column_name[1] = end
df_price_holder.columns = column_name

# save to sql
with sqlite3.connect('fund.sqlite') as db:
    df_price_holder.to_sql('price_holder', con = db, if_exists='replace')
    if is_new_week:
        df_week.T.to_sql('week', con = db, if_exists='replace')
