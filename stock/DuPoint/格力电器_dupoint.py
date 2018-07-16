import baostock as bs
import pandas as pd
import time
# 登陆系统
lg = bs.login()
# 显示登陆返回信息
print('login respond error_code:'+lg.error_code)
print('login respond  error_msg:'+lg.error_msg)

# 查询杜邦指数
def dupont(code_n, year_n, quarter_n):
    dupont_list = []
    rs_dupont = bs.query_dupont_data(code=code_n, year=year_n, quarter=quarter_n)
    while (rs_dupont.error_code == '0') & rs_dupont.next():
        dupont_list.append(rs_dupont.get_row_data())
    result_profit = pd.DataFrame(dupont_list, columns=rs_dupont.fields)
    # 打印输出
    return result_profit

code="sz.000651"
li_pd=[]
for i in [2014,2015,2016,2017]:
    for j in [1,2,3,4]:
	    li_pd.append(dupont(code, i, j))

zong=pd.concat(li_pd)

# 结果集输出到csv文件
date=time.strftime('%Y-%m-%d',time.localtime(time.time()))
zong.to_csv(date+"_格力电器_dupont_data.csv", encoding="gbk", index=False)

# 登出系统
bs.logout()