#!/usr/bin/env python
import water_levelRead_new 
import globalVals

globalVals.init()

water_levelRead_new.readLevel()

print globalVals.waterLevel
