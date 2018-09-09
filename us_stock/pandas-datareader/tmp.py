import datetime
import pandas as pd
import pandas_datareader.data as web
import fix_yahoo_finance as yf
import datetime
from pandas_datareader import data as pdr
import fix_yahoo_finance as yf

# start = datetime.datetime(2015, 2, 9)
# end = datetime.datetime(2017, 5, 24)
# f = web.DataReader('F', 'iex', start, end)
# print(f.loc['2015-02-09'])

yf.pdr_override() # <== that's all it takes :-)

# download dataframe
data = pdr.get_data_yahoo("SPY", start="2017-01-01", end="2017-04-30")

# download Panel
data = pdr.get_data_yahoo(["SPY", "IWM"], start="2017-01-01", end="2017-04-30")










# yf.pdr_override()

# start = datetime.datetime(2017, 1, 1)
# end = datetime.datetime(2017, 12, 31)
# data = web.get_data_yahoo('AAPL', start, end)
# print(data.head(10))
# print(type(data))