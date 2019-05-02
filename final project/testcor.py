import pandas as pd
import os
import math
from correlation import *

path = os.path.join('..','price.csv')

fund = pd.read_csv(path)

a = 'F0HKG05WZ3:FO'
'''
b = 'F0HKG05WVZ:FO'
print(b,downside_corr(fund,a,b))
'''
others = fund.columns[3:]

for b in others:
	print(b,downside_corr(fund,a,b))
    