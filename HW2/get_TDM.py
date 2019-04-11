import ast
import pandas as pd
import numpy as np
sentence_count = 0 

word_frag = False
word = ''
df_list = []
#with open( r'from NER\data_path_save\1554975189\results\label_test', 'r') as file:
with open( r'from NER/data_path_save/1554975189/results/label_test', 'r') as file:
	tem_dict = dict()
	for line in file:
		
		tokens = line.split()



		#如果遇到空行，則換下一句話
		if len(tokens) < 1:
			sentence_count += 1
			if len(tem_dict) > 0: 
				df  = pd.DataFrame.from_dict(tem_dict)
				df_list.append(df)
			tem_dict = dict()
			continue

		
			
		bytes_part = ast.literal_eval(tokens[0])
		s = bytes_part.decode('utf-8')  # Decode the bytes to convert to a string	
		
		if tokens[1] == '0':
			if not word_frag:
				#print(word)
				try:
					tem_dict[word][0] +=1
				except:
					tem_dict[word] = [1]
					
			word_frag = False
			
		elif tokens[1][0] == 'B':
			word = s
			word_frag = True
			
		elif tokens[1][0] == 'I':	
			word += s
			
#print(df_list[0:5])		
		
df = pd.concat(df_list).fillna(0)
'''
f = pd.read_csv('funds_info.csv')
fundname=f['基金id'].tolist()
fundname=[ str(fundname[i]) for i in range(len(fundname)) if i%3==0 ]
for i in range(len(fundname)):
    df.rename(index={i:fundname[i]}, inplace=True)
'''
names=[ '基金'+str(i) for i in range(df.shape[0])]
df.set_axis(names, axis='index', inplace=True)
print(df)
df.to_csv('TDM.csv')
cov=df.values
cov=cov.dot(np.transpose(cov))
df2=pd.DataFrame(cov)
for i in range(df2.shape[0]):
    df2.rename(columns={i:'基金'+str(i)}, index={i:'基金'+str(i)}, inplace=True)
print(df2)
df2.to_csv('Co-occur.csv')
