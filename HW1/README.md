# 作業一

## 爬蟲所使用的套件:
* Selenium -- 因為有些基金首頁中NAV的鏈接沒有直接取得的辦法，只能透過該套件利用點取方法來下載NAV
* Requests加上BeautifulSoup -- 有些基金首頁有可以不透過 Selenium 即可取得鏈結的方法的話，那就透過BeautifulSoup來找出鏈接網址

## 可能遇到的錯誤:
* 沒有安裝套件包 => 需要確保每個套件都已安裝
* 系統找不到Selenium的WebDreiver => 需要下載的WebDreiver，且應該放置在Python資料夾所在位置並設置環境變數
* Selenium 的WebDreiver 有放置還是出錯 => 檢查WebDreiver版本是否與對應的瀏覽器版本相符
* 打印出所有下載的NAV檔案時出錯 => Selenium每次打開webDriver的下載資料夾路徑會重設為預設，需要手動更改
* 在excel_list或者csv_list的處理出錯 => 確保下載的資料夾只有剛剛下載的檔案，不能有其他不相關的excel或csv檔案。



