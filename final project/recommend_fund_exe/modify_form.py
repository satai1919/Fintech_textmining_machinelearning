#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
import name_to_id, function

data = name_to_id.data
cols = list(data.columns)

def callbackFunc(event):
    fundlist = []
    for i in range(len(name_to_id.company(com.get()))):
        fundlist.append(name_to_id.company(com.get())[i][1].rstrip())
    fund['value'] = tuple(fundlist)


def appendtoList():
    if tree.get_children() != None:
        delButton(tree)
    chosen.append([fund.get(), name_to_id.fund_name(fund.get(), name_to_id.company(com.get())), int(amount.get())])
    for i in range(len(chosen)):
        tree.insert("",i,values=tuple([chosen[i][0],chosen[i][2]]))
#    print(chosen)

def delete():
    delButton(tree)
    for i in range(len(chosen)):
        chosen.pop()
 
def delButton(tree):
    x=tree.get_children()
    for item in x:
        tree.delete(item)
        

def recommend():
    if t2.get_children() != None:
        delButton(t2)
    if v.get() == 1:
        term = 'short_term'
    elif v.get() == 2:
        term = 'long_term'
    fid = []
    fam = []
    for i in range(len(chosen)):
        fid.append(chosen[i][1])
        fam.append(chosen[i][2])
#    print(fid)
#    print(fam)
    rlist = function.recommend_funds(fid, fam, term)
    for i in range(len(rlist)):
        t2.insert("",i,values=tuple([i+1,rlist[i][0],round(rlist[i][1], 4)]))

app = tk.Tk() 
app.title("台灣境內境外基金推薦")
app.geometry("1160x600")
app.configure(background = "whitesmoke")
app.resizable(0,0)

intro = tk.Frame(app, bg='white', width = 1040, height=130)
intro.place(x=60, y=30, anchor='nw')
name = tk.Label(intro, text='基金推薦資料庫', font=('Microsoft JhengHei',40),bg='white', fg='black')
name.place(x=330, y=20, anchor='nw')
introduction = tk.Label(intro, text='您輸入現有投資組合，我們幫您推薦基金，讓您的獲利更加穩定。',bg='white', font=('Microsoft JhengHei', 20), fg='black')
introduction.place(x=170, y=80, anchor='nw')

background = tk.Frame(app, bg='white', width = 1040, height=140)
background.place(x=60, y=175, anchor='nw')
#問問題的地方
q1 = tk.Label(background, text='1. 請在以下欄位選擇您已購買的基金', bg='white', font=('Microsoft JhengHei',11), fg='black')
q1.place(x=30, y=10, anchor='nw')
s1 = tk.Label(background, text='基金公司關鍵字：', bg='white', font=('Microsoft JhengHei',11), fg='black')
s1.place(x=45, y=40, anchor='nw')
com = ttk.Combobox(background, state='readonly',width=10)
com['values'] = tuple(cols)
com.place(x=170, y=40, anchor='nw')
s1 = tk.Label(background, text='基金名稱：', bg='white', font=('Microsoft JhengHei',11), fg='black')
s1.place(x=310, y=40, anchor='nw')
fund = ttk.Combobox(background, state='readonly', width=40)
fund.place(x=390, y=40, anchor='nw')
com.bind("<<ComboboxSelected>>", callbackFunc)

q2 = tk.Label(background, text='2. 已投資於此基金的金額（請直接輸入數字，如：10000）：', bg='white', font=('Microsoft JhengHei',11), fg='black')
q2.place(x=30, y=80, anchor='nw')
amount = tk.Entry(background)
amount.place(x=450, y=80, anchor='nw')


b2 = tk.Frame(app, bg='white', width = 500, height=230)
b2.place(x=60, y=330, anchor='nw')
in1 = tk.Label(b2, text='已選擇的基金：', bg='white', font=('Microsoft JhengHei',11), fg='black')
in1.place(x=10, y=5, anchor='nw')
tree = ttk.Treeview(b2, show='headings', height=4)
tree["columns"]=("基金名稱","投資金額")
tree.column("基金名稱",width=390)
tree.column("投資金額",width=70)
tree.heading("基金名稱",text="基金名稱")
tree.heading("投資金額",text="投資金額")
tree.place(x=15, y=30, anchor='nw')
chosen = []
addtolist = tk.Button(background, text='加入清單', command=appendtoList)
addtolist.place(x=480, y=110)
delete = tk.Button(b2, text='清除表格內容重填', command=delete)
delete.place(x=130, y=5, anchor='nw')

q3 = tk.Label(b2, text='3. 對於您來說，您比較在意：（根據持有習慣選擇期間長度）', bg='white', font=('Microsoft JhengHei',11), fg='black')
q3.place(x=30, y=150, anchor='nw')
v = tk.IntVar()
rdioOne = tk.Radiobutton(b2, text='短期分散風險程度',variable=v, value=1, bg='white') 
rdioTwo = tk.Radiobutton(b2, text='長期分散風險程度',variable=v, value=2, bg='white') 
rdioOne.place(x=45, y=180, anchor='nw')
rdioTwo.place(x=200, y=180, anchor='nw')

b3 = tk.Frame(app, bg='white', width = 525, height=230)
b3.place(x=575, y=330, anchor='nw')
in2 = tk.Label(b3, text='推薦您選擇以下其中一支基金：', bg='white', font=('Microsoft JhengHei',11), fg='black')
in2.place(x=10, y=5, anchor='nw')
t2 = ttk.Treeview(b3, show='headings', height=8)
t2["columns"]=('排名','基金名稱','平均月報酬')
t2.column("排名",width=30)
t2.column("基金名稱",width=380)
t2.column("平均月報酬",width=70)
t2.heading("排名",text="排名")
t2.heading("基金名稱",text="基金名稱")
t2.heading("平均月報酬",text="平均月報酬")
t2.place(x=20, y=30, anchor='nw')

submit = tk.Button(b2, text='開始推薦', command=recommend)
submit.place(x=410, y=200, anchor='nw')


app.mainloop()