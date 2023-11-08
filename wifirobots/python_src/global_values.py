# coding:utf-8
"""
@version: python3.7
@Author  : hbwz
@Explain : Global static files
@contact :
@Time    :2020/05/09
@File    :hbwz_global.py
@Software: PyCharm
"""
import RPi.GPIO as GPIO
import time
from socket import *

revstatus = 0
cruising_flag = 0
pre_cruising_flag = 0
min_distence = 15

# thread control
shutdown = False

# streaming
streaming_framerate = 20
image_streaming_socket = socket(AF_INET, SOCK_STREAM)
driving_status_socket = socket(AF_INET, SOCK_STREAM)

# Define TCP server related variables

TCP_Server = socket(AF_INET, SOCK_STREAM)
TCP_Server.bind(('', 2001))
TCP_Server.listen()
TCP_buffer = []

recv_len = 5  # Received character length

TCP_Client = False
socket_flag = 0
before_angle = [0, 0, 0, 0, 0, 0, 0, 0]

# Ultrasonic marker
dis_flag = 1
back_flag = 1
distance = 0
# i2c write flag
i2c_flag = 0
# Ultrasonic interface definition
Echo = 5  # Ultrasonic receiving pin
Trig = 6  # Ultrasonic transmitting pin
ultrasonic_flag = 0  # Ultrasonic obstacle avoidance mode switch flag

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
# The trig pin is set to output and initialized to low level
GPIO.setup(Trig, GPIO.OUT, initial=GPIO.HIGH)
time.sleep(0.5)
GPIO.output(Trig,GPIO.LOW)
# echo pin set as input
GPIO.setup(Echo, GPIO.IN, pull_up_down=GPIO.PUD_UP)
