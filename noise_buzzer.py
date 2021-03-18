#!/usr/bin/env python
#
# This library is for Grove - Buzzer(https://www.seeedstudio.com/Grove-Buzzer-p-768.html)
#
# This is the library for Grove Base Hat which used to connect grove sensors for raspberry pi.
#
# Author: Peter Yang <linsheng.yang@seeed.cc>
# Copyright (C) 2018  Seeed Technology Co.,Ltd.
#
# Author: Sarah Knepper <sarah.knepper@intel.com>
# Copyright (c) 2015 Intel Corporation.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
from __future__ import print_function
import time
from mraa import getGpioLookup
from upm import pyupm_buzzer as upmBuzzer
from grove.button import Button
import led_button 

#keep just to remember how to get different sounds
#chords = [upmBuzzer.BUZZER_DO, upmBuzzer.BUZZER_RE, upmBuzzer.BUZZER_MI,
#          upmBuzzer.BUZZER_FA, upmBuzzer.BUZZER_SOL, upmBuzzer.BUZZER_LA,
#          upmBuzzer.BUZZER_SI];

print(Button.EV_LONG_PRESS)
print(Button.EV_DOUBLE_CLICK)
print(Button.EV_SINGLE_CLICK)
print(Button.EV_LEVEL_CHANGED)
# slot/gpio number your device plugin
butt_pin = 5
press = led_button.GroveLedButton(butt_pin)
print("button = pin 5")
# the default behavior of led is
#   single click - on
#   double click - blink
#   long press   - off


#   PWM JST SLOT - PWM[12 13 VCC GND]
buzz_pin = 12
#
print("buzzer = pin 12")
# Create the buzzer object using RaspberryPi GPIO12
mraa_pin = getGpioLookup("GPIO%02d" % buzz_pin)
print("pin acquired: {}".format(mraa_pin))
buzzer = upmBuzzer.Buzzer(mraa_pin)
print("buzzer assigned")

# Print sensor name
print("buzzer is: {}".format(buzzer.name()))

#set led off
press.led.light(False)

# define a customized event handle for button (press.led controls led)
def cust_on_event(index, event, tm):
    print("event with code {}, time {}".format(event, tm))
    press.led.brightness = press.led.MAX_BRIGHT
    if event & Button.EV_SINGLE_CLICK:
        press.led.light(True)
        print("turn on  LED")
        print(buzzer.playSound(upmBuzzer.Buzzer_DO, 500000))
    elif event & Button.EV_DOUBLE_CLICK:
        press.led.blink()
        print(buzzer.playSound(upmBuzzer.Buzzer_DO, 250000))
        print("blink    LED")
    elif event & Button.EV_LONG_PRESS:
        press.led.light(False)
        print(buzzer.playSound(upmBuzzer.Buzzer_SI, 500000))
        print("turn off LED")


press.on_event = cust_on_event
print("custom event handler")

def main():
    from grove import helper
    from grove.helper import helper
    helper.root_check()

    while True:
        time.sleep(1)
	#print("time cycle")


    print("exiting application")

    # Delete the buzzer object
    del buzzer
    del press

if __name__ == '__main__':
    main()
