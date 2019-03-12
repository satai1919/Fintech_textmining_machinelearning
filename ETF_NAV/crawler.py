import login_website
import json
import time
import pandas as pd
from bs4 import BeautifulSoup

filename = "ETF_List_Filtered.csv"
file = open(filename, "r")
#name = "output.csv"
#output = open(name, "w")
#
#
a = file.readline()
#a = a.split(",")
##print(a[-1])
#output.write(""+a[0]+", "+a[-1]+"")
##output.close()

# 34 etfs
for i in range(34):
    a = file.readline()
    #print(a)
    a = a.split(",")
    #print(type(a))
    
    # 15 pages in total
    session = login_website.login()
    df_list = []
    for j in range(1,16):
        url = "https://ycharts.com/companies/"+a[0]+"/net_asset_value.json?endDate=12/31/2018&pageNum="+str(j)+"&startDate=12/31/2015"
        reqs = session.get(url)
        rj = json.loads(reqs.text)
        to_deal = rj["data_table_html"]
        time.sleep(1)
        soup = BeautifulSoup(to_deal, 'lxml')    

        col1 = soup.find_all('td',attrs={"class": "col1"})  
        col2 = soup.find_all('td',attrs={"class": "col2"})  
        print(col1[0].text.split())	#格式是這樣 ['Dec.', '31,', '2018']	一個list
		print(col2[0].text.strip())	#格式是這樣 '123.54' 一個字串並沒有多餘的符號
		
		"""
		接下來要做的是
		for index in range(len(col1)):
			把col1[index].text.split() 裡面的第一個元素 Dec. or Oct ...etc ，及第二個元素 1,2,3,...,31 來找出當個月分最大的日期
			if 日期如果是那月份最大的:
				用個dictionary 把NAV，也就是把 col2[index].text.split() 放進那個那個 年/月 對應的NAV即可
		"""

#output.close()