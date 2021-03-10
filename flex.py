#adapted from seeed wiki for grove slide potentiometer

import math
import sys
import time
#analogue to digital converter
from grove.adc import ADC

#has a specific channel and can read adc value from it
class GroveFlex(ADC):
    def __init__(self, channel):
        self.channel = channel
        self.adc = ADC()

    @property
    def value(self):
        return self.adc.read(self.channel)


Grove = GroveFlex


def main():
    #error handling
    if len(sys.argv) < 2:
        print('Usage: {} adc_channel'.format(sys.argv[0]))
        sys.exit(1)

    #data reading
    sensor = GroveFlex(int(sys.argv[1]))
    while True:
        print('Flex sensor VD value: {}'.format(sensor.value))
        time.sleep(.2)


if __name__ == '__main__':
    main()
