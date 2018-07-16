

import baostock as bs
import pandas as pd

#### 登陆系统 ####
lg = bs.login(user_id="anonymous", password="123456")
#### 获取沪深A股估值指标(日频)数据 ####
# peTTM    动态市盈率
# psTTM    市销率
# pcfNcfTTM    市现率
# pbMRQ    市净率
rs = bs.query_history_k_data("sh.600000",
    "date,code,close,peTTM,pbMRQ,psTTM,pcfNcfTTM",
    start_date='2015-01-01', end_date='2017-12-31', 
    frequency="d", adjustflag="3")
#### 打印结果集 ####
result_list = []
while (rs.error_code == '0') & rs.next():
    # 获取一条记录，将记录合并在一起
    result_list.append(rs.get_row_data())
result = pd.DataFrame(result_list, columns=rs.fields)

#### 结果集输出到csv文件 ####
result.to_csv("peTTM_sh.600000_data.csv", encoding="gbk", index=False)
print(result)

#### 登出系统 ####
bs.logout()