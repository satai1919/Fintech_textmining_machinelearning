import pickle
import pandas as pd


def vocab_build(vocab_path, min_count = 5):
	"""

	:param vocab_path:
	:param corpus_path:
	:param min_count:
	:return:
	"""
	filename = 'funds_info.csv'
	f = pd.read_csv(filename).fillna('')

	content = f["投資策略"].tolist()

	word2id = {}
	for sent_ in content:
		print(sent_)
		for word in sent_:
			if word.isdigit():
				word = '<NUM>'
			elif ('\u0041' <= word <='\u005a') or ('\u0061' <= word <='\u007a'):
				word = '<ENG>'
			if word not in word2id:
				word2id[word] = [len(word2id)+1, 1]
			else:
				word2id[word][1] += 1
	low_freq_words = []
	for word, [word_id, word_freq] in word2id.items():
		if word_freq < min_count and word != '<NUM>' and word != '<ENG>':
			low_freq_words.append(word)
	for word in low_freq_words:
		del word2id[word]

	new_id = 1
	for word in word2id.keys():
		word2id[word] = new_id
		new_id += 1
	word2id['<UNK>'] = new_id
	word2id['<PAD>'] = 0

	print(len(word2id))
	with open(vocab_path, 'wb') as fw:
		pickle.dump(word2id, fw)
		
vocab_build('word2id.pkl')