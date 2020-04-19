class csvWriter:
  
    import csv
    import threading
    import time
    import random

    starttime=time.time() 

    with open('mycsv.csv', 'w', newline='') as f:
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