class sensorReader:

    import time
    import board
    import busio
    import adafruit_dps310
    import adafruit_dht

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

        time.sleep(60)