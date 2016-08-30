#!/usr/bin/python3
#
#Lock the door.
#
import time
import pifacedigitalio

pfd = pifacedigitalio.PiFaceDigital(init_board=False)
from slacker import Slacker
log = open("/tmp/doorlog.txt", "a")
import configparser
config = configparser.ConfigParser()

slack = Slacker(config['slack.com']['token'])

slack.chat.post_message('#door', 'The forge door is locked at ' +time.strftime("%H:%M:%S") +' CST' +'\n')
log.write(time.strftime("%H:%M:%S") +" The door has been locked" +'\n')
pfd.relays[1].value = 0
log.close()
