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
from datetime import datetime

""" Initializers for the sensors.
i2c = busio.I2C(board.SCL, board.SDA)
dps310 = adafruit_dps310.DPS310(i2c)
dhtDevice = adafruit_dht.DHT22(board.D4) """

def sensor_emulator():
    
    while True:

        # Print the values to the console.
        try:
            print("Weather conditions at start: ")
            pressure = random.randint(900, 1000)                    # %dps310.pressure         |   random.randint(900, 1000)
            print("Pressure = %.2f hPa" %pressure)
#            time.sleep(1)
            temperature_c = random.randint(25, 30)                  # dhtDevice.temperature    |    random.randint(25, 30) 
            temperature_f = temperature_c * (9 / 5) + 32
            humidity = random.randint(0, 99)                        # dhtDevice.humidity       |   random.randint(0, 99)
            print("Temp: {:.1f} F / {:.1f} C \nHumidity: {}% "
                .format(temperature_f, temperature_c, humidity))
            print("")
            return [float(temperature_c), float(temperature_f), float(humidity)]
            
        # Errors happen fairly often with DHT sensors, and will occasionally throw exceptions.
        except RuntimeError as error:
            print("n/a")
            print("")

        # Waits 10 seconds before repeating.
        time.sleep(10.0)

# NOTE: Classes, which were present in the previous version, have been replaced with simpler functions due to problems with accessing the needed variables outside of their
# local scope. These will be reintroduced during a future refactoring phase.

# FOR TESTING ONLY! Initializes a background thread for logging activities.
threading.Thread(target=sensor_emulator, name="Thread #1", daemon=True).start()

# Fetches the date and time for future file naming and data logging operations.
starttime=time.time()
now = datetime.now()

# Writes the header for the .csv file once.
with open('D:\\Weather Log.csv', 'w', newline='') as f:
    fieldnames = ['Date', 'Time', 'Temperature (F)', 'Humidity (%)', 'Pressure (hPa)']
    thewriter = csv.DictWriter(f, fieldnames=fieldnames)
    thewriter.writeheader()

# Fetches the date and time.
while True:
    
    now = datetime.now()

    temperature_c_log = random.randint(25, 30)  # dhtDevice.temperature    |    random.randint(25, 30) 
    temperature_f_log = temperature_c_log * (9 / 5) + 32   
    humidity_log = random.randint(0, 99)        # dhtDevice.humidity       |   random.randint(0, 99)
    pressure_log = random.randint(900, 1000)    # %dps310.pressure         |   random.randint(900, 1000)
    
    # Writes incoming data to the .csv file.
    with open('D:\\Weather Log.csv', 'a', newline='') as f: 
        fieldnames = ['DATE', 'TIME', 'TEMP', 'HUMI', 'PRES'] 
        thewriter = csv.DictWriter(f, fieldnames=fieldnames)
        thewriter.writerow({'DATE' : now.strftime("%Y/%m/%d"),'TIME' : now.strftime("%I:%M:%S %p"), 'TEMP' : temperature_f_log, 'HUMI' : humidity_log, 'PRES' : pressure_log})

    # Writes a message confirming the data's entry into the log, then sets a 10 second repeat cycle. For logging every half hour, change interval to 1800.
    print("New entry added at " + now.strftime("%I:%M:%S %p") + ": "+ str(temperature_f_log) + " F | " + str(humidity_log) + "% | " + str(pressure_log) + " hPa")
    time.sleep(10.0) # Repeat every ten seconds.
