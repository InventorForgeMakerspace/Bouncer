#!/usr/bin/python3
#
#cron job that reboots our cable modem using a relay on a piface. LEDs sequence across the piface to indicate how
#many ping failures have occured before a reboot happens.
#
import subprocess as sp
import pifacedigitalio
from time import sleep
from slacker import Slacker
import configparser
config = configparser.ConfigParser()

slack = Slacker(config['slack.com']['token'])

pfd = pifacedigitalio.PiFaceDigital()

fails=0
maxfails=5
host = "8.8.8.8"

def ipcheck():
    status,result = sp.getstatusoutput("ping -c1 -w2 " + str(host))
    if status == 0:
        return 1
    else:
        print("System " + str(host) + " is DOWN ! ")
        return 0

def reboot():
   pfd.output_pins[0].value = 0
   pfd.output_pins[0].value = 1
   print("Rebooting...")
   sleep(5)
   pfd.output_pins[0].value = 0
   light_led(0)
   sleep(90)
   slack.chat.post_message('#tech_team', 'Ahhh! The cable modem is dead! I\'m gonna kick it')


def light_led(fail_count):
  MAX_LED_COUNT = 5
  for x in range(0, MAX_LED_COUNT):
    if fail_count - x > 0:
      # Turn On LEDs for fail
      pfd.output_pins[x +2].value = 1
      sleep(.1)

    else:
      # Turn on LED for blink start
      pfd.output_pins[x +2].value = 1
      sleep(.1)

      # Turn off LED for blink end
      pfd.output_pins[x +2].value = 0
      sleep(.1)



while True:
   maxattempts=30 #number of seconds between attempts
   attempts=0
   if ipcheck():
      pfd.output_pins[0].value = 0
      fails=0
   else:
      if fails > maxfails:
         fails=0
         reboot()
      else:
         fails +=1
   while attempts < maxattempts:
      light_led(fails)
      attempts +=1
