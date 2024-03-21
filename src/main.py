import ControlConnection
import ImageStreamer
import CameraServo
import CarDriver
from threading import Thread
from signal import signal, SIGINT
from time import sleep
import net

shutdown = False

control_thread = Thread(target=ControlConnection.connect_and_run_remote_control, args=(), daemon=False)
driving_status_buffer_thread = Thread(target=ImageStreamer.run_status_buffering, args=(), daemon=False)
image_streaming_thread = Thread(target=ImageStreamer.intialize_and_start_streaming, args=(), daemon=False)
model = net.load_model()

def signal_handler(sig, frame):
    global shutdown
    CarDriver.Stop()
    #ImageStreamer.force_shutdown()
    #ControlConnection.force_shutdown()
    #control_thread.join()
    #driving_status_buffer_thread.join()
    #image_streaming_thread.join()
    shutdown = True
    

if __name__ == '__main__':        
    signal(SIGINT, signal_handler)
    CameraServo.InitializeServo()
    CarDriver.SetLeftSpeed(3)
    CarDriver.SetRightSpeed(3)
    
    #control_thread.start()
    #driving_status_buffer_thread.start()
    #image_streaming_thread.start()

    #while not shutdown:
    #    sleep(1)

    prev_pred = 'stop'
    while not shutdown:

        equal = False
        pred_1 = ''
        while not equal:
            pred_1 = net.predict(model)
            pred_2 = net.predict(model)
            equal = (pred_1 == pred_2)
            
        print('Prediction is ', pred_1)

        #if pred_1 == 'forwards':
        #    CarDriver.DriveForward()
        #    sleep(0.05)
        #elif pred_1 == 'right':
        #    CarDriver.TurnRight()
        #else:
        #    CarDriver.TurnLeft()
            
        #sleep(0.1)
        #CarDriver.Stop()
