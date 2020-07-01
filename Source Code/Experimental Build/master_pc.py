#       .~~.   .~~.
#      '. \ ' ' / .'
#       .~ .~~~..~.
#      : .~.'~'.~. :
#     ~ (   ) (   ) ~
#    ( : '~'.~.'~' : )    WEATHER LOGGER V 0.0.1 - ALPHA
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
""" import board
import busio
import adafruit_dps310
import adafruit_dht """
import csv
import threading
import random
import logging
import math
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
from math import gamma

""" Initializers for the sensors.
i2c = busio.I2C(board.SCL, board.SDA)
dps310 = adafruit_dps310.DPS310(i2c)
dhtDevice = adafruit_dht.DHT22(board.D4) """

temperature_c_log = random.randint(25, 30)  # dhtDevice.temperature    |    random.randint(25, 30) 
temperature_f_log = temperature_c_log * (9 / 5) + 32   
humidity_log = random.randint(0, 99)        # dhtDevice.humidity       |   random.randint(0, 99)
pressure_log = random.randint(900, 1000)    # %dps310.pressure         |   random.randint(900, 1000)
altitude_log = 0
dew_log = random.randint(40, 60)
direction_log = 'SSE'
speed_log = random.randint(3, 15)
uv_log = random.randint(4, 6)

def sensor_emulator():
    
    while True:

        # Print the values to the console.
        "int.gamma = (17.62 * temperature_c_log /(243.12 + temperature_c_log)) + math.log(humidity_log / 100.0)"
        "int.dewpoint = (243.12 * gamma) / (17.62 - gamma)"

        print("Weather conditions at start: ")
        print("\nTemperature: %0.1f C" % temperature_f_log)
        print("Humidity: %0.1f %%" % humidity_log)
        print("Pressure: %0.1f hPa" % pressure_log)
        print("Altitude: %0.2f feet" % altitude_log)
        print("Dew Point: %0.2f C" % dew_log)
        print("Wind Heading: SSE")
        print("Wind Speed: %0.2f mph" % speed_log)
        print("UV Index: %0.2f" % uv_log)

        # Waits a second(s) before repeating.
        time.sleep(.1)

# NOTE: Classes, which were present in the previous version, have been replaced with simpler functions due to problems with accessing the needed variables outside of their
# local scope. These will be reintroduced during a future refactoring phase.

# FOR TESTING ONLY! Initializes a background thread for logging activities.
threading.Thread(target=sensor_emulator, name="Thread #1", daemon=True).start()

# Fetches the date and time for future file naming and data logging operations.
starttime=time.time()
now = datetime.now()

# Writes the header for the .csv file once.
with open('D:\\Weather Log ' + now.strftime("%Y-%m-%d") + '.csv', 'w', newline='') as f: # DO NOT EDIT THIS! ALLOWS FOR DAY-TIME FILE CREATION!
    fieldnames = ['Date', 'Time', 'Temperature (F)', 'Humidity (%)', 'Pressure (hPa)', 'Altitude (ft)', 'Dew Point (F)','Wind Heading', 'Wind Speed (mph)', 'UV Index']
    thewriter = csv.DictWriter(f, fieldnames=fieldnames)
    thewriter.writeheader()

# Fetches the date and time.
while True:
    
    now = datetime.now()
    
    # Writes incoming data to the .csv file.
    with open('D:\\Weather Log ' + now.strftime("%Y-%m-%d") + '.csv', 'a', newline='') as f: # DO NOT EDIT THIS! ALLOWS FOR DAY-TIME FILE CREATION!
        fieldnames = ['DATE', 'TIME', 'TEMP', 'HUMI', 'PRES', 'ALT', 'DEW', 'WIND', 'SPEED', 'UV'] 
        thewriter = csv.DictWriter(f, fieldnames=fieldnames)
        thewriter.writerow({'DATE' : now.strftime("%Y/%m/%d"),'TIME' : now.strftime("%I:%M:%S %p"), 'TEMP' : temperature_f_log, 'HUMI' : humidity_log, 'PRES' : pressure_log, 'ALT' : altitude_log, 'DEW' : dew_log, 'WIND' : direction_log, 'SPEED' : speed_log, 'UV' : uv_log})

    # Writes a message confirming the data's entry into the log, then sets a 10 second repeat cycle. For logging every half hour, change interval to 1800.
    print("New entry added at " + now.strftime("%I:%M:%S %p"))
    time.sleep(.1) # Repeat every second(s).
