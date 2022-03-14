import time
from machine import Pin
led1=Pin(3,Pin.OUT)
led2=Pin(4,Pin.OUT)
led3=Pin(5,Pin.OUT)#create LED object from pin2,Set Pin2 to output

while True:
  led1.value(1) 
  led2.value(1)#Set led turn on
  led3.value(1) 
  time.sleep(1)
  led1.value(0)
  led2.value(0)#Set led turn off
  led3.value(0) 
  time.sleep(1)
