如何在自己的電腦中測試：
1. 將整個recommend_fund資料夾載下來
2. 打開terminal/cmd，打開檔案夾至recommend_fund
3. 執行 chmod +x cgi-bin/final.py
4. 執行 python3 -m http.server --cgi 8000
5. 打開Chrome，在網址列輸入 localhost:8000/cgi-bin/final.py