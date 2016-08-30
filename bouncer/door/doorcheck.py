#!/usr/bin/python3
#
#Script that checks the status of the manual override on the door lock
#and updates slack if the door is manually unlocked
#
from time import sleep
import time
import pifacedigitalio
pfd = pifacedigitalio.PiFaceDigital(init_board=False) # creates a PiFace Digtal object
log = open("/tmp/doorlog.txt", "a")
from slacker import Slacker
import configparser
config = configparser.ConfigParser()
config.read('../../bouncer.ini')

slack = Slacker(config['slack.com']['token'])


if pfd.input_pins[3].value:
   slack.chat.post_message('#door', 'The forge door is manually held open at ' +time.strftime("%H:%M:%S") +' CST. This alert will repeat in 30 minutes')
   log.write(time.strftime("%H:%M:%S") +" Door is held open\n")
else:
   log.write(time.strftime("%H:%M:%S") +" Door is normal\n")

if pfd.input_pins[2].value:
   log.write(time.strftime("%H:%M:%S") +" Door is open\n")
else:
   log.write(time.strftime("%H:%M:%S") +" Door is closed\n")
log.close()
