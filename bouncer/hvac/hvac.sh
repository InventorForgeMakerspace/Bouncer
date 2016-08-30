#!/bin/bash
#
#cron job that looks for people in the space and sets the thermostat accordingly
#this requires unifi_api.sh until we extract out the web calls we need

. /usr/local/bin/unifi_api.sh
unifi_login >/dev/null
if unifi_list_sta  |sed 's/{/\n/g' |sed '/^\s*$/d' |grep -qv 'ForgeTV\|Gateway\|octopi\|Chromecast'; then
	echo "people in the forge, resetting timer"
	/usr/local/bin/thermostat.py -c 77
else
	echo "no one's home"
	/usr/local/bin/thermostat.py -x
fi
