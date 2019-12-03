# CamJam wall follower

This repository contains the code for a simple wall following robot.

To use the code simply transfer it to the robot and install the ``gpiozero`` library using pip.

Additionally the code is made for Python 3.5+

## Commands
The robot can be communicated with using commands, which requires that the IP is set in the code. The following commands are available (sent over TCP on port 8080):

- ``start`` - Starts the robot. If the distance is not set this will attempt to set the distance
- ``stop`` - Stops the robot
- ``getdist`` - Gets the current distance from the distance sensor
- ``getmotors`` - Gets the current motor speed
- ``reset`` - Resets the distance to the wall to the current distance
- ``scan`` - Scans the surroundings for a wall/the shortest distance and saves that as the distance to keep

(All commands are case sensitive)