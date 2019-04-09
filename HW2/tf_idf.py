import pandas as pd
str1 = '『』《》「」<>[]{}()“”’…,.。、:; ?~`!@#$%^&*+-/=_\\|' +'\n\t\r' +'””’' +"”’’”" +'1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
str2 = '＜＞［］｛｝（）“”’…，．：；　？	～｀！＠＃＄％＾＆＊＋－／＝＿＼＼｜' + '１２３４５６７８９０ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ'
split_set =  set(str1+str2)	#用來分割
#print(set(str1) & set(str2))

dict_of_tf_dict = dict()	#這是一個dictionary	裡面有5個dictionary
dict_of_df_dict = dict()
for i in range(2,7):	
	dict_of_tf_dict[i] = dict()		#用來記錄 i gram 字詞 的dicitonary
	dict_of_df_dict[i] = dict()	

def drop_sub_word(word):
	"""
	移除需要被移除的子字串，由於一個word是三個字的時候，需要check的只有兩個字的subword
	如果一個word是四個字的時候，需要check的只有三個字的subword，所以做法為下
	"""
	length = len(word)
	
	DF = dict_of_df_dict[length][word]
	
	sub_word_list = []		#比如說蔡英文
	sub_word_list.append( word[0:length-1] )	#蔡英
	sub_word_list.append( word[1:length] )	#英文
	

	for item in sub_word_list:	
		try:
			df_difference = dict_of_df_dict[length-1][item] - DF	#看"蔡英" 以及 "英文" 與"蔡英文" 的DF差距，注意! "蔡英"的DF必比 "蔡英文"DF高
			if df_difference <= DF * 0.05 :	#DF差距不到5%的話 就要被移除掉
				
				#移除該子字串
				dict_of_tf_dict[length-1].pop(item)
				dict_of_df_dict[length-1].pop(item)
		except:
			pass
	

def find_grams(article, gram = 2):
	"""
	用來找出所有 n_gram ，用dictionary，沒有輸出值
	"""

	dict1 = dict()
	for i in range( 0, len(article)- gram ):
		
		word =  article[i:i+gram]
		if len( set(word) & split_set ) == 0:
			if word not in dict1:
				dict1[word] = 1
				try:
					dict_of_df_dict[gram][word] += 1
				except:
					dict_of_df_dict[gram][word] = 1
			else:
				dict1[word] += 1
	
	for key in dict1.keys():
		try:
			dict_of_tf_dict[gram][key] += dict1[key]
			
		except:
			dict_of_tf_dict[gram][key] = dict1[key]

def contains_keyword(document, keyword_list):	#目前沒用到
	'''
	確認是否一個document內是否有包含keyword
	'''
	for keyword in keyword_list:
		if keyword in document:
			return True	#如果有包含 回傳True
			
	return False		#否則的話，都回傳False




	
def main(path):
# main function	找出所有的2~6 grams

	content = pd.read_csv(path)[u'投資策略'].tolist()	#一個list，每個元素為文章內文

	
	for n in range(2,7):	#對每個文章找出2~6 grams來
		count = 0
		
		# 找出 n gram 中的 所有字詞來 並放入對應的dictionary中
		for article in content:
			count +=1
			print('內容:',count, 'gram =', n)
		
			find_grams(article, n )
		
			# if count % 25000 == 0:	#每25000篇刪掉TF低的字詞
				# for value,key in sorted(zip(dict_of_tf_dict[n].values(), dict_of_tf_dict[n].keys())):
					# if value < 10 :	#每25000篇裡面 至少該字需要出現10次，否則就刪掉
						# dict_of_df_dict[n].pop(key)
						# dict_of_tf_dict[n].pop(key)
					# else:
						# break
				
		
		#把n gram對應的dictionary中TF低於50的給排除掉
		for value,key in sorted(zip(dict_of_tf_dict[n].values(), dict_of_tf_dict[n].keys())):
			if value < 50:
				dict_of_df_dict[n].pop(key)
				dict_of_tf_dict[n].pop(key)
			else:
				break
		
		#當n大於3之後，注意觀察是否有可以merge的子字串
		if n >=3:
			for key in dict_of_df_dict[n].keys():
				drop_sub_word(key)

		
if __name__ == '__main__' :
	import time

	t1 = time.time()
	main(path = r'C:\Users\User\Documents\GitHub\HW1\HW2\funds_info2.csv')
	print('time spent is:', time.time()-t1 ) #time spent is: 549.5456




	import csv #寫入檔案
	with open(r'C:\Users\User\Documents\GitHub\HW1\HW2\tf_idf', 'w',newline='', encoding = 'uft-8-sig') as file1:
		csv_writer = csv.writer(file1)
		csv_writer.writerow(['單詞', 'TF', 'DF'])
		for n in range(2,7):
			for value,key in sorted(zip(dict_of_tf_dict[n].values(), dict_of_tf_dict[n].keys()), reverse=True):
				csv_writer.writerow([ key, value, dict_of_df_dict[n][key] ])


		
