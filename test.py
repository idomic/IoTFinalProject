# this is just a template file! Imports have not been added yet,,

from range_sensor import *
from subprocess import call
import image_capture
import json
import requests
import servo 
from RPi import GPIO

GPIO.setmode(GPIO.BOARD)

FREQ1 = 50
FREQ2 = 50


def main():
    global FREQ1, FREQ2
    range_init()
    pwm1, pwm2 = servo.servo_init(FREQ1, FREQ2)
    while(1):
        try:
            dist = get_dist()
            print dist
            if dist < 100:
                call(['./take_pic.sh'])
                vect = image_capture.get_feature_vector('image.jpg')
                print vect
                clss = classify(vect)
                # Move laundry into correct bin
                print 'Moving laundry to ' + str(clss) + '\'s bin'
                servo.moveLaundry(clss, pwm1, pwm2)           
        except KeyboardInterrupt:
            GPIO.cleanup()


def classify(vect):
    url = 'http://34.210.106.90/test?msg=' + json.dumps([vect])
    response = requests.get(url)

    return response.text

# Call main()
main()
