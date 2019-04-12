
import asyncio
import requests
from bs4 import BeautifulSoup as bs
import pickle	
import time	#用來記錄所花時間
import multiprocessing as mp	#用來多進程
import pandas as pd
import sys
sys.setrecursionlimit(10000)
#define functions

def crawl(url):

	r =  requests.get(url)
	r.encoding = 'utf-8'
	html = r.text

	return html

def parse(html):
	soup  = bs(html, 'lxml')
	name = soup.select_one('h1').string
	df = pd.read_html(html)[1]
	col_1 = df.iloc[:,1]
	col_3 = df.iloc[:,3]
	a_dict = ({
	'基金id' : id,
	'基金名稱' : name, 
	'計價幣別': col_1[1],
	'基金公司/總代理人' : col_3[0],
	'成立時間' :  col_3[2],
	'基金規模' :  col_1[2],
	'投資策略' : col_1[4]
	})

	return a_dict #返回dictionary 作為 pool.get()方法的抓取值



async def main(loop,all_data):
	htmls = []
	pool = mp.Pool(4)

	print('crawling')
	count = 0
	for url in url_list:

		count +=1	
		print('crawling', count)
		htmls.append(crawl(url))
	
	
	# 多進程輸出dictionary
	print('Parsing')
	parse_tasks = [pool.apply_async(parse, args=(html, )) for html in htmls] 
	data1 = [j.get() for j in parse_tasks]
	# 存取資料
	all_data += data1
	print('Finish')

		
## 初始資料
domestic_url = 'https://tw.money.yahoo.com/fund/domestic'

fund_companies = []
funds = []
r = requests.get(domestic_url)
r.encoding = 'utf-8'
soup = bs(r.text, 'lxml')
patterns = soup.find_all('div', 'Ta-start Pstart-4')

for p in patterns:
	fund_companies.append( 'https://tw.money.yahoo.com' + p.a['href'])

for a_url in fund_companies:
	r = requests.get(a_url)
	r.encoding = 'utf-8'
	soup = bs(r.text, 'lxml')
	patterns = soup.find_all('td', 'Ta-start txt-left id')
	for p in patterns:
		funds.append(p['id'])

url_list = []
for id in funds:

	url = 'https://tw.money.yahoo.com/fund/summary/' + id
	url_list.append(url)		
## 初始資料		
		
		
		
		
		
		
		
		
		
		
if __name__ == "__main__":
	all_data = []
	t1 = time.time()
	loop = asyncio.get_event_loop()
	loop.run_until_complete(main(loop,all_data))
	loop.close()
	
		print('Total time consumed is %s seconds' %( time.time()-t1 )	)	


	
	#pandas
		
	table = pd.DataFrame(all_data)[['基金id', '基金名稱', '計價幣別', '基金公司/總代理人', '成立時間', '基金規模', '投資策略']]
	table.to_csv(r'C:\Users\User\pf\funds_info1.csv', encoding = 'utf-8-sig' )