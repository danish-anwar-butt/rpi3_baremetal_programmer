#!/usr/bin/python
import argparse, errno, logging, os, platform, re, select, serial, subprocess, sys, time
from serial.tools import list_ports
VERSION = "1.0"
# Open a file
# hexfile_h = open("notmain.srec", "r+")
# firmware = hexfile_h.read()
# # print ("Read String is : ", firmware)
# print(len(firmware))
# # Close opend file
# hexfile_h.close()


def error(shortmsg, msg=""):
    print(shortmsg)
    sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This script sends a binary file to the Raspberry Pi bootloader. ")
    parser.add_argument('file', help="binary file to upload", type=argparse.FileType('rb'), nargs='?')
    args = parser.parse_args()
    
    stream = args.file
    if not args.file:   # if no file to send, report status of serial device and exit
        print('Please enter file name as an arguement')
        sys.exit(0)
    
    portname = '/dev/ttyUSB0'
    try:
        # timeout set at creation of Serial will be used as default for both read/write
        port = serial.Serial(port=portname, baudrate=115200, timeout=2, exclusive=True)

        # Opening the port seems to always pull DTR low, so go ahead
        # and perform complete reset sequence no matter what. If DTR
        # unconnected, behaves as no-op.
        print("Toggling DTR pin to reset Pi: low... ", end='')
        port.dtr = True  # Pull DTR pin low.
        time.sleep(0.2)  # Wait for Pi to reset.
        print("high. Waiting for Pi to boot... ", end='')
        port.dtr = False  # Pull DTR pin high.
        time.sleep(1)     # Wait for Pi to boot.
        print("Done.")
        
        print("Waiting for reset....")
        while True:
            data= port.read(100)
            data = data.decode()
            startup_msg = "SREC"
            
            if startup_msg in data:
                print(data, end='')
                break

        # Open a file
        # hexfile_h = open("notmain.srec", "r+")
        print("Sending '%s' (%d bytes) " % (stream.name, os.stat(stream.name).st_size))

        # Open a file
        hexfile_h = open(stream.name, "r+")
        firmware = hexfile_h.read()
        
        for i in range(len(firmware)):
            d = firmware[i]
            # print(d,end='')
            port.write(bytes(d,'ascii'))
        # # Close opend file
        hexfile_h.close()

        time.sleep(1)     # Wait for Pi to boot.
        
        port.write(bytes('g','ascii'))

    except (OSError, serial.serialutil.SerialException) as e:
        if e.errno in [errno.EBUSY, errno.EWOULDBLOCK]:
            error("The serial device `%s` is busy." % portname, """
        Do you have a `screen` or `rpi-run.py` currently active on that device?
            """)
        else:
            error("Unable to open serial device `%s`.\n%s." % (portname, str(e)))
