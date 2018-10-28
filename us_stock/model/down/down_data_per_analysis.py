import pandas as pd
import numpy as np 
import pandas_datareader.data as web
import datetime
import time
import fix_yahoo_finance as yf
import xarray as xr

date=time.strftime('%Y-%m-%d',time.localtime(time.time()))
ds_disk =xr.open_dataset('E:/2018-10-27us_stock_day_saved.nc')
# # ds_disk=ds_disk
# print(dir(ds_disk.to_dict().keys()))
# dic_disk=ds_disk.to_dict()
# li_code_tmp=[]
# print(dir(ds_disk))

code=ds_disk.to_dataframe().columns.tolist()
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
li_123_tmp=[]
for code_nm in code:
        zong=ds_disk.get(str(code_nm)).to_pandas().sort_index(ascending=False)
        zong = zong.dropna(axis = 0)  #删除行
        # zong = zong.sort_values(by='time', ascending=False) 
        if len(zong) > 100:
            for i in range(len(zong)-5):
            # if round(zong.iloc[i]['open'],2) >= round(zong.iloc[i+1]['close'],2) and round(zong.iloc[i+1]['open'],2) >= round(zong.iloc[i+2]['open'],2):
                if round(zong.iloc[i]['open'],2) <= round(zong.iloc[i+2]['open'],2):
                    if round(zong.iloc[i+2]['open'],2) <= round(zong.iloc[i+3]['open'],2):
                        if round(zong.iloc[i+3]['open'],2) <= round(zong.iloc[i+4]['open'],2):
                            # if round(zong.iloc[i+4]['open'],2) <= round(zong.iloc[i+5]['open'],2):   

                                if (zong.iloc[i]['close'] - zong.iloc[i]['open'])/zong.iloc[i]['open'] <= 0:
                                    if (zong.iloc[i+1]['close'] - zong.iloc[i+1]['open'])/zong.iloc[i+1]['open'] >= 0:
                                        if (zong.iloc[i+2]['close'] - zong.iloc[i+2]['open'])/zong.iloc[i+2]['open'] <= 0:
                                            if (zong.iloc[i+3]['close'] - zong.iloc[i+3]['open'])/zong.iloc[i+3]['open'] <= 0:
                                                if (zong.iloc[i+4]['close'] - zong.iloc[i+4]['open'])/zong.iloc[i+4]['open'] <= 0:
                                                    if (zong.iloc[i+5]['close'] - zong.iloc[i+5]['open'])/zong.iloc[i+5]['open'] <= 0:

                                                        if zong.iloc[i-5]['close']:
                                                            li_code_tmp.append(str(code_nm))
                                                            # li_num_tmp.append(zong.iloc[i+5]['time'])
                                                            # li_0_tmp.append(zong.iloc[i]['close'])
                                                            li_0grow_tmp.append((zong.iloc[i+0]['close'] - zong.iloc[i+0]['open'])/zong.iloc[i+0]['open'] )
                                                            li_1grow_tmp.append((zong.iloc[i+1]['close'] - zong.iloc[i+1]['open'])/zong.iloc[i+1]['open'] )
                                                            li_2grow_tmp.append((zong.iloc[i+2]['close'] - zong.iloc[i+2]['open'])/zong.iloc[i+2]['open'] )
                                                            li_3grow_tmp.append((zong.iloc[i+3]['close'] - zong.iloc[i+3]['open'])/zong.iloc[i+3]['open'] )
                                                            li_4grow_tmp.append((zong.iloc[i+4]['close'] - zong.iloc[i+4]['open'])/zong.iloc[i+4]['open'] )
                                                            li_5grow_tmp.append((zong.iloc[i+5]['close'] - zong.iloc[i+5]['open'])/zong.iloc[i+5]['open'] )
                                                            li_1up_tmp.append((zong.iloc[i+1]['open'] - zong.iloc[i]['close'])/zong.iloc[i]['close']) 
                                                            li_2up_tmp.append((zong.iloc[i+2]['open'] - zong.iloc[i+1]['close'])/zong.iloc[i+1]['close']) 
                                                            li_3up_tmp.append((zong.iloc[i+3]['open'] - zong.iloc[i+2]['close'])/zong.iloc[i+2]['close']) 
                                                            li_4up_tmp.append((zong.iloc[i+4]['open'] - zong.iloc[i+3]['close'])/zong.iloc[i+3]['close'])
                                                            li_5up_tmp.append((zong.iloc[i+5]['open'] - zong.iloc[i+4]['close'])/zong.iloc[i+4]['close'])
                                                            li_123_avg=(zong.iloc[i-1]['close']+zong.iloc[i-2]['close']+zong.iloc[i-3]['close'])/3
                                                            li_123_tmp.append((li_123_avg - zong.iloc[i]['close'])/zong.iloc[i]['close'])



    # del jo, zong

    # gc.collect()

tmp_df=pd.DataFrame({'code': li_code_tmp,'li_0grow_tmp': li_0grow_tmp,
    'li_1grow_tmp': li_1grow_tmp,'li_2grow_tmp': li_2grow_tmp,
    'li_3grow_tmp': li_3grow_tmp,'li_4grow_tmp': li_4grow_tmp,
    'li_5grow_tmp': li_5grow_tmp, 'li_1up_tmp': li_1up_tmp,
    'li_2up_tmp': li_2up_tmp, 'li_3up_tmp': li_3up_tmp,
    'li_4up_tmp': li_4up_tmp, 'li_5up_tmp': li_5up_tmp,'li_123_tmp': li_123_tmp})
     
tmp_df.to_csv(date+'_down_analysis1.csv')


