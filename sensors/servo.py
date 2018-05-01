import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BOARD)

def servo_init(freq=50):
    GPIO.setup(03, GPIO.OUT)
    GPIO.setup(05, GPIO.OUT)
    GPIO.setup(07, GPIO.OUT)

    # GPIO.PWM(<pin>,<freq>)
    pwm1=GPIO.PWM(03,freq)
    pwm2=GPIO.PWM(05,freq)
    pwm3=GPIO.PWM(07,freq)

    pwm1.start(0)
    pwm2.start(0)
    pwm3.start(0)

    setAngle(90,pwm3)
    setAngle(90,pwm2)
    setAngle(90,pwm1)

    return pwm1, pwm2, pwm3

def moveMotor(clss, pwm1, pwm2, pwm3):
    if clss == 0:
        setAngle(120, pwm1)
    elif clss == 1:
        setAngle(120, pwm2)
    elif clss == 2:
        setAngle(120, pwm3)

    # Reset postion
    sleep(1)
    setAngle(90, pwm1)
    setAngle(90, pwm2)
    setAngle(90, pwm3)

def setAngle(angle,pwm):
    duty = angle / 18 + 2
    GPIO.output(03,True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(03, False)
    pwm.ChangeDutyCycle(0)

def reset_servo():
    pwm1, pwm2, pwm3 = servo_init()

    setAngle(90,pwm2)
    setAngle(90,pwm1)
    setAngle(90,pwm3)
    
    sleep(1)

    setAngle(120,pwm1)
    setAngle(120,pwm2)
    setAngle(120,pwm3)


if __name__ == '__main__':
    reset_servo()
