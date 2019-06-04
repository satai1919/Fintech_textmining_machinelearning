from function import recommend_funds

picked_fund = ['F0HKG05WWS:FO','F00000XGAS:FO','F000000RIH:FO']
picked_num = [76,80,92]

long_term, short_term = recommend_funds(picked_fund, picked_num)

print('{0:<3s} {1:<12s} {2:<5s}'.format('排名','基金ID','平均月報酬',))
for rank, (fund_id, mean) in enumerate(long_term):
    print('{0:<5d} {1:<14s} {2:<.6f}'.format(rank+1, fund_id, mean))

print('{0:<3s} {1:<12s} {2:<5s}'.format('排名','基金ID','平均月報酬',))
for rank, (fund_id, mean) in enumerate(short_term):
    print('{0:<5d} {1:<14s} {2:<.6f}'.format(rank+1, fund_id, mean))
