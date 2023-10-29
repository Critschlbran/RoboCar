# coding:utf-8
"""
@version: python3.7
@Author  : hbwz
@Explain :socket通信、指令解析
@contact :
@Time    :2020/05/09
@File    :hbwz_global.py
@Software: PyCharm
"""

from socket import *
import time
import binascii
import main_car_control as car
import global_values
import i2c
import image_recording_client
import threading


class Socket:
    def __init__(self):
        self.rec_flag = 0  # 0xff字节接收标志
        self.count = 0  # 数据接收计数器标志
        self.buffer = []

    def RunServer(self):
        while True:
            print(print('waitting for %s connection...' % "TCP", "\r"))

            global_values.TCP_Client = False
            global_values.TCP_Client, socket_addr = global_values.TCP_Server.accept()
            client = global_values.TCP_Client
            print((str(socket_addr[0]) + ' %s Connected!'), "\r")

            recording_thread = threading.Thread(target=image_recording_client.run, args=(), daemon=True)
            recording_thread.start()
            print("Started recording images.")

            while True:
                try:
                    data = global_values.TCP_Client.recv(global_values.recv_len)
                    if len(data) < global_values.recv_len:
                        break
                    if data[0] == 0xff and data[len(data) - 1] == 0xff:
                        buffer = []
                        for i in range(1, 4):
                            buffer.append(data[i])
                        self.command_analysis(buffer)

                except Exception as e:  # 接收出错
                    print('socket received error:', e)  # 打印出错信息
                    break

            client.close()
            car.MotorControl.Stop()
        print("closing server")
        global_values.TCP_Server.close()

    # Analyze the incoming data and perform the requested action
    # such as driving forwards, turning the lights on etc.
    def command_analysis(self, lists):
        # 判断小车方向电机指令      FF  XX   XX   XX   FF
        if lists[0] == 0x00:  # 包头 功能  状态  数据 包尾
            if lists[1] == 0x00:
                global_values.driving_status = 'stop'
                print('Stop,command send...')
                car.MotorControl.Stop()
            elif lists[1] == 0x01:
                #global_values.back_flag = 1
                if global_values.dis_flag == 1:
                    print('DriveForward,command send...')
                    global_values.driving_status = 'forward'
                    car.MotorControl.DriveForward()
            elif lists[1] == 0x02:
                print('DriveBackwards,command send...')
                if global_values.cruising_flag == 3:
                    global_values.cruising_flag = 0
                global_values.driving_status = 'backward'
                car.MotorControl.DriveBackwards()
            elif lists[1] == 0x03:
                print('TurnLeft,command send...')
                if global_values.cruising_flag == 3:
                    global_values.cruising_flag = 0
                global_values.driving_status = 'left'
                car.MotorControl.TurnLeft()
            elif lists[1] == 0x04:
                print('TurnRight,command send...')
                if global_values.cruising_flag == 3:
                    global_values.cruising_flag = 0
                global_values.driving_status = 'right'
                car.MotorControl.TurnRight()

        # 判断是否为调速指令
        elif lists[0] == 0x02:
            # 不存在0档调速，如果是0档调速那么置位1
            if lists[2] == 0x00:
                lists[2] = 0x01
            if lists[1] == 0x01:
                speed = lists[2]
                # 此处调用左侧调速函数
                car.MotorControl.SetLeftSpeed(speed)
            elif lists[1] == 0x02:
                speed = lists[2]
                # 此处此处调用右侧调速函数
                car.MotorControl.SetRightSpeed(speed)

        # 判断是否为舵机控制指令
        elif lists[0] == 0x01:
            servernum = lists[1]
            severangle = lists[2]
            # 加入防抖并过滤重复角度
            if abs(global_values.before_angle[servernum - 1] - severangle) > 2:
                print('severangle:%s' % severangle)
                car.ServoControl.SetServoAngle(servernum, severangle)
                global_values.before_angle[servernum - 1] = severangle

        # 存储舵机角度
        elif lists[0] == 0x32:
            car.ServoControl.StoreServoAngle()

        # 舵机角度初始化
        elif lists[0] == 0x33:
            car.ServoControl.InitializeServo()

        # 判断功能模式
        elif lists[0] == 0x13:
            # 判断是否为红外巡线模式
            if lists[1] == 0x02:
                global_values.cruising_flag = 1
                print('进入红外巡线模式:%d' % global_values.cruising_flag)
            # 判断是否为超声波模式
            elif lists[1] == 0x04:
                # 进入超声波测速前，调整速度
                speed_lists = [0x2606, 0x2706]
                for i in speed_lists:
                    i2c.writeinstruction(i)
                # 开启超声波测速标志
                global_values.ultrasonic_flag = 1
                # 控制台打印测试
                print('进入超声波避障模式:%d' % global_values.cruising_flag)
            # 判断是否为寻光模式
            elif lists[1] == 0x06:
                global_values.cruising_flag = 3
                print('进入寻光模式:%d' % global_values.cruising_flag)
            elif lists[1] == 0x00:
                global_values.revstatus = 0
                # 更改cruising_mod中的标志位
                global_values.cruising_flag = 0
                # 进入正常模式前关闭超声波避障
                global_values.ultrasonic_flag = 0
                # 再次确保避障方向位置位1，否则无法前进
                global_values.dis_flag = 1
                # 恢复最大速度值
                speed_lists = [0x260A, 0x270A]
                for i in speed_lists:
                    i2c.writeinstruction(i)
                # 控制台打印测试
                print('进入正常模式:%d' % global_values.cruising_flag)
        # 判断是否开关大灯模式
        elif lists[0] == 0x05:
            # 判断是否控制左侧大灯
            if lists[1] == 0x01:
                if lists[2] == 0x00:
                    print(lists)
                    print('left light turn off command send...')
                    car.LightControl.LeftLightOff()
                    print('3600')
                elif lists[2] == 0x01:
                    print(lists)
                    print('left light turn on command send...')
                    car.LightControl.LeftLightOn()
                    print('3601')
            # 判断是否控制右侧侧大灯
            elif lists[1] == 0x02:
                if lists[2] == 0x00:
                    print(lists)
                    print('right light turn off command send...')
                    car.LightControl.RightLightOff()
                    print('3700')
                elif lists[2] == 0x01:
                    print(lists)
                    print('right light turn on command send...')
                    car.LightControl.RightLightOn()
                    print('3701')
