import time
import board
import busio
import adafruit_dps310
import adafruit_dht
import csv
import threading
import random
import datetime


class sensorReader:

    #initializers
    i2c = busio.I2C(board.SCL, board.SDA)
    dps310 = adafruit_dps310.DPS310(i2c)
    dhtDevice = adafruit_dht.DHT22(board.D4)

    while True:

        try:
            # Print the values to the serial port
            print("Pressure = %.2f hPa"%dps310.pressure)
            time.sleep(1)
            temperature_c = dhtDevice.temperature
            temperature_f = temperature_c * (9 / 5) + 32
            humidity = dhtDevice.humidity
            print("Temp: {:.1f} F / {:.1f} C \nHumidity: {}% "
                .format(temperature_f, temperature_c, humidity))
            print("")

        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            print("n/a")
            print("")

        time.sleep(30)


class csvWriter:

    starttime=time.time()
    x = datetime.datetime.now()

    with open('Weather Log %s.csv' % x, 'w', newline='') as f:
        fieldnames = ['Time', 'Temperature (F)', 'Humidity (%)', 'Pressure (hPa)']
        thewriter = csv.DictWriter(f, fieldnames=fieldnames)
        thewriter.writeheader()

    while True: 
        from datetime import datetime
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        temp = random.randint(0,125) 
        humi = random.randint(0,100) 
        pres = random.randint(900,1000)

        with open('mycsv.csv', 'a', newline='') as f:
            fieldnames = ['TIME', 'TEMP', 'HUMI', 'PRES']
            thewriter = csv.DictWriter(f, fieldnames=fieldnames)
            thewriter.writerow({'TIME' : current_time, 'TEMP' : temp, 'HUMI' : humi, 'PRES' : pres})
    
        print("New entry added.")
        time.sleep(10.0 - ((time.time() - starttime) % 10.0))
