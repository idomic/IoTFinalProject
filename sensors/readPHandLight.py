#!/usr/bin/python
 
import spidev
import time
import os
 
# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=1000000
 
# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def ReadChannel(channel):
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data
 
# Function to convert data to voltage level,
# rounded to specified number of decimal places.
def ConvertVolts(data,places):
  volts = (data * 3.3) / float(1023)
  volts = round(volts,places)
  return volts

def readPH_and_light():
    ph_channel = 1
    light_channel = 0
    
    phValue = ReadChannel(ph_channel)
    phValue = phValue * 0.0137
    
    lightValue = ReadChannel(light_channel)
    lightValue = ConvertVolts(lightValue, 2)

    return lightValue, round(phValue,2)

if __name__ == "__main__":

    # Define sensor channels
    light_channel = 0
 
    # Define delay between readings
    delay = 2
    print("Start code\n")
    ph_channel = 1
    buf = [None] * 10 

    while True:
    # Get 10 sample value from the sensor for smooth the value
        print("channel reading: {}".format(ReadChannel(ph_channel)))
        avgValue = ReadChannel(ph_channel)
        phValue= float(avgValue*5.0/1024) #convert the analog into millivolt
        phValue = 3.5 * phValue             #convert the millivolt into pH value
        print("pH: {}".format(phValue))
    # Read the light sensor data
    #light_level = ReadChannel(light_channel)
    #print(light_level*0.0137)
    #light_volts = ConvertVolts(light_level,2)
 
    # Print out results
        print "--------------------------------------------"
    #print("Light: {} ({}V)".format(light_level,light_volts))
 
    # Wait before repeating loop
        time.sleep(delay)
