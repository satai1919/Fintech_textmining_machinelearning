# 金融科技——文字探勘與機器學習
成員：財金所碩二 陳昱誠(github: ga877439)、財金四 林昕靜(github: satai1919)、資工二 許育銘(github: d768092)



## HW 1
~透過json發request抓ETF_NAV：完成~ 方法與老師規定不同，棄用

1. 完成ETF_NAV爬蟲
2. 完成經濟指標爬蟲\
皆使用jupyter呈現


## HW 2

4/10 by d768092:
新增使用jieba套件取詞的code和得出的單詞data(tf_idf2)\
新增手動標記單詞(set_type.py)，要自行標記約600個單詞的種類，可以直接改wordtype.csv或玩一下我那個程式(?)\
註:我沒有標記完，只有試一下確定程式能跑，如果覺得jieba有些分詞怪怪的也可以直接改wordtype.csv\
新增標記程式(label.py)，以wordtype中單詞的種類做標記，沒有用jieba分詞，所以改wordtype.csv的單詞還是能正確執行\
註:無法保證全部都有標到(ex.出現太少次的國家)，或是一個詞有兩個意思(理論上我們的資料不太會有一個詞是兩種不同種類吧)\
以上皆用python3執行
