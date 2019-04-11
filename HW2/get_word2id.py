import pickle
import pandas as pd


def vocab_build(vocab_path, min_count = 5):
	"""

	:param vocab_path: the location we want to save the pkl file
	:param min_count: default five, if frequency less than min_count, the word should be dropped
	:return: None
	"""
	#讀取檔案
	filename = 'funds_info.csv'
	f = pd.read_csv(filename).fillna('')

	content = f["投資策略"].tolist()

	#創建id字典
	word2id = {}
	
	#首先把每一個sentence拿出來
	for sent_ in content:

		for word in sent_:	#對一個文章內的的每一個字，我們看看是否是number 還是 英文字母
			if word.isdigit():	#if數字
				word = '<NUM>'
			elif ('\u0041' <= word <='\u005a') or ('\u0061' <= word <='\u007a'):	#if英文字
				word = '<ENG>'
				
			#如果沒在字典裡出現過，那創建一個list, 第一個元素是id, 第二個是出現次數(frequency)
			if word not in word2id:	
				word2id[word] = [len(word2id)+1, 1]
			#在字典出現過則更新出現次數
			else:
				word2id[word][1] += 1
				
	#把frequency過低的字刪掉
	low_freq_words = []
	for word, [word_id, word_freq] in word2id.items():
		if word_freq < min_count and word != '<NUM>' and word != '<ENG>':
			low_freq_words.append(word)
	for word in low_freq_words:
		del word2id[word]
	#更新word2id這個字典，只保留id，因為不需要frequency了
	new_id = 1
	for word in word2id.keys():
		word2id[word] = new_id
		new_id += 1
	word2id['<UNK>'] = new_id
	word2id['<PAD>'] = 0

	print(len(word2id))
	#save PKL file
	with open(vocab_path, 'wb') as fw:
		pickle.dump(word2id, fw)
		
#run the script		
vocab_build('word2id.pkl')


