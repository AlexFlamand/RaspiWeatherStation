#       .~~.   .~~.
#      '. \ ' ' / .'
#       .~ .~~~..~.
#      : .~.'~'.~. :
#     ~ (   ) (   ) ~
#    ( : '~'.~.'~' : )    WEATHER LOGGER V 0.0.2 - ALPHA
#     ~ .~ (   ) ~. ~
#      (  : '~' :  ) 
#       '~ .~~~. ~'
#           '~'
#
# This Python script logs data from a Raspberry Pi 4 connected to a sensor array, and logs the information (along with time and date) to a CSV file once a minute.  
# It will serve as the foundation for a fully-independent IoT enabled weather station which will be mounted to a permanent fixture outdoors and feature a wider
# array of sensors, including a custom-built electronic wind vane and anemometer, ultraviolet indexer, and weatherproof camera.
# For now, it only has basic capability of taking readings of the local temperature, humidity, and atmospheric pressure, and logging it to a custom CSV file at 
# regular intervals. The list of sensors used follows:
#
# Adafruit AM2303 (wired variant of the DHT22) temperature and humidity sensor: [https://www.adafruit.com/product/393]
# Adafruit DPS310 precision barometer and altimeter: [https://www.adafruit.com/product/4494] 
# Adafruit SI1145 ultraviolet and visible light indexer (not active in this build): [https://www.adafruit.com/product/1777]
#
# You can also access .STL files for 3D printing hardware, KiCAD schematics for custom sensors, and additional scripts and documentation at the project's dedicated
# GitHub repository: [https://github.com/AlexFlamand/RaspiWeatherStation]

# Import necessary packages
import time
import math
import board
import busio
import adafruit_dps310
import adafruit_bme280
import csv
import threading
import random

from datetime import datetime
from math import gamma

# Initializers for the sensors.
i2c = busio.I2C(board.SCL, board.SDA)
# dps310 = adafruit_dps310.DPS310(i2c)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

def sensor_reader():
    
    while True:

    # Print the values to the console.
        int.gamma = (17.62 * bme280.temperature /(243.12 + bme280.temperature)) + math.log(bme280.humidity / 100.0)
        int.dewpoint = (243.12 * gamma) / (17.62 - gamma)

        print("Weather conditions at start: ")
        print("\nTemperature: %0.1f C" % bme280.temperature)
        print("Humidity: %0.1f %%" % bme280.humidity)
        print("Pressure: %0.1f hPa" % bme280.pressure)
        print("Altitude: %0.2f meters" % bme280.altitude)
        print("Dew Point: %0.2f C" % int.dewpoint)

    # Waits 10 seconds before repeating.
    time.sleep(10.0)

# NOTE: Classes, which were present in the previous version, have been replaced with simpler functions due to problems with accessing the needed variables outside of their
# local scope. These will be reintroduced during a future refactoring phase.

# Initializes a background thread for logging activities.
threading.Thread(target=sensor_reader, name="Thread #1", daemon=True).start()

# Fetches the date and time for future file naming and data logging operations.
starttime=time.time()
now = datetime.now()

# Writes the header for the .csv file once.
with open('D:\\Weather Log.csv', 'w', newline='') as f:
    fieldnames = ['Date', 'Time', 'Temperature (C)', 'Humidity (%)', 'Pressure (hPa)', 'Dew Point (C)']
    thewriter = csv.DictWriter(f, fieldnames=fieldnames)
    thewriter.writeheader()

# Fetches the date and time.
while True:
    
    now = datetime.now()

    bme280.temperature = int.temperature_c_log
    bme280.humidity =  int.humidity_log
    bme280.pressure = int.pressure_log

    str.temperature_f_log = int.temperature_c_log * (9 / 5) + 32   
    int.gamma = (17.62 * bme280.temperature /(243.12 + bme280.temperature)) + math.log(bme280.humidity / 100.0)
    int.dewpoint = (243.12 * gamma) / (17.62 - gamma)
    print(int.dewpoint)
        
    # Writes incoming data to the .csv file.
    with open('D:\\Weather Log.csv', 'a', newline='') as f: 
        fieldnames = ['DATE', 'TIME', 'TEMP', 'HUMI', 'PRES', 'DEW'] 
        thewriter = csv.DictWriter(f, fieldnames=fieldnames)
        thewriter.writerow({'DATE' : now.strftime("%Y/%m/%d"),'TIME' : now.strftime("%I:%M:%S %p"), 'TEMP' : int.temperature_c_log, 'HUMI' : int.humidity_log, 'PRES' : int.pressure_log, 'DEW' : int.dewpoint})

    # Writes a message confirming the data's entry into the log, then sets a 10 second repeat cycle. For logging every half hour, change interval to 1800.
    print("New entry added at " + now.strftime("%I:%M:%S %p"))
    time.sleep(10.0) # Repeat every ten seconds.
