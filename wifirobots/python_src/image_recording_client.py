# Code from https://gist.github.com/kittinan/e7ecefddda5616eab2765fdb2affed1b

import cv2
import io
import socket
import struct
import time
import pickle
import zlib
import global_values
import drivingStatusKeeper

def run():
    print("Connecting to the servers...")
    global_values.image_streaming_socket.connect(('192.168.1.125', 2003))
    print("Established connection to the image server...")
    global_values.driving_status_socket.connect(('192.168.1.125', 2004))
    print("Established connection to the driving status server...")
    
    
    print("Established both connections to the server!")
    connection = global_values.image_streaming_socket.makefile('wb')

    cam = cv2.VideoCapture(0)

    cam.set(3, 320) # width
    cam.set(4, 240) # height
    
    img_counter = 0

    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

    print("Starting streaming...")
    while not global_values.shutdown:
        _, frame = cam.read()
        
        _, frame = cv2.imencode('.jpg', frame, encode_param)
        data = pickle.dumps(frame, 0)
        size = len(data)

        global_values.image_streaming_socket.sendall(struct.pack(">L", size) + data)

        #ack = conn.recv(1024).decode()
        #print("Received ack: ", ack)

        # wait for acknowledgement of the server that he is ready to receive the driving status
        global_values.driving_status_socket.recv(1024)


        msg = drivingStatusKeeper.get_driving_status().encode()
        global_values.driving_status_socket.sendall(msg)
        
        # wait for the server to acknowledge that he received the driving status
        global_values.driving_status_socket.recv(1024)
        
        

        #done = conn.recv(1024).decode()
        #print("Received done signal: ", done)

        img_counter += 1
        time.sleep(1/global_values.streaming_framerate)
    
    print("Shutting recording cam and servers down...")
    cam.release()
    global_values.driving_status_socket.close()
    global_values.image_streaming_socket.close()
    print("Successfully shut down camera and servers...")