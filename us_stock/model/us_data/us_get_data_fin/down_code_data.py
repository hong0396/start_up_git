
import pandas as pd
import numpy as np 
import pandas_datareader.data as web
import datetime
import time
import fix_yahoo_finance as yf
import xarray as xr
from yahoo_fin.stock_info import *
from bs4 import BeautifulSoup
def write(name,na):
    file = open(name+'.txt','w');
    file.write(str(na));
    file.close();
    return True
def readd(name,na):
    file = open(name+'.txt','w');
    file.write(str(na));
    file.close();
    return True
yf.pdr_override()

# with open('nasdaq.txt') as f:
#     line1 = f.read()
    # print(line)
# with open('other.txt') as f:
#     line = f.read()

start=datetime.datetime(2007, 10, 1)
end=datetime.datetime(2009, 4, 1)

nu=0
# print('start')
# tickers1 = tickers_dow()
# write('dow',tickers1)
# print('1_ok')
# time.sleep(5)
# tickers2 = tickers_other()
# write('other',tickers2)
# print('2_ok')
# time.sleep(5)

# tickers3 = tickers_nasdaq()
# write('nasdaq',tickers3)
# print('3_ok')

# ids=tickers1+tickers2+tickers3
# a = list(set(ids))

# a=line.replace('[','').replace(']','').replace("'","").replace(" ","").strip(',').split(',')
# print(a[0])
# for n in range(len(a.code.tolist())):
#     if n//50 ==0:
#         nn=nn+1

a=pd.read_csv('all.csv')
a=a.code.values.tolist()



def save(na,ma):
    global nu
    dic={}
    for i in a[na:ma]:
        print(i)
        time.sleep(1)
        try:
            print('---------------'+str(nu)+'--------------------')
            result=web.get_data_yahoo(i,start,end)
            nu=nu+1
        except:
            continue 
        else: 
            if not result.empty:
                dic.update({i: result})
    ds=xr.Dataset(dic)  
    ds.to_netcdf('F:/down_saved_on_disk_all.nc',mode='a')
    return True

def save_0(na,ma):
    global nu
    dic={}
    for i in a[na:ma]:
        print(i)
        time.sleep(1)
        try:
            print('---------------'+str(nu)+'--------------------')
            result=web.get_data_yahoo(i,start,end)
            nu=nu+1
        except Exception as e:
            print(e)
            continue 
        else: 
            if not result.empty:
                dic.update({i: result})
    ds=xr.Dataset(dic)  
    ds.to_netcdf('F:/down_saved_on_disk_all.nc')
    return True

# save_0(0,50)

for n in range(len(a)//50):
    if n == 0:
        time.sleep(2)

        save_0(n*50,(n+1)*50)
    else:
        time.sleep(5)
        save(n*50,(n+1)*50)

    











# ds_disk =xr.open_dataset('saved_on_disk.nc')
# print(ds_disk['CORI'].to_pandas())


# with xr.open_dataset('saved_on_disk.nc') as ds:


# p = pd.Panel(dic)

# print(p)
# df_p=p.to_frame()

# df_p.to_csv('aaaaaa.csv')


# store = pd.HDFStore('all_store.h5')
# store['code'] = p


# p.to_hdf('all_store_p.h5','code', append=True)



# data = {'Item1' : pd.DataFrame(np.random.randn(4, 3)), 
#         'Item2' : pd.DataFrame(np.random.randn(4, 2))}
# p = pd.Panel(data)
# ds=apple.index.tolist()
# y=apple['Adj Close'].tolist()
# df=pd.DataFrame({'ds':ds,'y':y})
    
# df.to_csv('aapl.csv')


# store = pd.HDFStore('store.h5')
