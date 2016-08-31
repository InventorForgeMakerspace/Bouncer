#!/usr/bin/python3
#
#Script that checks the status of the manual override on the door lock
#and updates slack if the door is manually unlocked
#
import time
import pifacedigitalio
import ConfigParser
import logging
from logging import config as logconfig
import slacker

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('bouncer.ini')
    logconfig.fileConfig('bouncer.ini')

    slack = slacker.Slacker(config['slack.com']['token'])
    pfd = pifacedigitalio.PiFaceDigital(init_board=False)

    if pfd.input_pins[3].value:
       slack.chat.post_message('#door', 'The forge door is manually held open at ' +time.strftime("%H:%M:%S") +' CST. This alert will repeat in 30 minutes')
       logging.info("Door is held open")
    else:
       logging.info("Door is normal")

    if pfd.input_pins[2].value:
       logging.info("Door is open")
    else:
       logging.info("Door is closed")
