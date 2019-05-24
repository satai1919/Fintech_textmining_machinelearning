#假設是dataframe的狀態
import numpy as np
from scipy.stats.stats import pearsonr, spearmanr

def person_corr(fundlist, a, b, period=100):
    period = min(period,fundlist.shape[0])
    fundlist = fundlist[[a,b]].tail(period).dropna()
    funda = fundlist[a].values
    fundb = fundlist[b].values
    corr, _= pearsonr(funda, fundb)
    return corr
    
def rank_corr(fundlist, a, b, period=100):
    period = min(period,fundlist.shape[0])
    fundlist = fundlist[[a,b]].tail(period).dropna()
    funda = fundlist[a].values
    fundb = fundlist[b].values
    corr, _= spearmanr(funda, fundb)
    return corr

def downside_corr(fundlist, a, b, period=100):
    period = min(period,fundlist.shape[0])
    fundlist = fundlist[[a,b]].tail(period).dropna()
    funda = fundlist[a].values
    fundb = fundlist[b].values
    fundb_last = np.concatenate((np.zeros(1,),fundb[:-1]))
    i = funda[1:]<funda[:-1]
    corrab, _ = pearsonr(funda[1:][i], fundb[1:][i])
    j = fundb[1:]<fundb[:-1]
    corrba, _ = pearsonr(funda[1:][j], fundb[1:][j])
    return (corrab+corrba)/2
