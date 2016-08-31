#!/usr/bin/python3
#
#script that looks for door open/close events and reports them to slack


from time import sleep
import time
import pifacedigitalio
import slacker
import ConfigParser
import logging
from logging import config as logconfig

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('bouncer.ini')
    logconfig.fileConfig('bouncer.ini')

    slack = slacker.Slacker(config['slack.com']['token'])
    pfd = pifacedigitalio.PiFaceDigital()
    listener = pifacedigitalio.InputEventListener(chip=pfd)

    def doorclose(event):
       if pfd.input_pins[2].value:
          logging.info("Door is closed")
          slack.chat.post_message('#door', 'The forge door is closed at ' +time.strftime("%H:%M:%S") +' CST')
       else:
          logging.info("FALSE ALARM door is not really closed")
          # We're picking up noise somewhere that is causing false alerts, so this reads the pin and
          # looks for the expected logical value every time a rising/falling edge event occurs

    def dooropen(event):
       if pfd.input_pins[2].value:
          logging.info("FALSE ALARM door open")
       else:
          logging.info("Door is open")
          slack.chat.post_message('#door', 'The forge door is open at ' +time.strftime("%H:%M:%S") +' CST')

    def doorholdopen(event):
       logging.info("door held open")
       pfd.relays[1].value = 1
       slack.chat.post_message('#door', 'The forge door has been manually held open at ' +time.strftime("%H:%M:%S") +' CST')
       pfd.leds[7].value = 1
      # This makes the LED indicator by the door flash, but it also suppresses door open/close alerts. HALP!
    #   while pfd.input_pins[3].value:
    #      pfd.leds[7].toggle()
    #      sleep(.3)


    def doorholdclose(event):
       logging.info("door held close")
       pfd.relays[1].value = 0
       pfd.leds[7].value = 0
       slack.chat.post_message('#door', 'The forge door has closed from being manually held open at ' +time.strftime("%H:%M:%S") +' CST')

    listener.register(2, pifacedigitalio.IODIR_FALLING_EDGE, doorclose, settle_time=.3)
    listener.register(2, pifacedigitalio.IODIR_RISING_EDGE, dooropen, settle_time=.3)
    listener.register(3, pifacedigitalio.IODIR_FALLING_EDGE, doorholdopen, settle_time=.3)
    listener.register(3, pifacedigitalio.IODIR_RISING_EDGE, doorholdclose, settle_time=.3)
    listener.activate()
