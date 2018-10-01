from yahoo_fin.stock_info import *
# http://theautomatic.net/yahoo_fin-documentation/#get_analysts_info

# a=get_analysts_info('nflx')
# b=get_balance_sheet('nflx')
# c=get_cash_flow('nflx')
# d=get_quote_table('aapl')
# d.get()

li=[]
tickers = tickers_nasdaq()
tickers_other = tickers_other()
tickers_all=tickers+tickers_other
for i in tickers_all:
    print('------------------------')
    li.append(get_quote_table(i))

df = pd.DataFrame.from_dict(li)
df.to_csv('sum.csv')
# tickers = tickers_other()

# print(tickers)