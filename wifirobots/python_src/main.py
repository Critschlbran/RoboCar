# coding:utf-8
"""
@version: python3.7
@Author  : hbwz
@Explain :主程序，多线程启动
@contact :
@Time    :2020/05/09
@File    :hbwz_startmain.py
@Software: PyCharm
"""
import os
import time
import threading
import global_values
import main_car_control as car
from hotspot_server import Socket
from subprocess import call

socket = Socket()


# 多功能模式切换
def cruising_mod():
    time.sleep(0.05)
    if global_values.pre_cruising_flag != global_values.cruising_flag:
        if global_values.pre_cruising_flag != 0:
            car.MotorControl.Stop()
        global_values.pre_cruising_flag = global_values.cruising_flag
    else:
        time.sleep(0.01)
    
# 蓝牙终端设置
print("------wifirobots start-----")

t1 = threading.Thread(target=socket.RunServer, args=(), daemon=False)
t1.start()
print("Starting server thread..")

# path_sh = 'sh ' + os.path.split(os.path.abspath(__file__))[0] + '/start_mjpg_streamer.sh &'
# call("%s" % path_sh, shell=True)

while True:
    try:
        cruising_mod()
    except Exception as e:
        time.sleep(0.01)
        print('Cruising_Mod error：', e)
