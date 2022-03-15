from umqtt.simple import MQTTClient
from machine import Pin,Timer
import machine
import ubinascii
import time
import network
import json
dictn={}
led0 = Pin(16, Pin.OUT)
led1 = Pin(5, Pin.OUT)
led2 = Pin(4, Pin.OUT)
led3 = Pin(0, Pin.OUT)
led4 = Pin(14, Pin.OUT)
led5 = Pin(12, Pin.OUT)
led6 = Pin(13, Pin.OUT)
led7 = Pin(15, Pin.OUT)

#wifi crendentials
ssid = "SKP"
password = "02062001@"

#connects to the wifi network
sta = network.WLAN(network.STA_IF)
if not sta.isconnected():
    print('connecting to network...')
    sta.active(True)
    sta.connect(ssid,password)
    while not sta.isconnected():
        pass
print('network config:', sta.ifconfig())
#Mac Address of the chip
macaddress= ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
print(macaddress)
#configuration to connect to the mqtt broker
CONFIG = {
     "MQTT_BROKER": "14.97.22.54",
     "USER": "admin",
     "PASSWORD": "password",
     "PORT": 1883, 
     "PUBTOPIC": b"esppub",
     "SUBTOPIC": b"espsub",   
}


#Act based on received command & publish status of respective LED
def onMessage(topic, msg):
    print("Topic: %s, Message: %s" % (topic, msg))
   
    #take the json message and convert into dictionary
    print(type(msg))
    while True:
        try:
            msgjsn=json.loads(msg)
            for i in msgjsn.items():
                for j in range(len(lst)):
                    if '1' in i and lst[j] in i:
                        gpiolist[j].on()
                        dictn[lst[j]]='1'
                        #if led 1 is on then after 5s led 2 will be off
                        if led1.value() == 1:
                            time.sleep(5)
                            led1.off()
                            dictn[lst[j]]='0'
                        
                        
                        elif led2.value() == 1 and led6.value() == 1:
                            time.sleep(5)
                            led6.off()
                            dictn[lst[j]]='0' 


                    elif '0' in i and lst[j] in i:
                        gpiolist[j].off()
                        dictn[lst[j]]='0'
           
                    
                 
#dictionary is converted to json data             
            message=json.dumps(dictn)
            client.publish(CONFIG["SUBTOPIC"],message)
            break
#If there is invalid json syntax is entered then exception raised and take another input of valid json syntax           
        except :
            print("Error Raised Invalid Json...")
            print("Please enter valid json format")

            break
            
            

def Listen():
    #instance of MQTTClient
    
    client.set_callback(onMessage)
    client.subscribe(CONFIG["PUBTOPIC"])
    print("ESP8266 is Connected to %s and subscribed to %s topic" % (CONFIG['MQTT_BROKER'], CONFIG["PUBTOPIC"]))
   

    try:
        while True:
            #msg = client.wait_msg()
            msg = (client.check_msg())
          
          
          
    finally:
            client.disconnect()

#Connecting to the mqtt broker
client = MQTTClient(macaddress, CONFIG['MQTT_BROKER'], user=CONFIG['USER'], password=CONFIG['PASSWORD'], port=CONFIG['PORT'])
client.connect()
PUB_MSG="ESP8266 is Connected and it's mac address is: %s"%macaddress
client.publish(CONFIG["SUBTOPIC"], PUB_MSG)

#Lists
lst=['L0','L1','L2','L3','L4','L5','L6','L7']
gpiolist =[led0, led1, led2, led3, led4, led5, led6, led7]


#publish initial state data
for j in range(0,8):
    if gpiolist[j].value() == 1:
        dictn[lst[j]]='1'
    if gpiolist[j].value() == 0:
        dictn[lst[j]]='0'
#after completing the loop the initial data is stored in dictionary and it is converted to json data to publish       
message=json.dumps(dictn)
client.publish(CONFIG["SUBTOPIC"], message)


Listen() 
