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
import signal
import time
import threading
import global_values
import main_car_control as car
from hotspot_server import Socket
import image_recording_client
import drivingStatusKeeper
from socket import SHUT_RDWR

s = Socket()
tcp_thread = threading.Thread(target=s.RunServer, args=(), daemon=False)
driving_status_thread = threading.Thread(target=drivingStatusKeeper.append_status, args=(), daemon=False)
streaming_thread =  threading.Thread(target=image_recording_client.run, args=(), daemon=True)

# handle the graceful shutdown of the program
def signal_handler(sig, frame):
    global_values.shutdown = True
    global_values.TCP_Server.shutdown(SHUT_RDWR)
    global_values.image_streaming_socket.shutdown(SHUT_RDWR)
    global_values.driving_status_socket.shutdown(SHUT_RDWR)
    tcp_thread.join()
    streaming_thread.join()
    driving_status_thread.join()
    
signal.signal(signal.SIGINT, signal_handler)

# driving loop
def cruising_mod():
    time.sleep(0.05)
    if global_values.pre_cruising_flag != global_values.cruising_flag:
        if global_values.pre_cruising_flag != 0:
            car.MotorControl.Stop()
        global_values.pre_cruising_flag = global_values.cruising_flag
    else:
        time.sleep(0.01)
    
print("------wifirobots start-----")

print("Starting livestream...")
streaming_thread.start()
print("Starting app connection...")
tcp_thread.start()
print("Starting driving status buffer control...")
driving_status_thread.start()

# start the video streaming to the app
# path_sh = 'sh ' + os.path.split(os.path.abspath(__file__))[0] + '/start_mjpg_streamer.sh &'
# call("%s" % path_sh, shell=True)

while not global_values.shutdown:
    try:
        cruising_mod()
    except Exception as e:
        time.sleep(0.01)
        print('Cruising_Mod error：', e)
