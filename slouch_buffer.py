import time

#Set slice length variable, and initialise current time slice
SLICE_LENGTH = 20 #This is in seconds

#Gives the current time slice in terms of the seconds_since_epoch when it began
def sliced_time(slice_length):
    cur_time = int(time.time())
    time_into_slice = cur_time % slice_length
    cur_time -= time_into_slice
    return cur_time

class slouch_buffer:
    def __init__(self, slice_length_ms):
        self.slice_length = slice_length_ms / 1000
        self.time_slouching = 0.0
        self.cur_slice = sliced_time(self.slice_length)

    def update_buffer(self, slouching):
        new_slice = sliced_time(self.slice_length)
        if(new_slice != self.cur_slice):
            self.cur_slice = new_slice
            score = (1  - (self.time_slouching / self.slice_length)) * 100
            self.time_slouching = 0.0
            return score
        if slouching:
            print(str(self.time_slouching))
            self.time_slouching = self.time_slouching + 4
 