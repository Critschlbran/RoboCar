import CarDriver
import ImageStreamer
import CameraServo
import LightControl

from enum import Enum
from socket import socket, AF_INET, SOCK_STREAM, SHUT_RDWR

shutdown = False
server = socket(AF_INET, SOCK_STREAM)

class MessageCategories(Enum):
    LIGHT = 0x05
    LIGHT_LEFT = 0x01
    LIGHT_RIGHT = 0x02
    LIGHT_OFF = 0x0
    LIGHT_ON = 0x1
    DRIVE_COMMAND = 0x00
    DRIVE_COMMAND_STOP = 0x00
    DRIVE_COMMAND_FORWARD = 0x01
    DRIVE_COMMAND_BACKWARD = 0x02
    DRIVE_COMMAND_LEFT = 0x03
    DRIVE_COMMAND_RIGHT = 0x04
    SPEED_ADJUSTMENT = 0x02
    SPEED_ADJUSTMENT_LEFT = 0x01
    SPEED_ADJUSTMENT_RIGHT = 0x02
    SET_SERVO_ANGLE = 0x01
    STORE_SERVO_ANGLE = 0x32
    INITIALIZE_SERVO = 0x33

def execute_driving_command(command):
    if command == MessageCategories.DRIVE_COMMAND_STOP.value:
        CarDriver.Stop()
        ImageStreamer.current_driving_status = "stop"
    elif command == MessageCategories.DRIVE_COMMAND_FORWARD.value:
        CarDriver.DriveForward()
        ImageStreamer.current_driving_status = "forwards"
    elif command == MessageCategories.DRIVE_COMMAND_BACKWARD.value:
        CarDriver.DriveBackwards()
        ImageStreamer.current_driving_status = "backwards"
    elif command == MessageCategories.DRIVE_COMMAND_LEFT.value:
        CarDriver.TurnLeft()
        ImageStreamer.current_driving_status = "left"
    elif command == MessageCategories.DRIVE_COMMAND_RIGHT.value:
        CarDriver.TurnRight()
        ImageStreamer.current_driving_status = "right"
        
def execute_light_command(light_side, on_or_off):
    if light_side == MessageCategories.LIGHT_LEFT.value:
        if on_or_off == MessageCategories.LIGHT_ON:
            LightControl.LeftLightOn()
        elif on_or_off == MessageCategories.LIGHT_OFF.value:
            LightControl.LeftLightOff()
    elif light_side == MessageCategories.LIGHT_RIGHT.value:
        if on_or_off == MessageCategories.LIGHT_ON.value:
            LightControl.RightLightOn()
        elif on_or_off == MessageCategories.LIGHT_OFF.value:
            LightControl.RightLightOff()
        
def analyze_command(command):
    main_category = command[0]
    if main_category == MessageCategories.DRIVE_COMMAND.value:
        sub_category = command[1]
        execute_driving_command(sub_category)
    elif main_category == MessageCategories.SPEED_ADJUSTMENT.value:
        sub_category = command[1]
        # make sure that the speed is not 0
        new_speed_value = max(1, command[2])
        if sub_category == MessageCategories.SPEED_ADJUSTMENT_LEFT.value:
            CarDriver.SetLeftSpeed(new_speed_value)
        elif sub_category == MessageCategories.SPEED_ADJUSTMENT_RIGHT.value:
            CarDriver.SetRightSpeed(new_speed_value)
    elif main_category == MessageCategories.SET_SERVO_ANGLE.value:
        servonumber = command[1]
        servoangle = command[2]
        CameraServo.SetServoAngle(servonumber, servoangle)
    elif main_category == MessageCategories.STORE_SERVO_ANGLE.value:
        CameraServo.StoreServoAngle()
    elif main_category == MessageCategories.INITIALIZE_SERVO.value:
        CameraServo.InitializeServo()
    elif main_category == MessageCategories.LIGHT.value:
        light_side = command[1]
        light_on_or_off = command[2]
        execute_light_command(light_side, light_on_or_off)     
       
def connect_and_run_remote_control():
    global server
    
    # while not shutdown, try to create a new connection each time the old one is lost
    while not shutdown:
        print("Waiting for remote connection..") 
        client, address = server.accept()
        print("Connected to ", address[0])
        
        while not shutdown:
            try:
                data = client.recv(5) # receive 5 cahracters
                # if not enough data received, break and close the connection
                if len(data) < 5:
                    break
                
                # a valid command packet has to start and end with 0xFF
                if data[0] == 0xFF and data[len(data) - 1] == 0xFF:
                    # the middle three bytes contain the actual command. Analyze what has been sent
                    analyze_command(data[1:4])
            except Exception as exc:
                print("Error in reading from remote connection.")
                break
        print("Closing client connection")
        client.close()
        CarDriver.Stop()
    print("Closing server")
    server.close()
    
def force_shutdown():
    global shutdown
    shutdown = True
    server.shutdown(SHUT_RDWR)
    server.close()
    print("Closed control server.")