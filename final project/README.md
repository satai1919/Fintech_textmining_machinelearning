# 基金相關性資料庫

資料庫邏輯:   
1. 存報酬率的兩個檔案:weekly return and monthly return  


2. 第三個檔案: 每個id存4個數字  

組成共4 X 6193 的矩陣    

columns 為 fund id   
row 0 為 日期   
row 1 為 上月的最後一個有效NAV (不是np.nan)    
row 2 為 上周的最後一個有效NAV (不是np.nan)    
row 3 為 最後一個有效NAV (不是np.nan)    


每日爬取，爬到最後一個日期時間 ，替換 row3   
換周或換月份時，替換row1, row2, 並且計算報酬率，append到資料庫中   


##新增檔案
讀取資料庫的利率後，把無風險利率減去的檔案 substract_rf.py


##目前已完成資料庫爬取及更新 (建議換周或換月份再跟新)


## 代辦事項

* 使用介面
* 介面內根據使用者勾選基金名稱後計算三種 correlation

