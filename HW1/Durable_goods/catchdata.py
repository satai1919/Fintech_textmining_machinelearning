from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait,Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time
import pandas as pd
import datetime
url="https://www.census.gov/econ/currentdata" #all the history data can be got from here
driver=webdriver.Chrome()
wait=WebDriverWait(driver,10)
driver.get(url)
#select manufacturers' shipments, inventories, and orders
s1=Select(driver.find_element(By.NAME,"programCode"))
s1.select_by_visible_text("Manufacturers' Shipments, Inventories, and Orders")
driver.find_element(By.XPATH,"//input[@type='submit']").click()
#1.survey and 2.range are chosen, only need to choose from 3
#select durable goods
s2=Select(driver.find_element(By.NAME,"categories"))
s2.select_by_visible_text("Durable Goods")
time.sleep(1)
#select new orders
s3=Select(driver.find_element(By.NAME,"dataType"))
s3.select_by_visible_text("New Orders")
time.sleep(1)
driver.find_element(By.XPATH,"//input[@type='submit']").click()
url=driver.current_url
value=pd.read_html(url)[0]
iniy=value.iloc[0,0]
value=value.drop(labels='Year',axis=1)
value=value.values
value=value.flatten("C")
value=pd.DataFrame(value).rename(columns={0:"Value"})

d = []
for i in range(len(value)):
    a = datetime.date(iniy+i//12, 1+i%12, 1)
    d.append(a)
d = pd.DataFrame(d).rename(columns={0:"Date"})

table = pd.DataFrame(columns=['Date'], data=d)
table["Value"] = value
print(table.dropna(axis=0,how='any').head(20))
