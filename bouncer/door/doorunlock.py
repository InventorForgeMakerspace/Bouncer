#!/usr/bin/python3
#
#Unlock the door and report who did it to slack. This script requires the unifi_api.sh script
#from Ubiquiti. It acts as a sort of API for Unifi APs, but all we need is one or two web calls to
#get what we need.
#
import ConfigParser
import time
import logging
from logging import config as logconfig
import pifacedigitalio
import sys
from slacker import Slacker
import subprocess

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('bouncer.ini')
    logconfig.fileConfig('bouncer.ini')

    pfd = pifacedigitalio.PiFaceDigital(init_board=False)
    slack = Slacker(config['slack.com']['token'])

    if len(sys.argv) > 1:
       IP=str(sys.argv[1].replace(":",""))
       IP=IP.replace("f","")
       device = str(subprocess.check_output(['/usr/local/bin/unifi.sh', IP]))
    else:
       device = "Bouncer"


    pfd.relays[1].value = 1
    logger.info("The door has been unlocked by " +device +" "+IP)
    slack.chat.post_message('#door', 'The forge door is unlocked at ' +time.strftime("%H:%M:%S") +' CST by ' +device)
