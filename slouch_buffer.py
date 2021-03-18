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

def update_buffer():
    global cur_slice
    new_slice = sliced_time()
    if(new_slice != cur_slice):
        print "in dump bit"
        cur_slice = new_slice
        score = time_slouching / float(SLICE_LENGTH) * 100
        with open("./buffers/buffer", 'a') as buffer:
            buffer.write("0 " + str(sliced_time()) + "000 " + str(int(score)) + ": ")
    else:
        print "in else bit"
        global time_slouching
        print str(time_slouching)
        time_slouching = time_slouching + 4
 