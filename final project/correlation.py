#假設是dataframe的狀態
import numpy as np
from scipy.stats.stats import pearsonr, spearmanr

def person_corr(fundlist, a, b, period=100):
    fundlist = fundlist[[a,b]].tail(period).dropna()
    funda = fundlist[a].values
    fundb = fundlist[b].values
    corr, _= pearsonr(funda, fundb)
    return corr, fundlist.shape[0]
    
def rank_corr(fundlist, a, b, period=100):
    fundlist = fundlist[[a,b]].tail(period).dropna()
    funda = fundlist[a].values
    fundb = fundlist[b].values
    corr, _= spearmanr(funda, fundb)
    return corr

def downside_corr(fundlist, a, b, period=100):
    fundlist = fundlist[[a,b]].tail(period).dropna()
    funda = fundlist[a].values
    funda_last = np.concatenate((np.zeros(1,),funda[:-1]))
    fundb = fundlist[b].values
    fundb_last = np.concatenate((np.zeros(1,),fundb[:-1]))
    i, = np.where(funda<funda_last)
    corrab, _ = pearsonr(funda[i], fundb[i])
    j, = np.where(fundb<fundb_last)
    corrba, _ = pearsonr(funda[j], fundb[j])
    return corrab, corrba
