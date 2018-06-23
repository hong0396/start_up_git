import re

html = "<html><div><span>我叫邓旭东</span> <span>今年 27岁</span> </div> </html>"
pattern = re.compile('<span>我叫(.*?)</span> <span>今年 (.*?)岁</span>')
result = re.findall(pattern,  html)
print(result)
