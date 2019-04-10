import pandas as pd
import csv
wordtype=dict()
words=[]
try:
    path = 'wordtype.csv'
    table = pd.read_csv(path).fillna('')
    words = table['單詞'].tolist()
    for word in words:
        wordtype[word]=table.loc(word,'種類')
except:
    path = 'tf_idf2.csv'
    words = pd.read_csv(path)['單詞'].tolist()
    for word in words:
        wordtype[word]=''

types = {'LOC','TYP','STY'} #set for valid type
'''
LOC: location
TYP: type
STY: style
'''
start=input('start word (default first word):')
while True:
    if start=='':
        start=words[0]
        break
    elif start in words:
        break
    else:
        input(start+' not found. Please type again (or just press enter and start at first word).') 

start_type=False
finish=False
for word in words:
    if not start_type:
        if word == start:
            start_type=True
        else:
            continue
    if finish:
        break
    t=input('type of '+word+':')
    while True:
        if t in types:
            wordtype[word]=t
            break
        elif t=='stop':
            finish=True
            break
        elif t=='':
            break
        else:
            print('error: please type one of the following:')
            t=input('"LOC","TYP","STY",or just press enter:')
with open('wordtype.csv','w') as output:
    writer=csv.writer(output)
    writer.writerow(['單詞','種類'])
    for word in words:
        writer.writerow([word,wordtype[word]])
