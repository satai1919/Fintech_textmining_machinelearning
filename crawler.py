import login_website
import json
import time
import pandas as pd
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
        df_list.append(pd.read_html(to_deal, header = 0)[0])
        #print(type(to_deal))
    

#output.close()