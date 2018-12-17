import requests
 
#百度地图API搜索
def baidu_search(query, region):
    url = 'http://api.map.baidu.com/place/v2/search?'
    output = 'json'
    ak = 'vLyZjPkryKy5Mn2LG1fp6ColMGFfFFiu'
    uri = url + 'query=' + query + '&region='+region+'&output=' + output + '&ak=' + ak
    r = requests.get(uri)
    response_dict = r.json()
    results = response_dict["results"]
    for adr in results:
        name = adr['name']
        location= adr['location']
        lng = float(location['lng'])
        lat = float(location['lat'])
        address = adr['address']
        # telephone = adr['telephone']
        print('名称：'+name)
        print('坐标：%f,%f' %(lat,lng))
        print('地址：'+address)
        # print('电话：'+telephone)
 
baidu_search('曼玲粥店','上海')
