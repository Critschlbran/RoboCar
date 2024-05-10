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
parser.add_argument('--stream_images', action=argparse.BooleanOptionalAction)
parser.add_argument('--self_driving_enabled', action=argparse.BooleanOptionalAction)

args = parser.parse_args()
self_driving_enabled = args.self_driving_enabled
stream_images = args.stream_images

stream_images = False if stream_images is None else stream_images
self_driving_enabled = False if self_driving_enabled is None else self_driving_enabled
print(f'Main Method startup. Provided arguments: enable_self_driving: {self_driving_enabled}, stream_images: {stream_images}')

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
    CarDriver.SetLeftSpeed(4)
    CarDriver.SetRightSpeed(4)
    
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
            
            sleep(0.05)
            CarDriver.Stop()
        CarDriver.Stop()
    else:
        
        if stream_images:
            driving_status_buffer_thread.start()
            image_streaming_thread.start()
        
        ControlConnection.connect_and_run_remote_control()
