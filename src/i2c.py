# coding:utf-8
"""
@version: python3.7
@Author  : hbwz
@Explain :I2C Communication with microcontroller
@contact :
@Time    :2020/05/09
@File    :hbwz_i2c.py
@Software: PyCharm
"""

import smbus
import time, os
import traceback

# create smbus instance
bus = smbus.SMBus(1)  # 0 represents /dev/i2c0  1 represents /dev/i2c1
# I2C communication address
address = 0x18

bus_occupied = 0

# write command to i2c address
def writeinstruction(values):
    # print('writeinstruction run...')
    try:
        bus.write_word_data(address, 0xff, values)
        time.sleep(0.01)
    except IOError:
        print('Write Error')
        os.system('sudo i2cdetect -y 1')


# read data from i2c address
def readinstruction():
    s = traceback.extract_stack()
    print(s[-2][2])
    # infrared patrol line
    while(bus_occupied):
        pass
    bus_occupied=1
    if s[-2][2] == 'ir_trackline':  # Determine who is calling the readinstruction method
        try:
            # Send infrared reading command 0x32
            value = bus.read_word_data(address, 0x32)  # Return value: 0x00 0x01 0x10 0x11 one of the four
            bus_occupied=0
            # Return to infrared status command
            return value
        except IOError:
            print('Write Error')
            os.system('sudo i2cdetect -y 1')

    elif s[-2][2] == 'get_distence':  # Determine who is calling the readinstruction method
        try:
            value = bus.read_word_data(address, 0x31)
            bus_occupied = 0
            time.sleep(0.02)
            print('value:', value)
            if value == 0xFF:
                information = 'ultrasound error!'
            elif value == 254:
                information = 'Beyond the measuring distance!'
            else:
                return value
        except IOError:
            print('Write Error')
            os.system('sudo i2cdetect -y 1')

    elif s[-2][2] == 'get_ldrintensity':
        try:
            led_lists = []
            instruction = [0x33, 0x34, 0x35]
            for i in instruction:
                value = bus.read_word_data(0x18, i)
                led_lists.append(value)
                time.sleep(0.015)
            bus_occupied=0
            return led_lists
        except IOError:
            print('Write Error')
            os.system('sudo i2cdetect -y 1')

