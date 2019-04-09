import pandas as pd
import jieba
import re

#jieba reference: https://github.com/fxsjy/jieba 

dict_of_tf_dict = dict()
dict_of_df_dict = dict()
	
def find_grams(article):
    article=re.sub('[^\u4e00-\u9fa5]+','',article)
    words=jieba.cut(article,cut_all=False)
        
    dict1 = dict()
    for word in words:
        if len(word)<=1:
            continue
        if word not in dict1:
            dict1[word] = 1
            try:
                dict_of_df_dict[word] += 1
            except:
                dict_of_df_dict[word] = 1
        else:
            dict1[word] += 1
	
    for key in dict1.keys():
        try:
            dict_of_tf_dict[key] += dict1[key]
			
        except:
            dict_of_tf_dict[key] = dict1[key]
	
def main(path):
# main function	找出所有的2~6 grams

    content = pd.read_csv(path).fillna('')
    content = content['投資策略'].tolist()	#一個list，每個元素為文章內文
    count = 0
		
		# 找出 n gram 中的 所有字詞來 並放入對應的dictionary中
    for article in content:
        print('內容:',count)
        count+=1
        if article==None:
            continue
		
        find_grams(article)
		
		
    #把n gram對應的dictionary中TF低於50的給排除掉
    for value,key in sorted(zip(dict_of_tf_dict.values(), dict_of_tf_dict.keys())):
        if value < 50:
            dict_of_df_dict.pop(key)
            dict_of_tf_dict.pop(key)
        else:
            break
		
if __name__ == '__main__' :
	import time
	t1 = time.time()
	main(path = 'funds_info.csv')
	print('time spent is:', time.time()-t1 ) #time spent is: 549.5456

	import csv #寫入檔案
	with open('tf_idf2.csv', 'w',newline='',) as file1:
		csv_writer = csv.writer(file1)
		csv_writer.writerow(['單詞', 'TF', 'DF'])
		for value,key in sorted(zip(dict_of_tf_dict.values(), dict_of_tf_dict.keys()), reverse=True):
		        csv_writer.writerow([ key, value, dict_of_df_dict[key] ])


		
