#!/usr/bin/env python3

# Ecomet
from  ecomet_i2c_sensors.hdc1080 import hdc1080
from  ecomet_i2c_sensors.ms5637 import ms5637
from  ecomet_i2c_sensors.sn_gcja5 import sn_gcja5
from  ecomet_i2c_sensors.tsl2591 import tsl2591

# Configuration
import config

# Watchdog
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

# Opensensemap
import requests
import json
from time import sleep
import logging

logging.basicConfig(level=logging.INFO,  # change level looging to (INFO, DEBUG, ERROR)
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='opensensemap.log',
                    filemode='a')
console = logging.StreamHandler()
#console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
  
sens_hdc1080 = hdc1080.HDC1080()
sens_ms5637  = ms5637.MS5637()
sens_sn_gcja5 = sn_gcja5.SN_GCJA5()

def opensensemap(sensor_id, value):
    url = 'https://api.opensensemap.org/boxes/' + str(config.SENSEBOX_ID) + '/' + sensor_id
    data = {'value': value}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post(url, data=json.dumps(data), headers=headers)


(temp, hmdt, _) = sens_hdc1080.both_measurement()
(_, _, pressure, ret_ms5637) = sens_ms5637.measure (accuracy = 6) # ( temp_celsius, temp_fahrenheit, pressure, ret) 
(pm1_0, ret_pm1_0) = sens_sn_gcja5.read_register('PM1_0')
(pm2_5, ret_pm2_5) = sens_sn_gcja5.read_register('PM2_5')
(pm10, ret_pm10) = sens_sn_gcja5.read_register('PM10')

# Send data if SENSOR_ID is defined in config.py file
if config.SENSEBOX_SENSOR_ID_PRESSURE and ret_ms5637 == 0:
    opensensemap(config.SENSEBOX_SENSOR_ID_PRESSURE, round(pressure,3))
    sens_ms5637._logger.info('Sensor MS5637 data send ...')
if config.SENSEBOX_SENSOR_ID_TEMPERATURE :
    opensensemap(config.SENSEBOX_SENSOR_ID_TEMPERATURE, round(temp,3))
    sens_hdc1080._logger.info('Sensor HDC1080 temp data send ...')
if config.SENSEBOX_SENSOR_ID_HUMIDITY :
    opensensemap(config.SENSEBOX_SENSOR_ID_HUMIDITY, round(hmdt,3))
    sens_hdc1080._logger.info('Sensor HDC1080 humdt data send ...')
if config.SENSEBOX_SENSOR_ID_PM1_0 and ret_pm1_0 == 0:
    opensensemap(config.SENSEBOX_SENSOR_ID_PM1_0, round(pm1_0,3))
    sens_sn_gcja5._logger.info('Sensor SN_GCJA5 PM1.0 data send ...')
if config.SENSEBOX_SENSOR_ID_PM2_5 and ret_pm2_5 == 0:
    opensensemap(config.SENSEBOX_SENSOR_ID_PM2_5, round(pm2_5,3))
    sens_sn_gcja5._logger.info('Sensor SN_GCJA5 PM2.5 data send ...')
if config.SENSEBOX_SENSOR_ID_PM10 and ret_pm10 == 0:
    opensensemap(config.SENSEBOX_SENSOR_ID_PM10, round(pm10,3))
    sens_sn_gcja5._logger.info('Sensor SN_GCJA5 PM10 data send ...')

sleep(60)
sens_tsl2591 = tsl2591.TSL2591()
if sens_tsl2591._exit == -1 :
    sens_tsl2591._logger.info('Ambient light sensor skipped')
    exit(-1)
lux_average = round(sens_tsl2591.SelfCalibrate,3)
if config.SENSEBOX_SENSOR_ID_LIGHT :
    opensensemap(config.SENSEBOX_SENSOR_ID_LIGHT, round(lux_average,3))
    sens_tsl2591._logger.info('Sensor TSL2591 data send ...')
exit(0)
