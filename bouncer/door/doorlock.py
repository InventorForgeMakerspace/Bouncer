#!/usr/bin/python3
#
#Lock the door.
#
import ConfigParser
import logging
from logging import config as logconfig
import pifacedigitalio
from slacker import Slacker
import time

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('bouncer.ini')
    logconfig.fileConfig('bouncer.ini')
    pfd = pifacedigitalio.PiFaceDigital(init_board=False)

    slack = Slacker(config['slack.com']['token'])

    slack.chat.post_message('#door', 'The forge door is locked at ' +time.strftime("%H:%M:%S") +' CST' +'\n')
    logging.info("The door has been locked")
    pfd.relays[1].value = 0
