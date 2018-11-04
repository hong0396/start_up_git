import pandas as pd
import numpy as np 
import pandas_datareader.data as web
import datetime
import time
import fix_yahoo_finance as yf
import xarray as xr
from numba import jit


# ds_disk =xr.open_dataset('E:/saved_on_disk.nc')
# # ds_disk=ds_disk
# print(dir(ds_disk.to_dict().keys()))
# dic_disk=ds_disk.to_dict()
# li_code_tmp=[]
# print(dir(ds_disk))
# ds_disk =xr.open_dataset('E:/save.nc')
# # ds_disk=ds_disk
# print(dir(ds_disk.to_dict().keys()))
# dic_disk=ds_disk.to_dict()
# li_code_tmp=[]
# print(dir(ds_disk))

# code=ds_disk.to_dataframe().columns.tolist()
def todate(timeStamp):
    timeArray = time.localtime(timeStamp/1000)
    otherStyleTime = time.strftime("%Y-%m-%d", timeArray)
    return otherStyleTime
def cal_div(x,y):
    if y == 0:
       theta = 0
    else:
       theta = x/y
    return theta


# @jit()
def  get_data(zong,li):
    li_code_tmp=[]
    li_0grow_tmp=[]
    li_1grow_tmp=[]
    li_2grow_tmp=[]
    li_3grow_tmp=[]
    li_4grow_tmp=[]
    li_5grow_tmp=[]




    li_1up_tmp=[]
    li_2up_tmp=[]
    li_3up_tmp=[]
    li_4up_tmp=[]
    li_5up_tmp=[]



    li_0max_tmp=[]
    li_1max_tmp=[]
    li_2max_tmp=[]
    li_3max_tmp=[]
    li_4max_tmp=[]
    li_5max_tmp=[]

    li_0min_tmp=[]
    li_1min_tmp=[]
    li_2min_tmp=[]
    li_3min_tmp=[]
    li_4min_tmp=[]
    li_5min_tmp=[]


    li_0max_close_tmp=[]
    li_1max_close_tmp=[]
    li_2max_close_tmp=[]
    li_3max_close_tmp=[]
    li_4max_close_tmp=[]
    li_5max_close_tmp=[]

    li_0min_close_tmp=[]
    li_1min_close_tmp=[]
    li_2min_close_tmp=[]
    li_3min_close_tmp=[]
    li_4min_close_tmp=[]
    li_5min_close_tmp=[]


    li_0max_min_tmp=[]
    li_1max_min_tmp=[]
    li_2max_min_tmp=[]
    li_3max_min_tmp=[]
    li_4max_min_tmp=[]
    li_5max_min_tmp=[]


    li_0max_min_near_tmp=[]
    li_1max_min_near_tmp=[]
    li_2max_min_near_tmp=[]
    li_3max_min_near_tmp=[]
    li_4max_min_near_tmp=[]


    li_0open_near_tmp=[]
    li_1open_near_tmp=[]
    li_2open_near_tmp=[]
    li_3open_near_tmp=[]
    li_4open_near_tmp=[]

    li_0close_near_tmp=[]
    li_1close_near_tmp=[]
    li_2close_near_tmp=[]
    li_3close_near_tmp=[]
    li_4close_near_tmp=[]


    li_1vol_tmp=[]
    li_2vol_tmp=[]
    li_3vol_tmp=[]
    li_4vol_tmp=[]
    li_5vol_tmp=[]

    li_grow_mean=[]
    li_grow_std=[]

    li_large_range_tmp=[]
    li_large_2345_range_tmp=[]

    li_time_tmp=[]
    li_123_tmp=[]
    time=li.index('time')
    open=li.index('open')
    close=li.index('close')
    high=li.index('high')
    low=li.index('low') 
    if len(zong) > 100:
        for i in range(len(zong)-6):
            if (zong[i][close] - zong[i][open])/zong[i][open] < 0:
                if (zong[i+1][close] - zong[i+1][open])/zong[i+1][open] < 0:
                    if (zong[i+2][close] - zong[i+2][open])/zong[i+2][open] < 0:
                        if (zong[i+3][close] - zong[i+3][open])/zong[i+3][open] >0:
                            if (zong[i+4][close] - zong[i+4][open])/zong[i+4][open] < 0:
                                if (zong[i+5][close] - zong[i+5][open])/zong[i+5][open] < 0:
                                    if (zong[i+6][close] - zong[i+6][open])/zong[i+6][open] < 0:

                                        if zong[i][open] < zong[i+1][open]:
                                            if zong[i+1][open] < zong[i+2][open]:
                                                if zong[i+5][open] < zong[i+6][open]:
                                                    if zong[i+4][open] < zong[i+5][open]:

                                                            if zong[i-5][close]:
                                                                li_time_tmp.append(zong[i][time])
                                                                li_code_tmp.append(str(code_nm))
                                                              
                                                                grow0_tmp=(zong[i+0][close] - zong[i+0][open])/zong[i+0][open] 
                                                                grow1_tmp=(zong[i+1][close] - zong[i+1][open])/zong[i+1][open] 
                                                                grow2_tmp=(zong[i+2][close] - zong[i+2][open])/zong[i+2][open] 
                                                                grow3_tmp=(zong[i+3][close] - zong[i+3][open])/zong[i+3][open] 
                                                                grow4_tmp=(zong[i+4][close] - zong[i+4][open])/zong[i+4][open] 
                                                                grow5_tmp=(zong[i+5][close] - zong[i+5][open])/zong[i+5][open] 

                                                                
                                                                ll_tmp=[grow0_tmp,grow1_tmp,grow2_tmp,grow3_tmp,grow4_tmp,grow5_tmp] 

                                                                li_grow_std.append(np.std(ll_tmp,ddof=1))
                                                                li_grow_mean.append(np.mean(ll_tmp))

                                                                
                                                                close0=zong[i+0][close]
                                                                close1=zong[i+1][close]
                                                                close2=zong[i+2][close]
                                                                close3=zong[i+3][close]
                                                                close4=zong[i+4][close]
                                                                close5=zong[i+5][close]

                                                                open0=zong[i+0][open]
                                                                open1=zong[i+1][open]
                                                                open2=zong[i+2][open]
                                                                open3=zong[i+3][open]
                                                                open4=zong[i+4][open]
                                                                open5=zong[i+5][open]

                                                                min_value=min(open0,open1,open2,open3,open4,open5,close0,close1,close2,close3,close4,close5)
                                                                max_value=max(open0,open1,open2,open3,open4,open5,close0,close1,close2,close3,close4,close5)
                                                                
                                                                li_large_range_tmp.append((max_value-min_value)/min_value)

                                                                min_2345value=min(open2,open3,open4,open5,close2,close3,close4,close5)
                                                                max_2345value=max(open2,open3,open4,open5,close2,close3,close4,close5)
                                                                
                                                                li_large_2345_range_tmp.append((max_2345value-min_2345value)/min_2345value)



                                                                li_0grow_tmp.append((zong[i+0][close] - zong[i+0][open])/zong[i+0][open] )
                                                                li_1grow_tmp.append((zong[i+1][close] - zong[i+1][open])/zong[i+1][open] )
                                                                li_2grow_tmp.append((zong[i+2][close] - zong[i+2][open])/zong[i+2][open] )
                                                                li_3grow_tmp.append((zong[i+3][close] - zong[i+3][open])/zong[i+3][open] )
                                                                li_4grow_tmp.append((zong[i+4][close] - zong[i+4][open])/zong[i+4][open] )
                                                                li_5grow_tmp.append((zong[i+5][close] - zong[i+5][open])/zong[i+5][open] )


                                                                




                                                                li_1up_tmp.append((zong[i+1][open] - zong[i][close])/zong[i][close]) 
                                                                li_2up_tmp.append((zong[i+2][open] - zong[i+1][close])/zong[i+1][close]) 
                                                                li_3up_tmp.append((zong[i+3][open] - zong[i+2][close])/zong[i+2][close]) 
                                                                li_4up_tmp.append((zong[i+4][open] - zong[i+3][close])/zong[i+3][close])
                                                                li_5up_tmp.append((zong[i+5][open] - zong[i+4][close])/zong[i+4][close])


                                                                


                                                                li_0max_tmp.append((zong[i+0][high] - zong[i+0][open])/zong[i+0][open] )
                                                                li_1max_tmp.append((zong[i+1][high] - zong[i+1][open])/zong[i+1][open] )
                                                                li_2max_tmp.append((zong[i+2][high] - zong[i+2][open])/zong[i+2][open] )
                                                                li_3max_tmp.append((zong[i+3][high] - zong[i+3][open])/zong[i+3][open] )
                                                                li_4max_tmp.append((zong[i+4][high] - zong[i+4][open])/zong[i+4][open] )
                                                                li_5max_tmp.append((zong[i+5][high] - zong[i+5][open])/zong[i+5][open] )
                                                                
                                                                li_0max_min_tmp.append((zong[i+0][high] - zong[i+0][low])/zong[i+0][low] )
                                                                li_1max_min_tmp.append((zong[i+1][high] - zong[i+1][low])/zong[i+1][low] )
                                                                li_2max_min_tmp.append((zong[i+2][high] - zong[i+2][low])/zong[i+2][low] )
                                                                li_3max_min_tmp.append((zong[i+3][high] - zong[i+3][low])/zong[i+3][low] )
                                                                li_4max_min_tmp.append((zong[i+4][high] - zong[i+4][low])/zong[i+4][low] )
                                                                li_5max_min_tmp.append((zong[i+5][high] - zong[i+5][low])/zong[i+5][low] )

                                                                li_0max_min_near_tmp.append((zong[i+1][high] - zong[i+0][low])/zong[i+0][low] )
                                                                li_1max_min_near_tmp.append((zong[i+2][high] - zong[i+1][low])/zong[i+1][low] )
                                                                li_2max_min_near_tmp.append((zong[i+3][high] - zong[i+2][low])/zong[i+2][low] )
                                                                li_3max_min_near_tmp.append((zong[i+4][high] - zong[i+3][low])/zong[i+3][low] )
                                                                li_4max_min_near_tmp.append((zong[i+5][high] - zong[i+4][low])/zong[i+4][low] )
                                                              

                                                                li_0open_near_tmp.append((zong[i+1][open] - zong[i+0][open])/zong[i+0][open] )
                                                                li_1open_near_tmp.append((zong[i+2][open] - zong[i+1][open])/zong[i+1][open] )
                                                                li_2open_near_tmp.append((zong[i+3][open] - zong[i+2][open])/zong[i+2][open] )
                                                                li_3open_near_tmp.append((zong[i+4][open] - zong[i+3][open])/zong[i+3][open] )
                                                                li_4open_near_tmp.append((zong[i+5][open] - zong[i+4][open])/zong[i+4][open] )
       
                                                                li_0close_near_tmp.append((zong[i+1][close] - zong[i+0][close])/zong[i+0][close] )
                                                                li_1close_near_tmp.append((zong[i+2][close] - zong[i+1][close])/zong[i+1][close] )
                                                                li_2close_near_tmp.append((zong[i+3][close] - zong[i+2][close])/zong[i+2][close] )
                                                                li_3close_near_tmp.append((zong[i+4][close] - zong[i+3][close])/zong[i+3][close] )
                                                                li_4close_near_tmp.append((zong[i+5][close] - zong[i+4][close])/zong[i+4][close] )
       





                                                                li_0min_tmp.append((zong[i+0][low] - zong[i+0][open])/zong[i+0][open] )
                                                                li_1min_tmp.append((zong[i+1][low] - zong[i+1][open])/zong[i+1][open] )
                                                                li_2min_tmp.append((zong[i+2][low] - zong[i+2][open])/zong[i+2][open] )
                                                                li_3min_tmp.append((zong[i+3][low] - zong[i+3][open])/zong[i+3][open] )
                                                                li_4min_tmp.append((zong[i+4][low] - zong[i+4][open])/zong[i+4][open] )
                                                                li_5min_tmp.append((zong[i+5][low] - zong[i+5][open])/zong[i+5][open] )

                                                                li_0max_close_tmp.append((zong[i+0][high] - zong[i+0][close])/zong[i+0][close] )
                                                                li_1max_close_tmp.append((zong[i+1][high] - zong[i+1][close])/zong[i+1][close] )
                                                                li_2max_close_tmp.append((zong[i+2][high] - zong[i+2][close])/zong[i+2][close] )
                                                                li_3max_close_tmp.append((zong[i+3][high] - zong[i+3][close])/zong[i+3][close] )
                                                                li_4max_close_tmp.append((zong[i+4][high] - zong[i+4][close])/zong[i+4][close] )
                                                                li_5max_close_tmp.append((zong[i+5][high] - zong[i+5][close])/zong[i+5][close] )
                                                                
                                                                li_0min_close_tmp.append((zong[i+0][low] - zong[i+0][close])/zong[i+0][close] )
                                                                li_1min_close_tmp.append((zong[i+1][low] - zong[i+1][close])/zong[i+1][close] )
                                                                li_2min_close_tmp.append((zong[i+2][low] - zong[i+2][close])/zong[i+2][close] )
                                                                li_3min_close_tmp.append((zong[i+3][low] - zong[i+3][close])/zong[i+3][close] )
                                                                li_4min_close_tmp.append((zong[i+4][low] - zong[i+4][close])/zong[i+4][close] )
                                                                li_5min_close_tmp.append((zong[i+5][low] - zong[i+5][close])/zong[i+5][close] )

                                                                










                                                                

                                                                # if zong[i]['Volume'] != 0 :
                                                                #     li_1vol_tmp.append((zong[i+1]['Volume'] - zong[i]['Volume'])/zong[i]['Volume']) 
                                                                # else:
                                                                #     li_1vol_tmp.append(0)
                                                                # if zong[i+1]['Volume'] != 0 :
                                                                #     li_2vol_tmp.append((zong[i+2]['Volume'] - zong[i+1]['Volume'])/zong[i+1]['Volume']) 
                                                                # else:
                                                                #     li_2vol_tmp.append(0)
                                                                # if zong[i+2]['Volume'] != 0 :
                                                                #     li_3vol_tmp.append((zong[i+3]['Volume'] - zong[i+2]['Volume'])/zong[i+2]['Volume']) 
                                                                # else:
                                                                #     li_3vol_tmp.append(0)
                                                                # if zong[i+3]['Volume'] != 0 :
                                                                #     li_4vol_tmp.append((zong[i+4]['Volume'] - zong[i+3]['Volume'])/zong[i+3]['Volume']) 
                                                                # else:
                                                                #     li_4vol_tmp.append(0)
                                                                # if zong[i+4]['Volume'] != 0 :
                                                                #     li_5vol_tmp.append((zong[i+5]['Volume'] - zong[i+4]['Volume'])/zong[i+4]['Volume']) 
                                                                # else:
                                                                #     li_5vol_tmp.append(0)
                     

                        




                                                                li_123_avg=(zong[i-1][close]+zong[i-2][close])/2
                                                                li_123_tmp.append((li_123_avg - min_value)/min_value)



        # del jo, zong

        # gc.collect()
    print('ok')    
    if li_code_tmp and li_0grow_tmp:
        ttmp=True
        tmp_dic={'code': li_code_tmp,'li_0grow_tmp': li_0grow_tmp,
        'li_1grow_tmp': li_1grow_tmp,'li_2grow_tmp': li_2grow_tmp,
        'li_3grow_tmp': li_3grow_tmp,'li_4grow_tmp': li_4grow_tmp,
        'li_5grow_tmp': li_5grow_tmp, 'li_1up_tmp': li_1up_tmp,
        'li_2up_tmp': li_2up_tmp, 'li_3up_tmp': li_3up_tmp,
        'li_4up_tmp': li_4up_tmp, 'li_5up_tmp': li_5up_tmp,
        'li_0max_tmp': li_0max_tmp,
        'li_1max_tmp': li_1max_tmp,'li_2max_tmp': li_2max_tmp,
        'li_3max_tmp': li_3max_tmp,'li_4max_tmp': li_4max_tmp,'li_5max_tmp': li_5max_tmp,
         'li_0min_tmp': li_0min_tmp,
        'li_1min_tmp': li_1min_tmp,'li_2min_tmp': li_2min_tmp,
        'li_3min_tmp': li_3min_tmp,'li_4min_tmp': li_4min_tmp,'li_5min_tmp': li_5min_tmp,

         'li_0max_min_tmp':li_0max_min_tmp,
         'li_1max_min_tmp':li_1max_min_tmp,
         'li_2max_min_tmp':li_2max_min_tmp,
         'li_3max_min_tmp':li_3max_min_tmp,
         'li_4max_min_tmp':li_4max_min_tmp,
         'li_5max_min_tmp':li_5max_min_tmp,
          
         'li_0max_min_near_tmp':li_0max_min_near_tmp,
         'li_1max_min_near_tmp':li_1max_min_near_tmp,
         'li_2max_min_near_tmp':li_2max_min_near_tmp,
         'li_3max_min_near_tmp':li_3max_min_near_tmp,
         'li_4max_min_near_tmp':li_4max_min_near_tmp,

         #    'li_0open_near_tmp':li_0open_near_tmp,
         #    'li_1open_near_tmp':li_1open_near_tmp,
         #    'li_2open_near_tmp':li_2open_near_tmp,
         #    'li_3open_near_tmp':li_3open_near_tmp,
         #    'li_4open_near_tmp':li_4open_near_tmp,

         #    'li_0close_near_tmp':li_0close_near_tmp,
         #    'li_1close_near_tmp':li_1close_near_tmp,
         #    'li_2close_near_tmp':li_2close_near_tmp,
         #    'li_3close_near_tmp':li_3close_near_tmp,
         #    'li_4close_near_tmp':li_4close_near_tmp,

        'li_large_range_tmp':li_large_range_tmp,
        'li_large_2345_range_tmp':li_large_2345_range_tmp,

        'li_0max_close_tmp': li_0max_close_tmp,
        'li_1max_close_tmp': li_1max_close_tmp,'li_2max_close_tmp': li_2max_close_tmp,
        'li_3max_close_tmp': li_3max_close_tmp,'li_4max_close_tmp': li_4max_close_tmp,'li_5max_close_tmp': li_5max_close_tmp,
         'li_0min_close_tmp': li_0min_close_tmp,
        'li_1min_close_tmp': li_1min_close_tmp,'li_2min_close_tmp': li_2min_close_tmp,
        'li_3min_close_tmp': li_3min_close_tmp,'li_4min_close_tmp': li_4min_close_tmp,'li_5min_close_tmp': li_5min_close_tmp,
        #  'li_1vol_tmp': li_1vol_tmp,
        # 'li_2vol_tmp': li_2vol_tmp, 'li_3vol_tmp': li_3vol_tmp,
        # 'li_4vol_tmp': li_4vol_tmp, 'li_5vol_tmp': li_5vol_tmp,
         'li_time_tmp':li_time_tmp,
        'li_grow_std':li_grow_std,'li_grow_mean':li_grow_mean,
        'li_123_tmp': li_123_tmp}
    else:
        tmp_dic=False
        ttmp=False

    return tmp_dic,ttmp
         
