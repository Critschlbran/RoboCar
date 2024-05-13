import SMBus

def LeftLightOn():
    print("Turning left light on...")
    value = 0x3601
    SMBus.writeinstruction(value)

def LeftLightOff():
    print("Turning left light off...")
    value = 0x3600
    SMBus.writeinstruction(value)

def RightLightOn():
    print("Turning right light on...")
    value = 0x3701
    SMBus.writeinstruction(value)

def RightLightOff():
    print("Turning right light off...")
    value = 0x3700
    SMBus.writeinstruction(value)
