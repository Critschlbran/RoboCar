import time
import threading
import global_values

status_list = []

driving_status = 'stop'

# buffer the driving status for a certain amount of time (4 * 0.05 seconds)
# because the camera has a slight delay and this way we make sure that the driving status
# is in sync with the camera picture
def append_status():
    while not global_values.shutdown:
        if len(status_list) > 3:
            del status_list[0]
        status_list.append(driving_status)
        time.sleep(0.055) # figured it out trough trial and error
    print("Stop driving status buffer control...")
    
def get_driving_status():
    if len(status_list) > 0:
        return status_list[0]
    else:
        return 'stop'

