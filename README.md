# rpi3_baremetal_programmer
This is a python utility python 3 code for uploading SREC file to raspberry pi 3 having @dwelch67 https://github.com/dwelch67/raspberrypi-three/tree/master/orig/withconfig/aarch64 files on SD card

Use following flow to get blink led on GPIO 21 of  Raspberry Pi 3:
1. Rename bootloader file https://github.com/dwelch67/raspberrypi-three/blob/master/orig/withconfig/aarch64/bootloader.img to kernal8.img 

2. Copy following files to SD Card:
  a. bootcode.bin
  b. start.elf
  c. config.txt
  d. kernal8.img

3. Update Port variable in the code (I'm trying to automate this process).
4. Upload your code using following command (notmain.srec is my firmware in case):
    python3 programmer.py notmain.srec
5. Reset RPI.
6. Done.
