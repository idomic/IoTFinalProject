import readPHandLight as analog_read
import AdafruitDHT as temp_humid
import requests
import time
import RPi as GPIO
import servo

#GPIO.setmode(GPIO.BOARD)

#FREQ = 50

#print(analog_read.readPH_and_light())
#print(temp_humid.readTempandHumid())

def getValues():
    ph, light = analog_read.readPH_and_light()
    temp, humid = temp_humid.readTempandHumid()
    print(ph, light, temp, humid)

    return temp, humid, light, ph

def sendRequest(temp, humid, light, ph):
    url = 'http://18.208.31.46:8080/api/setSensorData'
    r = requests.post(url, data = {'temperature':temp, 'humidity':humid, 'lighting':light, 'ph':ph})

    return r.text


if __name__ == "__main__":
    
    #global FREQ
    #pwm1, pwm2, pwm3 = servo.servo_init(FREQ)

    while(1):
        try:
            temp, humid, light, ph = getValues()
            #servo.moveMotor(2,pwm1,pwm2,pwm3)
            print(sendRequest(temp,humid,light,ph))
            time.sleep(5)
        except KeyboardInterrupt:
            GPIO.cleanup()

