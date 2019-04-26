import requests
from bs4 import BeautifulSoup as bs
import pickle	
import time	#用來記錄所花時間
import pandas as pd
import sys
sys.setrecursionlimit(10000)	
# 初始資料
domestic_url = 'https://tw.money.yahoo.com/fund/offshore'

fund_companies = []
funds_id = []
r = requests.get(domestic_url)
r.encoding = 'utf-8'
soup = bs(r.text, 'lxml')
patterns = soup.find_all('div', 'Ta-start Pstart-4')

for p in patterns:
	fund_companies.append( 'https://tw.money.yahoo.com' + p.a['href'])

count = 0
for a_url in fund_companies:
	count += 1
	r = requests.get(a_url)
	r.encoding = 'utf-8'
	soup = bs(r.text, 'lxml')
	patterns = soup.find_all('td', 'Ta-start txt-left id')
	for p in patterns:
		funds_id.append(str(p['id']))

		
first_id = 	funds_id[0]	

		
count = 1

print( first_id, '處理df，第%i/%i個基金' %(count, len(funds_id)))
price_url = 'https://tw.money.yahoo.com/fund/download/' + first_id + '?startDate=2018-03-01&endDate=2019-04-21'
df = pd.read_csv(price_url).iloc[:,0:2]
df.columns = ['date', first_id]
	

for id in funds_id[1:]:
	count+=1
	print(id, '處理df，第%i/%i個基金' %(count, len(funds_id)))
	price_url = 'https://tw.money.yahoo.com/fund/download/' + id + '?startDate=2018-03-01&endDate=2019-04-21'
	
	try:
		tem_df = pd.read_csv(price_url).iloc[:,0:2]
		tem_df.columns = ['date', id]
		df = pd.merge(df, tem_df, on=['date'], how='outer')
		print(df)
	except:
		pass
	

print(df)
df.to_csv(r'C:\Users\User\Documents\GitHub\HW1\price_foreign.csv', encoding = 'utf-8')		
