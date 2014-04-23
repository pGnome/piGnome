#!/usr/bin/env python
import time
import os
import RPi.GPIO as GPIO
import array
import globalVals

# create global variables
# half hour of seconds the frequency of water level reading when not pumping
MIN_30 = 1800 
# frequency when the pump is on
SEC_5 = 5


# values are 2 inches off - fix it!
ADJUST = 4.0

def pulse_clock( clk_pin ):
    GPIO.output(clk_pin, True)
    time.sleep( 0.000002 )     # wait 
    GPIO.output(clk_pin, False)

def read_adc( clk_pin, din_pin, cs_pin, dout_pin):
    GPIO.output(cs_pin, True)   # cs starts high
    GPIO.output(clk_pin, False) # clk starts low
    GPIO.output(cs_pin, False)  # bring cs down low

    # indicate to the MCP3008 that we only need to readee from channel 0
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


def readLevelCont():

    GPIO.setwarnings(False)

    # declare pin names
    CLK = 18
    DIN = 24
    CS = 21
    DOUT = 23
    
    # set pinout numbering convention
    GPIO.setmode(GPIO.BOARD)
    
    # set up input and output channels
    GPIO.setup(CLK, GPIO.OUT)
    GPIO.setup(DIN, GPIO.OUT)
    GPIO.setup(CS, GPIO.OUT)
    GPIO.setup(DOUT, GPIO.IN)
    
    BUFF_SIZE = 5
    
    d_level = CircBuffer(BUFF_SIZE)
   
   
    while True:
        
        n = read_adc(CLK, DIN, CS, DOUT)

#        print "Inserting: ", n
        # d_level: raw digital output of MCP3008
        d_level.insert( n )
        
        # a_level: analog water level
        a_level = ( d_level.average() / 1024.0 ) * 3.3
        
        print "Digital: ", d_level.average()
        
        print "Potential: ", a_level
        
        time.sleep(1)    # sleep for a sec

    
    return "DONE!"


def readLevel():
    
    GPIO.setwarnings(False)

    # declare pin names
    CLK = 18
    DIN = 24
    CS = 21
    DOUT = 23
    
    # max digital output of sensor
#    DOUT_MAX = 1024.0
    
    # VOLT_MAX is the max voltage that can be read across the sensor
#    VOLT_MAX = 3.3

    # set pinout numbering convention
    GPIO.setmode(GPIO.BOARD)
    
    # set up input and output channels
    GPIO.setup(CLK, GPIO.OUT)
    GPIO.setup(DIN, GPIO.OUT)
    GPIO.setup(CS, GPIO.OUT)
    GPIO.setup(DOUT, GPIO.IN)
    
    
    
    SAMPLE_SIZE = 5

    d_level = CircBuffer(SAMPLE_SIZE)
        
    runsum = 0

    for ii in range(0, SAMPLE_SIZE ):
        
        n = read_adc(CLK, DIN, CS, DOUT)

        time.sleep(0.5) 

        print "Inserting: ", n

        d_level.insert( n )
        

        #time.sleep(0.5)    # sleep for a milli sec

    raw = d_level.average()

    print "raw averate: ", raw

    level = depth2percent( resist2depth( voltage2resist( digit2analog( raw ) ) ) )

    if level > 0 and level < 100:
        globalVals.waterLevel = level

    level = -1

    return level
        

# digit2analog: the voltage is read in as an analog value between
# 0 and 1024 we need to convert that to an anolog value between 0 
# and the supply voltage
def digit2analog( d ):

    return (3.3 / 1024.0) * d * 2  # also the value is off by a factor of two don't know why


# voltage2resist: converts output voltage of sensor to the resistence
# in the sensor
#
#  VDD______
#      |
#     {Rr}
#      |____Vout  <--- voltage we are measuring
#      |
#     {Rs}   <--- variable resistence of our sensor
#      |
#  VDD_|____
#

def voltage2resist( Vout ):

    VDD = 3.3  # V
    Rr = 5.0  # kOhm
    
    return (Vout * Rr) / (VDD - Vout)

# resist2depth: converts resistence in the sensor to depth of water that the
# sensor is covered in.  The depth ranges from 0 to 32 inches, which correspondes with a resitence of 5 to 0.4 kOhms
def resist2depth( Rs ):


    return -(32.0 / 4.6) * Rs + (160 / 4.6) + ADJUST

# depth2percent: converts depth that the sensor is covered to percent
# the barrel is ful
def depth2percent( d ):

    maxHeight = 32.0 + ADJUST
    return (d / maxHeight) * 100
    

# read the water level and update the 'lastReadLevel'
def periodicReadLevel():
    
    
    while True: 
        # update the last level read
        # by reading the new level (voltage)
        # converting that voltage to resistence

        actualDepth = raw_input("Enter depth: ")
        runsum = 0

        for ii in range (1,3):
            globalVals.waterLevel = readLevel()
            print "                    waterLevel: ", globalVals.waterLevel
        
            runsum = runsum + globalVals.waterLevel
            print ii, ") depth: ", actualDepth, ", resist ave: ", runsum/ii

            # no we play the waiting game
            time.sleep( globalVals.waterLevelFreq )



# set the read frequency to the period
def set_levelReadFreq( period ):
    
    globalVals.levelReadFreq = period
