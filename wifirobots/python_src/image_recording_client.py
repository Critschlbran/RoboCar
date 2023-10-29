# Code from https://gist.github.com/kittinan/e7ecefddda5616eab2765fdb2affed1b

import cv2
import io
import socket
import struct
import time
import pickle
import zlib
import global_values

def run():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ack_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ack_socket.bind(('', 2004))
    client_socket.connect(('192.168.1.125', 2003))
    #print("Connected to server!")
    connection = client_socket.makefile('wb')

    ack_socket.listen(10)
    #print("Acknowledgement socket now listening.")
    conn, addr = ack_socket.accept()


    cam = cv2.VideoCapture(0)

    cam.set(3, 320 * 2);
    cam.set(4, 240 * 2);
    
    img_counter = 0

    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

    print("Start recording")
    while True:
        ret, frame = cam.read()
        result, frame = cv2.imencode('.jpg', frame, encode_param)
    #    data = zlib.compress(pickle.dumps(frame, 0))
        data = pickle.dumps(frame, 0)
        size = len(data)


        #print("{}: {}".format(img_counter, size))
        client_socket.sendall(struct.pack(">L", size) + data)

        ack = conn.recv(1024).decode()
        #print("Received ack: ", ack)

        msg = global_values.driving_status.encode()
        conn.sendall(msg)

        img_counter += 1
        time.sleep(1/global_values.recording_framerate)
    

    cam.release()
    ack_socket.close()
    client_socket.close()