#!/usr/bin/python
import argparse, errno, logging, os, platform, re, select, serial, subprocess, sys, time
from serial.tools import list_ports
VERSION = "1.0"

def error(shortmsg, msg=""):
    print(shortmsg)
    sys.exit(1)


if __name__ == "__main__": 
    portname = '/dev/ttyUSB1'
    try:
        # timeout set at creation of Serial will be used as default for both read/write
        port = serial.Serial(port=portname, baudrate=115200, timeout=2, exclusive=True)

        # Opening the port seems to always pull DTR low, so go ahead
        # and perform complete reset sequence no matter what. If DTR
        # unconnected, behaves as no-op.
        while True:
            print("Toggling DTR pin to reset Pi: low... ", end='')
            port.dtr = True  # Pull DTR pin low.
            time.sleep(0.5)  # Wait for Pi to reset.
            print("high. Waiting for Pi to boot... ", end='')
            port.dtr = False  # Pull DTR pin high.
            time.sleep(0.5)     # Wait for Pi to boot.
            print("Done.")
    

    except (OSError, serial.serialutil.SerialException) as e:
        if e.errno in [errno.EBUSY, errno.EWOULDBLOCK]:
            error("The serial device `%s` is busy." % portname, """
        Do you have a `screen` or `rpi-run.py` currently active on that device?
            """)
        else:
            error("Unable to open serial device `%s`.\n%s." % (portname, str(e)))
