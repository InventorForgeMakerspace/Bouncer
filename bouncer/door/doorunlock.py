#!/usr/bin/python3
#
#Unlock the door and report who did it to slack. This script requires the unifi_api.sh script
#from Ubiquiti. It acts as a sort of API for Unifi APs, but all we need is one or two web calls to
#get what we need.
#
import time
import pifacedigitalio
import sys
import subprocess


pfd = pifacedigitalio.PiFaceDigital(init_board=False)
from slacker import Slacker
log = open("/tmp/doorlog.txt", "a")
import configparser
config = configparser.ConfigParser()

slack = Slacker(config['slack.com']['token'])

if len(sys.argv) > 1:
   IP=str(sys.argv[1].replace(":",""))
   IP=IP.replace("f","")
   device = str(subprocess.check_output(['/usr/local/bin/unifi.sh', IP]))
else:
   device = "Bouncer"


pfd.relays[1].value = 1
log.write(time.strftime("%H:%M:%S") +" The door has been unlocked by " +device +" "+IP +'\n')
slack.chat.post_message('#door', 'The forge door is unlocked at ' +time.strftime("%H:%M:%S") +' CST by ' +device)
log.close()
