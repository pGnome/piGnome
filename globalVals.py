#all the global variables
def init():
	#global variable that tracks pump state
    global pumpOn
    pumpOn = True

    #True, if manual override scheduling is on
    #False, otherwise
    global manual
    manual = False

    global watering_duration
    watering_duration = 1.0;

    # last updated water level
    # initialized to -1, if the value is -1 it means that it has
    # not yet read the value from the pump
    global waterLevel
    waterLevel = -1
    
    # time that the water level was last updated
    global waterLevelTime
    waterLevelTime = -1
    
    # period at which the water level is checked in seconds
    global waterLevelFreq
    waterLevelFreq = 5

    #Water level threshold
    global waterLevelThreshold
    waterLevelThreshold = 17

    #indicator weather text message has sent
    global isSent
    isSent = False

