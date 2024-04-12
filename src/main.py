import ControlConnection
import ImageStreamer
import CameraServo
import CarDriver
from threading import Thread
from signal import signal, SIGINT
from time import sleep
import NeuralNet

shutdown = False

driving_status_buffer_thread = Thread(target=ImageStreamer.run_status_buffering, args=(), daemon=False)
image_streaming_thread = Thread(target=ImageStreamer.intialize_and_start_streaming, args=(), daemon=False)

self_driving_enabled = False
if self_driving_enabled:
    NeuralNet.initialize_camera()
    NeuralNet.load_model()

def signal_handler(sig, frame):
    CarDriver.Stop()
    
    global shutdown
    shutdown = True

    if not self_driving_enabled:
        ImageStreamer.force_shutdown()
        ControlConnection.force_shutdown()
        driving_status_buffer_thread.join()
        image_streaming_thread.join()

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
        driving_status_buffer_thread.start()
        image_streaming_thread.start()
        ControlConnection.connect_and_run_remote_control()