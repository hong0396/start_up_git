import pandas as pd

url="http://www.xgb.ecnu.edu.cn/xxcj/jzgsmd.asp?page=5"
ad=pd.read_html(url)
print(ad)

