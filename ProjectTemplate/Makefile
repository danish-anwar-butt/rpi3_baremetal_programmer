
ARMGNU ?= aarch64-none-elf

AOPS = --warn --fatal-warnings
COPS = -Wall -O2 -nostdlib -nostartfiles -ffreestanding 

gcc : kernel8.img

all : gcc

clean :
	rm -f *.o
	rm -f *.bin
	rm -f *.srec
	rm -f *.elf
	rm -f *.list
	rm -f *.img

vectors.o : vectors.s
	$(ARMGNU)-as $(AOPS) vectors.s -o vectors.o

main.o : main.c
	$(ARMGNU)-gcc $(COPS) -c main.c -o main.o

periph.o : periph.c 
	$(ARMGNU)-gcc $(COPS) -c periph.c -o periph.o

kernel8.img : memmap vectors.o periph.o main.o 
	$(ARMGNU)-ld vectors.o periph.o main.o -T memmap -o main.elf
	$(ARMGNU)-objdump -D main.elf > main.list
	$(ARMGNU)-objcopy --srec-forceS3 main.elf -O srec main.srec
	$(ARMGNU)-objcopy main.elf -O binary kernel8.img



