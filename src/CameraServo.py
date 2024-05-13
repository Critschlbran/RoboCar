import SMBus
from time import sleep

def GetAngle(anglenum_from_buffer):
    angle = hex(eval('0x' + anglenum_from_buffer))
    angle = int(angle, 16)  # convert value from hex to int?
    
    # Adjust angle protection
    if angle > 160:
        angle = 160
    elif angle < 15:
        angle = 15
    return angle

def SetServoAngle(servonum, angle):
    print('Setting the servoangle has been disabled.')
    # Call I2C to send the servo number and angle to the microcontroller
    # 0xFF 0x744 0x0160
    #data = (servonum << 8) + angle
    #print('Setting servo angle {}, {}'.format(servonum, angle))
    #SMBus.writeinstruction(data)

def StoreServoAngle():
    print('Storing Servo angle...')
    data = 0x1101
    SMBus.writeinstruction(data)
    sleep(0.1) 

def InitializeServo():
    # todo init servo to face front.
    # therefore: servonum 7, angle 95
    # servonum 8, angle 160 and format as in the SetServoAngle method n 
    print('Initializing Servo..')
    data = 0x1100
    SMBus.writeinstruction(data)
    
    sleep(0.1)

    print('Setting servo angle..')
    servonum = 7
    angle = 95
    data = (servonum << 8) + angle
    SMBus.writeinstruction(data)

    sleep(0.1)

    servonum = 8
    angle = 160
    data = (servonum << 8) + angle
    SMBus.writeinstruction(data)

    sleep(0.1)
