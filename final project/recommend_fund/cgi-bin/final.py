#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import print_function
import cgi, cgitb, sys, os, name_to_id, id_to_name, function
import numpy as np
import pickle

with open("data/id_name", "rb") as f:
    data = pickle.load(f)
cols = list(data.columns)

form = cgi.FieldStorage() 
print("Content-type:text/html\r\n\r\n")
print('<html>')
print('<head>')
print('<meta HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=utf-8">')
print('<title>基金推薦</title>')
print('</head>')
print('<body>')
print('<h2 align=center>基金推薦資料庫</h2>')
print('<p align=center>您輸入現有投資組合，我們幫您推薦一支基金，讓您的獲利更加穩定。</p>')
print('<hr>')

print('<script>')
print('department=new Array();')
for i in range(len(cols)):
    l = []
    for j in range(len(name_to_id.company(cols[i]))):
        l.append(name_to_id.spl(name_to_id.company(cols[i]))[j][1])
    string = '["' + '","'.join(l) + '"]'
    print('department['""+str(i)+""']='""+string+""';')
print('function renew(index){')
print('	for(var i=0;i<department[index].length;i++)')
print('		document.myForm.member.options[i]=new Option(department[index][i], department[index][i]);	// 設定新選項')
print('	document.myForm.member.length=department[index].length;	// 刪除多餘的選項')
print('}')
print('</script>')

print('<form method="post" name="myForm">')

print('<h3>1. 請在以下欄位選擇您已購買的基金</h3>')
print('基金公司名稱：')
print('<select name="com" onChange="renew(this.selectedIndex);">')
for i in range(len(cols)):
    print('<option value="%s">%s</option>' %(cols[i], cols[i]))
print('</select>')
print('基金名稱：')
print('<select name="member">')
print('	<option value="">請先選取基金公司名稱')
print('</select>')
print('<input type="submit" value="選擇"/><br>')
print('</form>')
fund = form.getvalue("member")
com = form.getvalue("com")

print('<form method="post">')
print('<h3>2. 您目前的選擇是：')
print('<input type="text" name="selected_com" value="%s" readonly size="10">' %com)
print('<input type="text" name="selected" value="%s" readonly size="60">' %fund)
print('已投資於此基金的金額<input type="text" name="amount">元')
print('<input type="submit" value="加入清單" onclick="myFunction()"></h3>')
print('</form>')
choose_c = form.getvalue('selected_com')
choose_f = form.getvalue('selected')
amount = form.getvalue('amount')
print('<hr>')

try:
    fund = name_to_id.fund_name(choose_f,name_to_id.spl(name_to_id.company(choose_c)))
except:
    pass

import time

filename = "chosen.txt"

if os.path.isfile(filename):
    if os.path.getmtime(filename) <= time.time()-600:
        os.remove(filename)
        file = open(filename, "w")
    file = open(filename, "a")
else:
    file = open(filename, "w")

try:
    file.write(choose_f + "," + amount + "," + fund + "\n")
except:
    pass
file.close()

print('<script>')
print('$("#myTable").sisyphus();')
print('</script>')
         
print('<form method="post">')

print('<table width="400" bordercolor="black" border="1" style="border-collapse: collapse" id="myTable">')
print('<tr><th>基金名稱</th><th>投資金額</th>')
file = open(filename, "r")
table = file.readlines()
for rows in table:
    row = rows.split(",")
    print('<tr><td align="center">'""+row[0]+""'</td><td align="center">'""+row[1]+""'</td>')
print('</table>')

print('<h3>3. 對於您來說，您比較在意：</h3>')
print('（建議根據自己持有基金的習慣選擇期間長度）')
print('<br>')
print('<input type="radio" name="corr" value=“short_term”>短期分散風險程度')
print('<input type="radio" name="corr" value=“long_term”>長期分散風險程度')
print('<input type="submit" value="開始推薦"/><br>')
print('</form>')
way = form.getvalue("corr")

import warnings

if not sys.warnoptions:
    warnings.simplefilter("ignore")

if way != None:
    fid = []
    fam = []
    for rows in table:
        row = rows.split(",")
        fid.append(row[2].rstrip())
        fam.append(float(row[1]))
    result = []
    if way == "short_term":
        _, result = function.recommend_funds(fid, fam)
    else:
        result, _ = function.recommend_funds(fid, fam)
        
print('<h3>推薦結果</h3>')
print('<table width="600" bordercolor="black" border="1" style="border-collapse: collapse">')
print('<tr><th>風險分散排名</th><th>基金名稱</th><th>本基金平均月報酬</th>')
for i in range(len(result)):
    print('<tr><td align="center">'""+str(i+1)+""'</td><td align="center">'""+result[i][0]+""'</td><td align="center">'""+str(result[i][1])+""'</td>')
print('</table>')
print('</body>')
print('</html>')