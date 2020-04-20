import time
import board
import busio
import adafruit_dps310
import adafruit_dht
import csv
import threading
import datetime
# import random


class sensorReader:

    # Initializers for the sensors.
    i2c = busio.I2C(board.SCL, board.SDA)
    dps310 = adafruit_dps310.DPS310(i2c)
    dhtDevice = adafruit_dht.DHT22(board.D4)

    while True:

        # Print the values to the console.
        try:
            print("Pressure = %.2f hPa"%dps310.pressure)
            temperature_c = dhtDevice.temperature
            temperature_f = temperature_c * (9 / 5) + 32
            humidity = dhtDevice.humidity
            print("Temp: {:.1f} F / {:.1f} C \nHumidity: {}% "
                .format(temperature_f, temperature_c, humidity))
            print("")
            
        # Errors happen fairly often with DHT sensors, and will occasionally throw exceptions.
        except RuntimeError as error:
            print("n/a")
            print("")

        # Waits 60 seconds before repeating.
        time.sleep(60)


class csvWriter:

    # Fetches the date and time for future file naming and data logging operations.
    starttime=time.time()
    x = datetime.datetime.now()

    # Writes the header for the .csv file once.
    with open('Weather Log %s.csv' % x, 'w', newline='') as f:
        fieldnames = ['Time', 'Temperature (F)', 'Humidity (%)', 'Pressure (hPa)']
        thewriter = csv.DictWriter(f, fieldnames=fieldnames)
        thewriter.writeheader()

    # Fetches the date and time.
    while True: 
        from datetime import datetime
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        # When the below lines are uncommented, the console simulates data output from the sensors. Used to test csvWriter class.
        # temp = random.randint(0,125)       
        # humi = random.randint(0,100)       
        # pres = random.randint(900,1000)    
        
        temp = temperature_f
        humi = dhtDevice.humidity
        pres = dps310.pressure
        
        # Writes incoming data to the .csv file.
        with open('Weather Log %s.csv', 'a', newline='') as f: 
            fieldnames = ['TIME', 'TEMP', 'HUMI', 'PRES'] 
            thewriter = csv.DictWriter(f, fieldnames=fieldnames)
            thewriter.writerow({'TIME' : current_time, 'TEMP' : temp, 'HUMI' : humi, 'PRES' : pres})
    
        # Writes a message confirming the data's entry into the log, then sets a 60 second repeat cycle.
        print("New entry added.")
        time.sleep(60.0 - ((time.time() - starttime) % 60.0)) # Repeat every ten seconds.
