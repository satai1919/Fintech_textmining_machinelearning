from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait,Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time
import pandas as pd
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
table=pd.read_html(url)
print(table)
