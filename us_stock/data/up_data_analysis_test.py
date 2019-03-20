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
ds_disk =xr.open_dataset('E:/us_data/2019-03-17us_stock_month_saved.nc')
code=ds_disk.to_dataframe().columns.tolist()
n=1
for code_nm in code:
    zong = ds_disk.get(str(code_nm)).to_pandas().sort_index(ascending=False)
    zong = zong.dropna(axis = 0)  #删除行
    zong = zong.fillna(0)
    zong = zong.round(6)   
    # zong = zong.sort_values("time",ascending=False)
    # zong = zong.sort_index(ascending=False)
    zong = zong.sort_values("time",ascending=True)
    li=zong.columns.values.tolist()
    print('-------'+str(n)+'---------'+str(code_nm)+'------------------')
    n=n+1
    if len(zong)/12 <= 5 : # 1 上市小于5年
        regr = linear_model.LinearRegression()
        rang=(zong.close-zong.close[0])/zong.close[0]
        regr.fit(zong.index.values.reshape(-1, 1), rang) # 注意此处.reshape(-1, 1)，因为X是一维的！
        a, b = regr.coef_, regr.intercept_ 
        r2=r2_score(rang, regr.predict(zong.index.values.reshape(-1, 1)))
        # if  r2 > 0.9 and a[0] > 0.1:
        if a[0] > 0 and zong.close.values.tolist()[-1] >= zong.close.max()*0.9 and int(zong.close.max()) <= 26:
        # 2 价格大于最大值0.9
        # 3 价格小于20
            plt.scatter(zong.index.values.reshape(-1, 1), rang, color='blue')
            plt.plot(zong.index.values.reshape(-1, 1), regr.predict(zong.index.values.reshape(-1, 1)), color='red', linewidth=4)
            plt.title(str(code_nm)+' R2='+str(round(r2))+' a='+str(round(a[0],5)))
            plt.legend((str(zong.close.min()), str(zong.close.max())), loc='lower right')
            plt.show()






            
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

   