import i2c

def LeftLightOn():
    print("Turning left light on...")
    value = 0x3601
    i2c.writeinstruction(value)

def LeftLightOff():
    print("Turning left light off...")
    value = 0x3600
    i2c.writeinstruction(value)

def RightLightOn():
    print("Turning right light on...")
    value = 0x3701
    i2c.writeinstruction(value)

def RightLightOff():
    print("Turning right light off...")
    value = 0x3700
    i2c.writeinstruction(value)