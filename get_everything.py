# get_everything 2019-08-31
#
# for logging Raspberry Pi (RPi) and PC parameters
# reads the size of the Qtum blocks and stateQtum folders and additional parameters for the RPi
# prints comma delimited parameter strings to the console every minute.
#
# get the size of folder by walking a list of all files
# based on https://stackoverflow.com/questions/1392413/calculating-a-directorys-size-using-python
#
# Raspberry Pi parameters based on 
# https://learn.pimoroni.com/tutorial/networked-pi/raspberry-pi-system-stats-python
#
# copyright (C) 2019 Jackson Belove
#
# MIT license
#

'''
Replace the paths below 

For Raspberry Pi, default Qtum data directory files
blocksSizePath  = "/home/pi/.qtum/blocks"
stateQtumSizePath = "/home/pi/.qtum/stateQtum"

For Windows PC, default Qtum data directory files
blocksSizePath = "C:/Users/username/AppData/Roaming/Qtum/blocks"
stateQtumSizePath = "C:/Users/username/AppData/Roaming/Qtum/stateQtum"

For Ubuntu PC, default Qtum data directory files
blocksSizePath = "/home/username/.qtum/blocks"
stateQtumSizePath = "/home/username/.qtum/stateQtum"

'''

isRPi = False          # set True if on Raspberry Pi, set False otherwise
blocksSizePath = "C:/Users/Jack/AppData/Roaming/Qtum/blocks"
stateQtumPath = "C:/Users/Jack/AppData/Roaming/Qtum/stateQtum"

import os
import os.path
from os import path

if isRPi == True:
    import psutil
    from gpiozero import CPUTemperature
    
import time
import datetime

def get_size(start_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            time.sleep(0.01)     # not sure why
            if path.exists(fp):  # will get some nonexistant files
                # skip if it is symbolic link
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)
            
    return total_size

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

def main():
    
    if isRPi == True:
        print("time,minuteCount,blocks,stateQtum,total,CPU %,disk free,disk total,disk %,mem available,mem total,mem %,CPU temp")
    else:
        print("time,minuteCount,blocks,stateQtum,total")

    '''

    Raspberry Pi example, initial blockchain sync:
    
    time,minuteCount,blocks,stateQtum,total,CPU %,disk free,disk total,disk %,mem available,mem total,mem %,CPU temp
    01:06:16,0,0,0,0,30.0,19.2,26.7,24.0,3514.8,3906.0,10.0,56.965
    01:07:00,1,16777369,15040,16792409,17.5,19.2,26.7,24.0,3286.5,3906.0,15.9,57.452
    01:08:00,2,19294080,21626,19315706,30.3,19.2,26.7,24.1,3190.9,3906.0,18.3,49.173
    01:09:00,3,56386362,25992,56412354,28.3,19.2,26.7,24.2,3182.2,3906.0,18.5,47.712
    01:10:00,4,95575334,119247,95694581,26.0,19.1,26.7,24.4,3168.0,3906.0,18.9,43.816
    01:11:00,5,115917374,2913636,118831010,25.4,19.1,26.7,24.5,3155.8,3906.0,19.2,46.251

    PC example, initial blockchain sync:
    
    time,minuteCount,blocks,stateQtum,total
    05:05:27,0,0,0,0
    05:06:00,1,0,0,0
    05:07:00,2,16777316,15025,16792341
    05:08:00,3,16777316,15025,16792341
    05:09:00,4,16777316,15025,16792341
    05:10:00,5,16777316,15025,16792341    
    
    '''

    minuteCount = 0
    sizeBlocks = 0
    sizeStateQtum = 0
    sizeTotal = 0

    while True:

        unixTime = int(time.time())
        utcTime = datetime.datetime.utcfromtimestamp(unixTime)

        oldMinute = utcTime.minute   # save to detect new minute

        # get the folder sizes

        sizeBlocks = get_size(blocksSizePath)
        sizeStateQtum = get_size(stateQtumPath)
        sizeTotal = sizeBlocks + sizeStateQtum

        tempStr = format(utcTime.hour, "02.0f") + ":" + format(utcTime.minute, "02.0f") + ":" + format(utcTime.second, "02.0f") + "," + str(minuteCount) + "," + str(sizeBlocks) + "," + str(sizeStateQtum) + "," + str(sizeTotal)              

        if isRPi == True:    # additional parameters for RPi
        
            tempStr += "," + str(psutil.cpu_percent())

            disk = psutil.disk_usage('/')
            # Divide from Bytes -> KB -> MB -> GB
            free = round(disk.free/1024.0/1024.0/1024.0,1)
            total = round(disk.total/1024.0/1024.0/1024.0,1)
            # print("GB free ", str(total), "% ", str(disk.percent))
            tempStr += "," + str(free) + "," + str(total) + "," + str(disk.percent)

            memory = psutil.virtual_memory()
            # Divide from Bytes -> KB -> MB
            available = round(memory.available/1024.0/1024.0,1)
            total = round(memory.total/1024.0/1024.0,1)

            tempStr += "," + str(available) + "," + str(total) + "," + str(memory.percent)
            
            cpu = CPUTemperature()
            tempStr += "," + str(cpu.temperature)
            

        print(tempStr)

        while True:  # wait until the next minute

            unixTime = int(time.time())
            utcTime = datetime.datetime.utcfromtimestamp(unixTime)

            if utcTime.minute != oldMinute:   # found a new minute
                minuteCount += 1
                oldMinute = utcTime.minute
                break
            
            else:
                time.sleep(0.3)
            
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

if __name__ == '__main__':

    main()

    



      

                  


    
