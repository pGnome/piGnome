#!/usr/bin/env python
import time
import os
import RPi.GPIO as GPIO
import array

def pulse_clock( clk_pin ):
    GPIO.output(clk_pin, True)
    time.sleep( 0.000002 )     # wait 
    GPIO.output(clk_pin, False)

def read_adc( clk_pin, din_pin, cs_pin, dout_pin):
    GPIO.output(cs_pin, True)   # cs starts high
    GPIO.output(clk_pin, False) # clk starts low
    GPIO.output(cs_pin, False)  # bring cs down low

    # indicate to the MCP3008 that we only need to read from channel 0
    # by pulsing b11000 through the CS pin
    ch0 = 0x02
    for ii in range(5):
        
        if(ch0 & 0x01): #if this is an actual number we have hit a bit we should pulse high
            GPIO.output(din_pin, True)

        else: 
            GPIO.output(din_pin, False)

        ch0 >>= 1
        # pulse the clock
        pulse_clock( clk_pin )

    # adc_read: 10 bit digital output of ADC
    adc_read = 0
    # read in 1 empty bit, 10 acd bits then 1 null bit 
    for ii in range(12):
        
        # pulse clock
        pulse_clock( clk_pin )
        
        adc_read <<=1     # shift adc so that we can change the next bit if needed
        if (GPIO.input(dout_pin)):
            adc_read |= 0x01


    GPIO.output(cs_pin, True)

    # drop null bit
    adc_read >>= 1

    return adc_read


# define circ_buffer used to keep a running mean of the last SIZE values
class CircBuffer:

   
    def __init__(self, size):
        self.size = size
        self.data = [0] * self.size  # create list of size SIZE
        self.last_changed = 0  # index of data last changed

    # insert: insert value val into buffer and make any necessary changes
    def insert(self, val): 
        self.data[ self.last_changed ] = val
        
        self.last_changed = (self.last_changed + 1) % self.size

    # returns average of the buffer
    def average(self):
        runsum = 0
        
        for ii in range(self.size):
            runsum = runsum + self.data[ii]
        
        return runsum * 1.0 / self.size


GPIO.setwarnings(False)

# declare pin names
CLK = 18
DIN = 24
CS = 25
DOUT = 23

# set pinout numbering convention
GPIO.setmode(GPIO.BCM)

# set up input and output channels
GPIO.setup(CLK, GPIO.OUT)
GPIO.setup(DIN, GPIO.OUT)
GPIO.setup(CS, GPIO.OUT)
GPIO.setup(DOUT, GPIO.IN)

BUFF_SIZE = 5

d_level = CircBuffer(BUFF_SIZE)


while True:


    # d_level: raw digital output of MCP3008
    d_level.insert( read_adc(CLK, DIN, CS, DOUT) )
    
    # a_level: analog water level
    a_level = ( d_level.average() / 1024.0 ) * 3.3

    print "Digital: ", d_level.average()

    print "Potential: ", a_level

    time.sleep(1)    # sleep for a sec

    