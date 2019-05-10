import pandas as pd 
import pickle
# import id_list
'''
需要更改檔案資料夾地址 以及 檔案名稱
'''
id_list = pd.read_csv(r'C:\Users\User\Documents\GitHub\HW1\final project\id1.csv')['fund_id'].tolist()


# 為了存檔
length_1_10 = int(  len(id_list) / 10 )



count = 0
df_list = []
error_list = []


for id in id_list:
	count+=1
	if count % length_1_10 == 0 : #如果已經處理十分之一，存檔一次
		merged_df = pd.concat(df_list, axis=1, sort = True)
		merged_df.to_csv('df_save_%d.csv' %count)
		df_list = [merged_df]
        
        
	print(id, '處理df，第%i/%i個基金' %(count, len(id_list)))
	price_url = 'https://tw.money.yahoo.com/fund/download/' + id + '?startDate=2017-05-10&endDate=2019-05-10'
	
	try:
		tem_df = pd.read_csv(price_url).iloc[:,0:2]
		tem_df.columns = ['date', id]
		tem_df.set_index('date', inplace = True)
		df_list.append(tem_df)
        
	except:
		error_list.append(id)
		pass
    
merged_df = pd.concat(df_list, axis=1, sort = True)
merged_df.to_csv('df_save_final.csv')

# dump file into pkl
with open('data.pickle', 'wb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    pickle.dump(merged_df, f)
	
	
# load file from pkl
'''

with open('data.pickle', 'rb') as f:
    data = pickle.load(f)

'''