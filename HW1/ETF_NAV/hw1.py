
######## selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

def get_home_page(symbol):
    url = "https://www.etf.com/" + symbol
    r = requests.get(url)
    r.encoding = 'utf-8'
    soup = bs(r.text, 'lxml')	#'lxml'解析器	優點速度快
    pattern = soup.find('div',attrs={"class": "field-content helplink"}) #首頁鏈結放在該標籤之下
    url2 = pattern.a['href']
    return url2
	
	
import csv
path = 'ETF List Filtered.csv'
in_file =  open( path , 'r')
csv_reader = csv.DictReader(in_file)



## 確保資料夾位置
location = r'C:\Users\User\Desktop\新增資料夾\fund'

import pandas as pd
import time
for a_row in csv_reader:
    symbol = a_row['Symbol']
    etf_name = a_row['ETF Name']
    company_name = etf_name.split()[0]
    if company_name == 'Invesco':  #如果基金公司是Invesco，那下載鏈結為id = downloadNavHistory
        url = get_home_page(symbol)
        driver.get(url)
        driver.find_element_by_id("downloadNavHistory").click()
    elif company_name == 'Market': ##如果基金公司是Market Vectors，可直接用網址加代號取得檔案
        driver.get('https://www.marketvectorsetns.com/HistoPriceExport.aspx?ticker=' + symbol)
        
    elif company_name == 'ProShares': ##如果基金公司是ProShares，可直接用網址加代號取得CSV檔案  
        url = 'https://accounts.profunds.com/etfdata/ByFund/' + symbol +'-historical_nav.csv'
        df = pd.read_csv(url)
        df.to_csv( location + '\%s.csv' %symbol)
        
    elif company_name == 'WisdomTree': ##如果基金公司是WisdomTree，得先進去一個網址後用beautifulsoup以及pandas來處理網站表格
        homepage = 'https://www.wisdomtree.com/etfs/currency/'+ symbol.lower()
        r = requests.get(homepage)
        r.encoding = 'utf-8'
        soup = bs(r.text, 'lxml')
        pattern = soup.find('ul',attrs={"class": "footer-links"}) 
        table_html = pattern.a['data-href']

        r = requests.get(table_html)
        html_df = pd.read_html(r.text)
        html_df[0].to_csv( location + '\%s.csv' %symbol)
    elif company_name == 'SPDR': ##如果基金公司是SPDR，得先進去一個網址後用beautifulsoup以及pandas來處理網站表格
        driver.get('https://us.spdrs.com/site-content/xls/PSK_HistoricalNav.xls?fund=' + symbol)
        
    else:#其他基金公司 必須從yahoo來爬取
        url = 'https://finance.yahoo.com/quote/' + symbol + "/history?period1=1448899200&period2=1557469791&interval=1d&filter=history&frequency=1d"
        driver.get(url)
        time.sleep(2)
        wait.until(EC.presence_of_element_located((By.XPATH, "(.//*[normalize-space(text()) and normalize-space(.)='Currency in USD'])[1]/following::span[2]")))
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Currency in USD'])[1]/following::span[2]").click()
    print('Symbol %s is done.' %symbol)
	
	
	
#找到資料夾
import os
import glob

path = location	#the path where you put your downloaded files
extension1 = 'csv'
extension2 = 'xls'
os.chdir(path)
csv_list = [i for i in glob.glob('*.{}'.format(extension1))]
excel_list = [i for i in glob.glob('*.{}'.format(extension2))]

##開始處理
from datetime import datetime
df_list = []
start_of_2016 =  datetime.strptime( '1/1/2016', "%m/%d/%Y")	
		
for file in excel_list:
	try:
		df = pd.read_html(path + '\\' +file, skiprows=2)[0].iloc[:, 0:2]
		
	except:
		df = pd.read_excel(path + '\\' +file, skiprows=3).iloc[:-12, 0:2]	#該檔案最後幾行是文字，而非我們需要的
			
	#使用dictionary來處理資料
	tem_dict = {}
	dict = df.to_dict('split')
	list_of_date_and_nav = dict['data']		

	#開始轉成dictionary，需要調整時間格式!!
	#還需要確保此時間不會早於2015年底的最後一個交易日
	max_date_prior_to_2016 = datetime.strptime( '12/1/2015', "%m/%d/%Y")	#時間的default value，為了找出2015年的最後一個交易日為何時。
	for date, nav in list_of_date_and_nav:
		try:
			datetime = datetime.strptime( date, "%d-%b-%Y")
		except:
			datetime = datetime.strptime( date, "%m/%d/%Y")	
	
		if datetime >= start_of_2016:
			tem_dict[datetime] = nav
		elif start_of_2016 > datetime > max_date_prior_to_2016:	#更新2015年的最後一個交易日
			if max_date_prior_to_2016 in tem_dict:
				tem_dict.pop(max_date_prior_to_2016)
			tem_dict[datetime] = nav
			max_date_prior_to_2016 = datetime
		
	#找出symbol 來當作 column name，並轉成dataframe
	symbol =  file.split('_')[0]
	df = pd.DataFrame.from_dict(tem_dict, orient='index',  columns=[symbol])
	
	print(df.head(1))
	print(df.tail(1))
	#append 到list 以便之後合併
	df_list.append(df)



for file in csv_list:
	#找出datafram，並留下Date及NAV
	df = pd.read_csv(path + '\\' +file)
	col_name = list(df.columns.values)
	if 'NAV' not in col_name:
		if 'Nav' in col_name:
			df = df.loc[:, ['Date', 'Nav']]
		else:
			df = df.loc[:, ['Date', 'Adj Close']]	
	else:
		df = df.loc[:, ['Date', 'NAV']]
	
	#使用dictionary來處理資料
	tem_dict = {}
	dict = df.to_dict('split')
	list_of_date_and_nav = dict['data']
	
	#開始轉成dictionary，需要調整時間格式!!
	#還需要確保此時間不會早於2015年底的最後一個交易日
	max_date_prior_to_2016 = datetime.strptime( '12/1/2015', "%m/%d/%Y")	#時間的default value，為了找出2015年的最後一個交易日為何時。
	for date, nav in list_of_date_and_nav:
		try:
			datetime = datetime.strptime( date, "%m/%d/%Y")
		except:
			datetime = datetime.strptime( date, "%Y-%m-%d")
			
		if datetime >= start_of_2016:
			tem_dict[datetime] = nav
		elif datetime > max_date_prior_to_2016:	#更新2015年的最後一個交易日
			if max_date_prior_to_2016 in tem_dict:
				tem_dict.pop(max_date_prior_to_2016)
			tem_dict[datetime] = nav
			max_date_prior_to_2016 = datetime
			
	#找出symbol 來當作 column name，並轉成dataframe
	if file.split('_')[0] == 'historical':
		symbol =  file.split('_')[2]
	else:
		symbol =  file.split('.')[0]
	df = pd.DataFrame.from_dict(tem_dict, orient='index',  columns=[symbol])
	
	print(df.head(1))
	print(df.tail(1))
	#append 到list 以便之後合併
	df_list.append(df)




res = pd.concat( df_list , axis=1)
print( res )

res.to_csv('output2.csv')

