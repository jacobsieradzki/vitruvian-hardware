import time

#Set slice length variable, and initialise current time slice
SLICE_LENGTH = 60 #This is in seconds

#Gives the current time slice in terms of the seconds_since_epoch when it began
def sliced_time():
    cur_time = int(time.time())
    time_into_slice = cur_time % SLICE_LENGTH
    cur_time -= time_into_slice
    return cur_time

cur_slice = sliced_time()
time_slouching = 0

def update_buffer(slouching):
    global cur_slice
    global time_slouching
    new_slice = sliced_time()
    if(new_slice != cur_slice):
        cur_slice = new_slice
        score = (SLICE_LENGTH - time_slouching) / float(SLICE_LENGTH) * 100
        return score
    if slouching:
        print(str(time_slouching))
        time_slouching = time_slouching + 4
        return False
    else:
        return False
 