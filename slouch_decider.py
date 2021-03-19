

def over_threshold(reading):
    if(abs(reading[0]) > 10 and abs(reading[1]) > -15):
        return True
    else:
        return False