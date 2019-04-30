#假設是dataframe的狀態
import numpy as np
from scipy.stats.stats import pearsonr, spearmanr

def person_corr(fundlist, a, b, period=100):
    funda = fundlist[""+a+""].tail(period).values
    fundb = fundlist[""+b+""].tail(period).values
    corr, _= pearsonr(funda, fundb)
    return corr
    

def rank_corr(fundlist, a, b, period=100):
    funda = fundlist[""+a+""].tail(period).values
    fundb = fundlist[""+b+""].tail(period).values
    corr, _= spearmanr(funda, fundb)
    return corr

def downside_corr(fundlist, a, b, period=100):
    funda = fundlist[""+a+""].tail(period).values
    fundb = fundlist[""+b+""].tail(period).values
    i, = np.where(funda<0)
    corrab, _ = pearsonr(funda[i], fundb[i])
    j, = np.where(fundb<0)
    corrba, _ = pearsonr(funda[j], fundb[j])
    return corrab, corrba
