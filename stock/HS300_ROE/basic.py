import tushare as ts

basic=ts.get_stock_basics()

basic=basic.sort_values(by=["totalAssets"], ascending=False)

b500=basic[0:500]

basic.to_excel('D:/Git/stock/basic.xlsx')
b500.to_excel('D:/Git/stock/b500.xlsx')