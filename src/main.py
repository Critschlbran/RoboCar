import ControlConnection
import ImageStreamer
import CameraServo
import CarDriver
from threading import Thread
from signal import signal, SIGINT
from time import sleep
import NeuralNet
import argparse
import sys

# argument parser
parser = argparse.ArgumentParser()
parser.add_argument('--stream_images', type=bool, default=False, nargs='?')
parser.add_argument('--self_driving_enabled', type=bool, default=False, nargs='?')

args = parser.parse_args()
self_driving_enabled = args.self_driving_enabled
stream_images = args.stream_images

# thread and termination setup
shutdown = False
driving_status_buffer_thread = Thread(target=ImageStreamer.run_status_buffering, args=(), daemon=False)
image_streaming_thread = Thread(target=ImageStreamer.intialize_and_start_streaming, args=(), daemon=False)


if self_driving_enabled:
    NeuralNet.Initialize(stream_images)

def signal_handler(sig, frame):
    CarDriver.Stop()
    
    global shutdown
    shutdown = True

    if not self_driving_enabled:
        if stream_images:
            ImageStreamer.force_shutdown()
            image_streaming_thread.join()
            driving_status_buffer_thread.join()
        ControlConnection.force_shutdown()

if __name__ == '__main__':        
    signal(SIGINT, signal_handler)
    
    CameraServo.InitializeServo()
    CarDriver.SetLeftSpeed(3)
    CarDriver.SetRightSpeed(3)
    
    if self_driving_enabled:
        while not shutdown:

            prediction = NeuralNet.predict()
                
            print(f'Prediction is: {prediction}')

            if prediction == 'forwards':
                CarDriver.DriveForward()
            elif prediction == 'right':
                CarDriver.TurnRight()
            else:
                CarDriver.TurnLeft()
            
            sleep(0.075)
            CarDriver.Stop()
    else:
        
        if stream_images:
            driving_status_buffer_thread.start()
            image_streaming_thread.start()
        
        ControlConnection.connect_and_run_remote_control()