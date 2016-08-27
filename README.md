# Bouncer
Raspberry Pi wifi door control scripts

We use a raspberry pi attached to a piface to control a magnetic lock at the Forge.  Members come to the space, join the members wireless network and then access a node.js page from their phone that causes these scripts to fire.  The scripts talk to our Ubiquiti access point to determine what device is inside the space and to write alerts into slack regarding the status of the door, who unlocked it, etc. 
