from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import sys, os
import signal
import subprocess
import threading
import time
from subprocess import call
import servo
import RPi as GPIO

FREQ = 50
pwm1, pwm2, pwm3 = servo.servo_init(FREQ)

class ServerHandler(BaseHTTPRequestHandler):
    
    global pwm1, pwm2, pwm3

    def _set_headers(self, content_type="text/plain"):
        self.send_response(200)
        self.end_headers()

    def do_HEAD(self):
        self._set_headers()

    def do_GET(self):
        print("in do get")
        action = self.path.split("/")
        action = action[1]
        print("here is the action",action)
        if(action == "waterup"):
            servo.moveMotor(1,pwm1,pwm2,pwm3)
        elif(action == "phup"):
            servo.moveMotor(2,pwm1,pwm2,pwm3)
        elif (action == "phdown"):
            servo.moveMotor(3,pwm1,pwm2,pwm3)
        #print("here is self",self)
        self._set_headers()

    def do_POST(self):
        self._set_headers()
        paths = self.path.split("/")
        file_name = paths[1]
        if file_name == "small.txt" or file_name == "large.txt":
            src_content_len = int(self.headers.getheader('content-length', 0))
            src_body = self.rfile.read(src_content_len)
            thread1 = measureThread(src_body, self.client_address[0])
            #, self.server.server_address[0])
            thread1.start()

            with open(file_name, "rb") as f:
                dst_body = f.read()
                self.wfile.write(dst_body)
        print("response POST")

def main():
    #if len(sys.argv) < 3:
    #    print "usage: http_server.py ip out_dir"
    #    exit()
    #mac, ip, gateway = get_mac_address("enp3s0")
    subprocess.Popen("lt --port 80 --subdomain yuvaldoingiot", shell=True)
    time.sleep(3)
    subprocess.Popen("lt --port 8090 --subdomain idodoingiot", shell=True)
    time.sleep(3)
    print("Starting httpd...")
    httpd = HTTPServer(("localhost", 80), ServerHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        GPIO.cleanup()


if __name__ == "__main__":
    main()


