#!/usr/bin/env python3

# Ecomet
from  ecomet_i2c_sensors.tsl2591 import tsl2591

# Configuration
import config

# Opensensemap
import requests
import json

from time import sleep
 
sens_tsl2591 = tsl2591.TSL2591()

lux_average = round(sens_tsl2591.SelfCalibrate,3)

print('Average Lux: (%s)',lux_average)

exit()
