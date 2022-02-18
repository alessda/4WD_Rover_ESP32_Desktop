# robot car
# Created at 2020-04-09 15:46:51.374016

import streams
import pin #import pin setup
import func #import functions 
import hcsr04 #import driver hc-sr04
from wireless import wifi # import the wifi interface
from mqtt import mqtt # import MQTT library
from espressif.esp32net import esp32wifi as wifi_driver # import wifi support

status = 'off'
mode = 'manual'
command = 'stop'
flag_connectivity = 0  

streams.serial()
wifi_driver.auto_init()
front = hcsr04.hcsr04(pin.trigger, pin.echo)  #frontal ultrasonic sensor object
back = hcsr04.hcsr04(pin.trigger_back, pin.echo_back) #behind ultrasonic sensor object

def wifi_connect(): #wifi connection
    print("Establishing wifi Link...")
    try:
        wifi.link("D-Apice WiFi",wifi.WIFI_WPA2,"1998Cristal2008!")
        print("wifi Link Established")
    except Exception as e:
        print("ooops, something wrong while linking :-(", e)
        global flag_connectivity
        flag_connectivity = 2
        while True:
            sleep(1000)
            
# callback function for printing data received from MQTT messages
def print_sample(client,data):
     message = data['message']
     print("sample received: ", message.payload)
     
# function for publishing obj on the topic
def send_sample(topic, obj, qos):
    print("publishing: ", obj, "on topic", topic, "with QoS", qos)
    client.publish(str(topic), str(obj), qos)

def print_connectOK(client):
    print("connected to MQTT server :-).")

# function for recived messages
def print_messageREC(client, data):
    message = data['message']
    #print("topic: ", message.topic)
    #print("payload received: ", message.payload)
    if message.payload == 'on' or message.payload == 'off' or message.payload == 'stop':
        global status
        status = message.payload
    if message.payload == 'automatic' or message.payload == 'manual':
        global mode
        mode = message.payload
    if message.payload == 'go' or message.payload == 'back' or message.payload == 'left' or message.payload == 'right':
        global command
        command = message.payload
        
try:
    wifi_connect()
    # set the mqtt id to "MQTT_smart_car"
    client = mqtt.Client("MQTT_smart_car",True)
    # and try to connect to "test.mosquitto.org"
    for retry in range(5):
        try:
            #client.connect("test.mosquitto.org",60)
            client.connect("test.mosquitto.org", 60, aconnect_cb=print_connectOK)
            global flag_connectivity
            flag_connectivity = 1
            break
        except Exception as e:
            print(e)
            print("re-connecting...", retry)
            global flag_connectivity
            flag_connectivity = 4
    if retry>=5:
        print('imposible to connect mqtt server')
        global flag_connectivity
        flag_connectivity = 3
        while True:
            sleep(1000)
    # register call back functions on publish event
    client.on(mqtt.PUBLISH, print_sample)
    client.subscribe([["car/status/#",0]])
    client.subscribe([["car/commands",0]])
    # start the mqtt loop
    client.loop(print_messageREC) 
            

    while True:
        if flag_connectivity == 1:
            send_sample("car/connectivity",'Device connected',0)
        if flag_connectivity == 2:
            send_sample("car/connectivity",'ooops, something wrong while linking :-(',0)
        if flag_connectivity == 3:
            send_sample("car/connectivity",'mqtt server error, retry',0)
        if flag_connectivity == 4:
            send_sample("car/connectivity",'re-connecting...',0)
        if status == 'on':
            if mode == 'automatic':
                func.forward()
                distance = front.getDistanceCM()
                send_sample("car/distance/sens1",distance,0)
                back_distance = back.getDistanceCM()
                send_sample("car/distance/sens2",back_distance,0)
                infrared_l = digitalRead(pin.left_infrared)
                infrared_r = digitalRead(pin.right_infrared)
                if (infrared_l == LOW):
                    send_sample("car/infrared/left","Object on left infrared sensor",0)
                else:
                    send_sample("car/infrared/left","No object on left infrared sensor",0)
                if (infrared_r == LOW):
                    send_sample("car/infrared/right","Object on right infrared sensor",0)
                else:
                    send_sample("car/infrared/right","No object on right infrared sensor",0)
                if distance<=25 or distance>=613:
                    func.ultrasonic() #obstacle avoid function using ultrasonic sensor and infrared sensors
                func.infrared() #obstacle avoid function using infrared sensors
            if mode == 'manual':
                distance = front.getDistanceCM()
                send_sample("car/distance/sens1",distance,0)
                back_distance = back.getDistanceCM()
                send_sample("car/distance/sens2",back_distance,0)
                infrared_l = digitalRead(pin.left_infrared)
                infrared_r = digitalRead(pin.right_infrared)
                if (infrared_l == LOW):
                    send_sample("car/infrared/left","Object on left infrared sensor",0)
                else:
                    send_sample("car/infrared/left","No object on left infrared sensor",0)
                if (infrared_r == LOW):
                    send_sample("car/infrared/right","Object on right infrared sensor",0)
                else:
                    send_sample("car/infrared/right","No object on right infrared sensor",0)
                if command == 'go':
                    func.forward()
                    sleep(300)
                    command='stop'
                if command == 'back':
                    func.backword()
                    sleep(300)
                    command='stop'
                if command == 'left':
                    func.right_turn()
                    sleep(250)
                    command='stop'
                if command == 'right':
                    func.left_turn()
                    sleep(250)
                    command='stop'
                if command == 'stop':
                    func.stop()
                sleep(1000)
                    
        if status == 'stop':
            func.stop()
            distance = front.getDistanceCM()
            send_sample("car/distance/sens1",distance,0)
            back_distance = back.getDistanceCM()
            send_sample("car/distance/sens2",back_distance,0)
            infrared_l = digitalRead(pin.left_infrared)
            infrared_r = digitalRead(pin.right_infrared)
            if (infrared_l == LOW):
                send_sample("car/infrared/left","Object on left infrared sensor",0)
            else:
                    send_sample("car/infrared/left","No object on left infrared sensor",0)
            if (infrared_r == LOW):
                send_sample("car/infrared/right","Object on right infrared sensor",0)
            else:
                    send_sample("car/infrared/right","No object on right infrared sensor",0)
            sleep(1000)
            
        if status == 'off':
            func.stop()
            send_sample("car/distance/sens1","the device is sleeping",0)
            send_sample("car/distance/sens2","the device is sleeping",0)
            send_sample("car/infrared/left","the device is sleeping",0)
            send_sample("car/infrared/right","the device is sleeping",0)
            sleep(1000)
except Exception as e:
    print("Master Error: ",e)
    
    
    
    
    