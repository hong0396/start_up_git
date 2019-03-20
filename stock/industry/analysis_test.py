import pandas as pd
import numpy as np 
import pandas_datareader.data as web
import datetime
import time
import fix_yahoo_finance as yf
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from sklearn.linear_model import LinearRegression
from sklearn.isotonic import IsotonicRegression
from sklearn.utils import check_random_state
from numba import jit
from sklearn import linear_model
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

date=time.strftime('%Y-%m-%d',time.localtime(time.time()))
sum_dic={}
ds_disk =xr.open_dataset('E:/stock_data/2019-03-10stock_industry_month_saved.nc')
code=ds_disk.to_dataframe().columns.tolist()
n=1
fig, ax = plt.subplots(nrows=3, ncols=1 )
for code_nm in code[:2]:
    zong = ds_disk.get(str(code_nm)).to_pandas().sort_index(ascending=False)
    zong = zong.dropna(axis = 0)  #删除行
    zong = zong.fillna(0)
    zong = zong.round(6)   
    # zong = zong.sort_values("time",ascending=False)
    # zong = zong.sort_index(ascending=False)
    zong = zong.sort_values("date",ascending=True)
    li=zong.columns.values.tolist()
    axes=ax[n]
    axes.plot(zong.date.values, zong.close.values, color='red', linewidth=4)
    # axes.title(code_nm)
    n=n+1

plt.show()

















    # print('-------'+str(n)+'---------'+str(code_nm)+'------------------')
    # n=n+1
    # if len(zong)/12 <= 5 and len(zong)/12 >= 2: # 1 上市小于5年
        # regr = linear_model.LinearRegression()
        # rang=(zong.close-zong.close[0])/zong.close[0]
        # regr.fit(zong.index.values.reshape(-1, 1), rang) # 注意此处.reshape(-1, 1)，因为X是一维的！
        # a, b = regr.coef_, regr.intercept_ 
        # r2=r2_score(rang, regr.predict(zong.index.values.reshape(-1, 1)))
        # if  r2 > 0.9 and a[0] > 0.1:
        # if a[0] > 0 and zong.close.values.tolist()[-1] >= zong.close.max()*0.9 and int(zong.close.max()) <= 30:
        # 2 价格大于最大值0.9
        # 3 价格小于20
    # plt.scatter(zong.index.values.reshape(-1, 1), rang, color='blue')







            
    ###方法二####### 
    # n = len(zong)
    # x = zong.index.values
    # y = zong.close
    # ir = IsotonicRegression()
    # y_ = ir.fit_transform(x, y)
    # lr = LinearRegression()
    # lr.fit(x[:, np.newaxis], y)  # x needs to be 2d for LinearRegression
    # # #############################################################################
    # # Plot result
    # segments = [[[i, y[i]], [i, y_[i]]] for i in range(n)]
    # lc = LineCollection(segments, zorder=0)
    # lc.set_array(np.ones(len(y)))
    # lc.set_linewidths(np.full(n, 0.5))
    # fig = plt.figure()
    # plt.plot(x, y, 'r.', markersize=12)
    # plt.plot(x, y_, 'g.-', markersize=12)
    # plt.plot(x, lr.predict(x[:, np.newaxis]), 'b-')
    # plt.gca().add_collection(lc)
    # plt.legend(('Data', 'Isotonic Fit', 'Linear Fit'), loc='lower right')
    # plt.title('Isotonic regression')
    # plt.show()
    ###方法二####### 

   