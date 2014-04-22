import RPi.GPIO as GPIO
import sqlite3
import time
import threading
import serial
#python modules for pGnome
import db
import pump
import globalVals

#connect to the local database#
myDatabase = sqlite3.connect("myDBfile.sqlite3", check_same_thread=False)

#GPIO settings#

#PINOUT NUMBER#
pumpOut = 15
zone1 = 11
zone2 = 12
zone3 = 13
gpio_pins = [pumpOut,zone1,zone2,zone3]


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
#pump GPIO pin
GPIO.setup(pumpOut, GPIO.OUT, initial=GPIO.LOW)
#zone GPIO pins
GPIO.setup(zone1, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(zone2, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(zone3, GPIO.OUT, initial=GPIO.HIGH)



def intervalExecute(interval, func, *args, **argd):
    ''' @param interval: execute func(*args, **argd) each interval
        @return: a callable object to enable you terminate the timer.
    '''
    cancelled = threading.Event()
    def threadProc(*args, **argd):
        while True:
            if args[0] == 4:
                if globalVals.manual == True:
                    cancelled.wait(globalVals.watering_duration)
                elif globalVals.pumpOn == False:
                    cancelled.wait(30.0)
                elif globalVals.pumpOn == True:
                    cancelled.wait(interval)
            else:
                cancelled.wait(interval)
	    if cancelled.isSet():
                break
            func(*args, **argd) #: could be a lenthy operation
    th = threading.Thread(target=threadProc, args=args, kwargs=argd)
    th.start()
    def close(block=True, timeout=3):
        ''' @param block: if True, block the caller until the thread 
                          is closed or time out
            @param timout: if blocked, timeout is used
            @return: if block, True -> close successfully; False -> timeout
                     if non block, always return False
        '''
        if not block:
            cancelled.set()
            return False
        else:
            cancelled.set()
            th.join(timeout)
            isClosed = not th.isAlive()
            return isClosed
    return close

if __name__=='__main__':
    
    cur = myDatabase.cursor()
    db.init_tables()
    myDatabase.commit()
    globalVals.init()

    data_Collect = intervalExecute(1.0, db.data_collect, 1, 'data_collect')
    moisture_Setting = intervalExecute(1.0, db.moisture_setting, 2, 'moisture_setting')
    sync_DB = intervalExecute(30.0, db.update_remote_db, 3, 'update_remote_db')
    pump_Trigger = intervalExecute(5.0, pump.pump_sig, 4, gpio_pins)
    water_Level = intervalExecute(30.0, db.data_water_collect, 5, 'data_water_collect')
    
    #print cancellObj() #: cancel the intervalExecute timer.
    #print 'after calling close'
    myDatabase.commit()
    myDatabase.close()
