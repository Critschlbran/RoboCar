import i2c
import time

class MotorControl(object):
    @staticmethod
    def Stop():
        print('Car stopping...')
        value = 0x210A
        i2c.writeinstruction(value)
        print('i2c write 0x210A')
        i2c.writeinstruction(value)

    @staticmethod
    def DriveForward():
        print('Driving forwards...')
        value = 0x220A
        i2c.writeinstruction(value)
        print('i2c write 0x220A')

    @staticmethod
    def DriveBackwards():
        print('Driving backwards...')
        value = 0x230A
        i2c.writeinstruction(value)
        print('i2c write 0x230A')

    @staticmethod
    def TurnLeft():
        print('carleft run...')
        value = 0x240A
        i2c.writeinstruction(value)
        print('i2c write 0x240A')

    @staticmethod
    def TurnRight():
        print('carright run...')
        value = 0x250A
        i2c.writeinstruction(value)
        print('i2c write 0x250A')

    @staticmethod
    def SetRightSpeed(speed):
        right_motor = 0x27
        right_speed = speed
        a = right_motor << 8
        right_value = a + right_speed
        print(hex(right_value))
        i2c.writeinstruction(right_value)
        time.sleep(0.001)

    @staticmethod
    def SetLeftSpeed(speed):
        left_motor = 0x26
        left_speed = speed
        a = left_motor << 8
        left_value = a + left_speed
        print(hex(left_value))
        i2c.writeinstruction(left_value)
        time.sleep(0.001)

class LightControl(object):
    @staticmethod
    def LeftLightOn():
        value = 0x3601
        i2c.writeinstruction(value)

    @staticmethod
    def LeftLightOff():
        value = 0x3600
        i2c.writeinstruction(value)

    @staticmethod
    def RightLightOn():
        value = 0x3701
        i2c.writeinstruction(value)

    @staticmethod
    def RightLightOff():
        value = 0x3700
        i2c.writeinstruction(value)

class ServoControl(object):
    def GetAngle(anglenum_from_buffer):
        angle = hex(eval('0x' + angelnum_from_buffer))
        angle = int(angle, 16)  # 16为进制
        # 设置角度保护
        if angle > 160:
            angle = 160
        elif angle < 15:
            angle = 15
        return angle

    def SetServoAngle(servonum, angle):
        # 调用I2C发送舵机号和角度给单片机
        # 0xFF 0x744 0x0160
        data = (servonum << 8) + angle
        i2c.writeinstruction(data)

    def StoreServoAngle():
        data = 0x1101
        i2c.writeinstruction(data)
        print('Storing Servo angle...')
        time.sleep(0.1) 

    def InitializeServo():
        data = 0x1100
        i2c.writeinstruction(data)
        print('Initializing Servo..')
        time.sleep(0.1)