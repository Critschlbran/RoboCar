import i2c
from time import sleep

current_driving_status = 'stop'

def Stop():
    print('Car stopping...')
    
    global current_driving_status
    current_driving_status = 'stop'
    
    value = 0x210A
    i2c.writeinstruction(value)

def DriveForward():
    print('Driving forwards...')
    
    global current_driving_status
    current_driving_status = 'forwards'
    
    value = 0x220A
    i2c.writeinstruction(value)

def DriveBackwards():
    print('Driving backwards...')
    
    global current_driving_status
    current_driving_status = 'backwards'
    
    value = 0x230A
    i2c.writeinstruction(value)

def TurnLeft():
    print('Turning left...')

    global current_driving_status
    current_driving_status = 'left'

    value = 0x240A
    i2c.writeinstruction(value)

def TurnRight():
    print('Turning right...')
    
    global current_driving_status
    current_driving_status = 'right'
    
    value = 0x250A
    i2c.writeinstruction(value)

def SetRightSpeed(speed):
    print(f'Right speed: {speed}')
    right_motor = 0x27
    right_speed = speed
    a = right_motor << 8
    right_value = a + right_speed
    print("Setting the speed for the right side: ", hex(right_value))
    i2c.writeinstruction(right_value)
    sleep(0.001)

def SetLeftSpeed(speed):
    print(f'Left speed: {speed}')
    left_motor = 0x26
    left_speed = speed
    a = left_motor << 8
    left_value = a + left_speed
    print("Setting the speed for the left side: ", hex(left_value))
    i2c.writeinstruction(left_value)
    sleep(0.001)