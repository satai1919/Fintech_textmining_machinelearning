import login_website
import json
import time
import pandas as pd
import re
import csv
from bs4 import BeautifulSoup

filename = "ETF_List_Filtered.csv"
#filename = "..\data\ETF_List_Filtered.csv"
file = open(filename, "r")
name = "output.csv"
output = open(name, "w+", newline='')
writer=csv.writer(output)
time_list=['']
for i in range(2018,2015,-1):
    for j in range(12,0,-1):
        time_list.append(str(i)+'/'+str(j))
print(time_list)
writer.writerow(time_list)
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
    nav_dict=dict()
    for j in range(1,16):
        url = "https://ycharts.com/companies/"+a[0]+"/net_asset_value.json?endDate=12/31/2018&pageNum="+str(j)+"&startDate=12/31/2015"
        reqs = session.get(url)
        rj = json.loads(reqs.text)
        to_deal = rj["data_table_html"]
        time.sleep(1)
        soup = BeautifulSoup(to_deal, 'lxml')

        col1 = soup.find_all('td',attrs={"class": "col1"})
        col2 = soup.find_all('td',attrs={"class": "col2"})
        #print(col1[0].text.split())    #格式是這樣 ['Dec.', '31,', '2018']    一個list
        #print(col2[0].text.strip())    #格式是這樣 '123.54' 一個字串並沒有多餘的符號

        date = [ col1[index].text.split() for index in range(len(col1)) ]
        nav = [ col2[index].text.strip() for index in range(len(col2)) ]

        #dict('2018 Dec.')=[31,123.54]

        for index in range(len(col1)):
            month=date[index][2]+" "+date[index][0]
            day=int(re.sub(',', ' ', date[index][1]))
            if nav_dict.get(month)==None:
                nav_dict[month]=[day,nav[index]]
            elif day>nav_dict[month][0]:
                nav_dict[month]=[day,nav[index]]

    print(list(nav_dict.items()))
    nav_list=[a[0]]
    for item in list(nav_dict.items()):
        nav_list.append(item[1])
    writer.writerow(nav_list)

#output.close()