# order = ['code', 'li_0close_near_tmp', 'li_0grow_tmp', 'li_0max_close_tmp', 'li_0max_min_near_tmp', 'li_0max_min_tmp', 'li_0max_tmp', 'li_0min_close_tmp', 'li_0min_tmp', 'li_0open_near_tmp', 'li_123_tmp', 'li_1close_near_tmp', 'li_1grow_tmp', 'li_1max_close_tmp', 'li_1max_min_near_tmp', 'li_1max_min_tmp', 'li_1max_tmp', 'li_1min_close_tmp', 'li_1min_tmp', 'li_1open_near_tmp', 'li_1up_tmp', 'li_2close_near_tmp', 'li_2grow_tmp', 'li_2max_close_tmp', 'li_2max_min_near_tmp', 'li_2max_min_tmp', 'li_2max_tmp', 'li_2min_close_tmp', 'li_2min_tmp', 'li_2open_near_tmp', 'li_2up_tmp', 'li_3close_near_tmp', 'li_3grow_tmp', 'li_3max_close_tmp', 'li_3max_min_near_tmp', 'li_3max_min_tmp', 'li_3max_tmp', 'li_3min_close_tmp', 'li_3min_tmp', 'li_3open_near_tmp', 'li_3up_tmp', 'li_4close_near_tmp', 'li_4grow_tmp', 'li_4max_close_tmp', 'li_4max_min_near_tmp', 'li_4max_min_tmp', 'li_4max_tmp', 'li_4min_close_tmp', 'li_4min_tmp', 'li_4open_near_tmp', 'li_4up_tmp', 'li_5grow_tmp', 'li_5max_close_tmp', 'li_5max_min_tmp', 'li_5max_tmp', 'li_5min_close_tmp', 'li_5min_tmp', 'li_5up_tmp', 'li_grow_mean', 'li_grow_std']
# tmp_df = tmp_df[order] 
 

sum_dic={}
ds_disk =xr.open_dataset('E:/2018-10-27us_stock_day_saved.nc')
code=ds_disk.to_dataframe().columns.tolist()
for code_nm in code:
    zong = ds_disk.get(str(code_nm)).to_pandas().sort_index(ascending=False)
    zong = zong.dropna(axis = 0)  #删除行
    zong = zong.fillna(0)
      
    zong = zong.sort_values("time",ascending=False)
    zong = zong.drop(['volume'], axis = 1)
    # zong = zong.sort_index(ascending=False)
    li=zong.columns.values.tolist()
    # print(li.index('attrib_nm2'))
     
    tmp_dic, ttmp=get_data(zong.values,li)
    if ttmp and tmp_dic:
        for key in tmp_dic:
            if sum_dic.get(key):
                sum_dic[key].extend(tmp_dic[key])
            else:     
                sum_dic[key]=tmp_dic[key]

#检验数据            
# for key in sum_dic:
#     print(key)
#     print(len(sum_dic[key]))

tmp_df=pd.DataFrame(sum_dic)
tmp_df['li_time_tmp']=tmp_df['li_time_tmp'].apply(todate)
tmp_df.to_csv('test1_analysis_1.csv',index=False)






