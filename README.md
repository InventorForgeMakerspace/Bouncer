# Bouncer
Raspberry Pi wifi door control and HVAC control scripts

We use a raspberry pi attached to a piface to control a magnetic lock at the Forge.  Members come to the space, join the members wireless network and then access a node.js page from their phone that causes these scripts to fire.  The scripts talk to our Ubiquiti access point to determine what device is inside the space and to write alerts into slack regarding the status of the door, who unlocked it, etc. 

## How to Build

1. Use `make` to install dependencies. You may need to prepend `sudo -H`, depending on your system's configuration.

```sh
make init
```
2. Use `make` to run tests.

```sh
make test
```

## License

Copyright (C) 2016 Inventor Forge Makerspace

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

