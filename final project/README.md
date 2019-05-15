# 金融科技——文字探勘與機器學習

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


