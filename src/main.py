import ControlConnection
import ImageStreamer
from threading import Thread
from signal import signal, SIGINT
from time import sleep

shutdown = False

control_thread = Thread(target=ControlConnection.connect_and_run_remote_control, args=(), daemon=False)
driving_status_buffer_thread = Thread(target=ImageStreamer.run_status_buffering, args=(), daemon=False)
image_streaming_thread = Thread(target=ImageStreamer.intialize_and_start_streaming, args=(), daemon=False)

def signal_handler(sig, frame):
    global shutdown
    ImageStreamer.force_shutdown()
    ControlConnection.force_shutdown()
    control_thread.join()
    driving_status_buffer_thread.join()
    image_streaming_thread.join()
    shutdown = True

if __name__ == '__main__':        
    signal(SIGINT, signal_handler)

    control_thread.start()
    driving_status_buffer_thread.start()
    image_streaming_thread.start()


    while not shutdown:
        sleep(0.1)
