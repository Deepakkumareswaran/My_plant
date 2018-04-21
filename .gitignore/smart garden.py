import Adafruit_DHT
import RPi.GPIO as GPIO
import time
from firebase import firebase
GPIO.setmode(GPIO.BCM)
motor = 20
motor1 = 26
firebase = firebase.FirebaseApplication('https://my-plant-2.firebaseio.com', None)
water_db = 'water'
hum_db = 'humidity'
temp_db = 'temperature'

def blink():
    for i in range(0,5,1):
        GPIO.output(motor, GPIO.HIGH)
        time.sleep(i)
        GPIO.output(motor, GPIO.LOW)
        time.sleep(i)


GPIO.setup(motor, GPIO.OUT)
GPIO.setup(motor1, GPIO.OUT) 
#PIO.output(motor, GPIO.HIGH)
#GPIO.output(motor1, GPIO.HIGH)
sensor=Adafruit_DHT.DHT11
channel = 21

GPIO.setup(channel, GPIO.IN)

gpio=17
while True:

    humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)
     
    
    if humidity is not None and temperature is not None:
      print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
      result = firebase.put('/',hum_db,{'hum': str(humidity)})
      result1 = firebase.put('/',temp_db,{'temp': str(temperature)})
      
    else:
      print('Failed to get reading. Try again!')
      
    if not GPIO.input(channel):	
		print"Detected water"
		output = firebase.put('/',water_db, {'water':'Wet'})
		GPIO.output(motor , GPIO.LOW)
		GPIO.output(motor1, GPIO.LOW)
    else:
                print"not detected"
		output = firebase.put('/', water_db, {'water':'Dry'})
		time.sleep(3)
		GPIO.output(motor , GPIO.HIGH)
		GPIO.output(motor1, GPIO.LOW)		
		time.sleep(3)
