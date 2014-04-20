#!/usr/bin/env python
import water_levelRead 
import globalVals

globalVals.init()

water_levelRead.periodicReadLevel()

print globalVals.waterLevel
