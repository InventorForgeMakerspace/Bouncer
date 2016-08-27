#!/usr/bin/python3
#
#script that looks for door open/close events and reports them to slack


from time import sleep
import time
import pifacedigitalio
pfd = pifacedigitalio.PiFaceDigital() # creates a PiFace Digtal object
listener = pifacedigitalio.InputEventListener(chip=pfd)
from slacker import Slacker


slack = Slacker('xoxb-************************************')


def doorclose(event):
   log = open("/tmp/doorlog.txt", "a")
   if pfd.input_pins[2].value:
      log.write(time.strftime("%H:%M:%S") +" door is closed" +'\n')
      slack.chat.post_message('#door', 'The forge door is closed at ' +time.strftime("%H:%M:%S") +' CST')
   else:
      log.write(time.strftime("%H:%M:%S") +" FALSE ALARM door is not really closed" +'\n')
      # We're picking up noise somewhere that is causing false alerts, so this reads the pin and 
      # looks for the expected logical value every time a rising/falling edge event occurs
   log.close()
   
def dooropen(event):
   log = open("/tmp/doorlog.txt", "a")
   if pfd.input_pins[2].value:
      log.write(time.strftime("%H:%M:%S") +" FALSE ALARM door open" +'\n')
   else:
      log.write(time.strftime("%H:%M:%S") +" door is open" +'\n')
      slack.chat.post_message('#door', 'The forge door is open at ' +time.strftime("%H:%M:%S") +' CST')
   log.close()

def doorholdopen(event):
   log = open("/tmp/doorlog.txt", "a")
   log.write(time.strftime("%H:%M:%S") +" door hold open" +'\n')
   pfd.relays[1].value = 1
   slack.chat.post_message('#door', 'The forge door has been manually held open at ' +time.strftime("%H:%M:%S") +' CST')
   pfd.leds[7].value = 1
  # This makes the LED indicator by the door flash, but it also suppresses door open/close alerts. HALP!
#   while pfd.input_pins[3].value:
#      pfd.leds[7].toggle()
#      sleep(.3)
   log.close()

def doorholdclose(event):
   log = open("/tmp/doorlog.txt", "a")
   log.write(time.strftime("%H:%M:%S") +" door hold close" +'\n')
   pfd.relays[1].value = 0
   pfd.leds[7].value = 0
   slack.chat.post_message('#door', 'The forge door has closed from being manually held open at ' +time.strftime("%H:%M:%S") +' CST')
   log.close()

listener.register(2, pifacedigitalio.IODIR_FALLING_EDGE, doorclose, settle_time=.3)
listener.register(2, pifacedigitalio.IODIR_RISING_EDGE, dooropen, settle_time=.3)
listener.register(3, pifacedigitalio.IODIR_FALLING_EDGE, doorholdopen, settle_time=.3)
listener.register(3, pifacedigitalio.IODIR_RISING_EDGE, doorholdclose, settle_time=.3)
listener.activate()
