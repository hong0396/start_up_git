import os
import time

start = time.time()


os.system("python ./Sequential_all_code.py 1>>./log/log_code.txt")
print('----------------1---------------')
time.sleep(0.5)
os.system("python ./Sequential_dji_week.py 1>>./log/log_dji.txt")
print('----------------2---------------')
time.sleep(0.5)
os.system("python ./Sequential_main_quarter_income.py 1>>./log/log_income.txt")
print('----------------3---------------')
time.sleep(0.5)
os.system("python ./Sequential_week_grow_radio_rs_2.py 1>>./log/log_week_grow.txt")
print('----------------4---------------')
end = time.time()
print('总共运行'+(end-start)/60+'分钟')

