import time

#Set slice length variable, and initialise current time slice
SLICE_LENGTH = 60 #This is in seconds

#Gives the current time slice in terms of the seconds_since_epoch when it began
def sliced_time():
    cur_time = int(time.time())
    time_into_slice = cur_time % slice_length
    cur_time -= time_into_slice
    return cur_time

cur_slice = sliced_time()
time_slouching = 0

