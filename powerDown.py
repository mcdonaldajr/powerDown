#!/usr/bin/python3
#
# Routine to be run at startup that triggers OS shutdown if power lost for more than safe period.
# Author: Anthony McDonald 2022
#
# add the following line to /etc/rc.local
# python /home/pi/powerDown/powerDown.py &
# or better still set up as a system service - see file powerDown.service
# You can view the system log file with the command "sudo tail /var/log/syslog" in the terminal.

import RPi.GPIO as GPIO
import time
import os
from datetime import datetime
import logging
import logging.handlers

PIN = 24 # GPIO Pin that goes low when power is lost
POWER_OUTAGE = 12 # How long to run on UPS before initiating shutdown (seconds)
FLUSH_TO_DISK = 3 # How long to wait before shutting down after OS sync instruction issued

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.IN)

# Create a logger object
logger = logging.getLogger('powerDown')
logger.setLevel(logging.INFO)

# Create a log handler that sends messages to the system log
syslog_handler = logging.handlers.SysLogHandler(address='/dev/log')

# Create a formatter for the log messages
formatter = logging.Formatter('%(name)s %(levelname)s %(message)s')

# Set the formatter for the handler
syslog_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(syslog_handler)

while True:
   # Wait for power to drop.
   logger.info("Waiting for power loss signal on GPIO "+str(PIN))
   GPIO.wait_for_edge(PIN, GPIO.FALLING)
   logger.info("Power loss occurred.")

   # Give user time to restore power.
   logger.info("Waiting to see if power is restored.")
   time.sleep(POWER_OUTAGE)

   if GPIO.input(PIN) == 0:
       logger.info("Power not restored. Saving data then shutting down.")
       os.system('sync')
       time.sleep(FLUSH_TO_DISK)
       os.system("sudo shutdown -h now")
       break;
   else:
       logger.info("Power restored.")
