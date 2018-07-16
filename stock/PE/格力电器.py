import baostock as bs
import pandas as pd
import time
#### 登陆系统 ####
lg = bs.login(user_id="anonymous", password="123456")
#### 获取沪深A股估值指标(日频)数据 ####
# peTTM    动态市盈率
# psTTM    市销率
# pcfNcfTTM    市现率
# pbMRQ    市净率
date=time.strftime('%Y-%m-%d',time.localtime(time.time()))

rs = bs.query_history_k_data("sz.000651",
    "date,code,close,peTTM,pbMRQ,psTTM,pcfNcfTTM",
    start_date='2000-01-01', end_date=date, 
    frequency="d", adjustflag="3")
#### 打印结果集 ####
result_list = []
while (rs.error_code == '0') & rs.next():
    # 获取一条记录，将记录合并在一起
    result_list.append(rs.get_row_data())
result = pd.DataFrame(result_list, columns=rs.fields)

#### 结果集输出到csv文件 ####
result.to_csv(date+"_格力电器_peTTM_data.csv", encoding="gbk", index=False)
print(result)

#### 登出系统 ####
bs.logout()