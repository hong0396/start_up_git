import requests
# jzc_html = "http://datainterface3.eastmoney.com/EM_DataCenter_V3/api/GDZC/GetGDZC?" \
#                "tkn=eastmoney&cfg=gdzc&secucode=&sharehdname=&pageSize=200&pageNum=1&sortFields=NOTICEDATE&sortDirec=1" \
#                "&fx=2"\
#                "&startDate="+start_data+"&endDate="+end_data

jzc_html = "http://datainterface3.eastmoney.com/EM_DataCenter_V3/api/GDZC/GetGDZC?" \
               "tkn=eastmoney&cfg=gdzc&secucode=&sharehdname=&pageSize=200&pageNum=1&sortFields=NOTICEDATE&sortDirec=1" \
               "&fx=2"\
               "&startDate=&endDate="
response = requests.get(jzc_html).json()

print(response.get('Data'))
