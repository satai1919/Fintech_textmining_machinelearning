import ast
import pandas as pd
sentence_count = 0 

word_frag = False
word = ''
df_list = []
with open( r'C:\Users\User\Documents\GitHub\HW1\HW2\from NER\data_path_save\1554975189\results\label_test', 'r') as file:
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
				print(word)
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
			
print(df_list[0:5])		
		
df = pd.concat(df_list)
print(df)
