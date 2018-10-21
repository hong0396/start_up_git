import pandas as pd

code=pd.read_csv('2018-10-13us_all_code.csv',encoding='gbk')
print(code.iloc[0]['open'])