import paho.mqtt.client as mqtt
import time
import tkinter as tk #gui
from tkinter import * #gui

#callback definitions 
def on_connect(client,userdata,flags,rc): 
    if rc == 0:
        connectivityLable['text'] = 'Connectivity status: connected'
        connectivityLable['fg'] = 'green'
        if connectButton['state'] == 'normal':
            connectButton['state'] = 'disabled'
        if onButton['state'] == 'disabled':
            onButton['state'] = 'active'
        if stopButton['state'] == 'disabled':
            stopButton['state'] = 'active'
    else:
        connectivityLable['text'] = 'Connectivity status: connection error with code[ ' + str(rc) + ']'
        connectivityLable['fg'] = 'red'

def on_disconnect(client,userdata,flags,rc=0):
    connectivityLable['text'] = 'Connectivity status: disconnected with code: ['+ str(rc) + ']'
    connectivityLable['fg'] = 'red'
    if connectButton['state'] == 'disabled':
            connectButton['state'] = 'active'
    upButton['state'] = 'disabled'
    downButton['state'] = 'disabled'
    leftButton['state'] = 'disabled'
    rightButton['state'] = 'disabled'
    client.publish("car/status",'off')

def on_message(client,userdata,message):
    if (message.topic == 'car/connectivity'):
        carConnectivityLabel['text'] = message.payload
        if message.payload  == b'Device connected':
            carConnectivityLabel['fg'] = 'green'
    if (message.topic == 'car/distance/sens1'):
        ultrasonic1Lable['text'] = message.payload
    if (message.topic == 'car/distance/sens2'):
        ultrasonic2Lable['text'] = message.payload
    if (message.topic == "car/infrared/right") :
        infrared_r_value_Lable['text'] = message.payload
    if (message.topic == "car/infrared/left") :
        infrared_l_value_Lable['text'] = message.payload

#button actions
def on_click(): #turn on the device in order to receive data and control it
    statusLable['text'] = 'Device status: on'
    statusLable['fg'] = 'green'
    client.publish("car/status",'on')
    client.publish("car/status/mode",selectedMode.get())
    onButton["state"] = 'disabled'
    offButton["state"] = 'active'
    stopButton["state"] = 'active'
    if selectedMode.get() == 'manual':
        upButton['state'] = 'active'
        downButton['state'] = 'active'
        leftButton['state'] = 'active'
        rightButton['state'] = 'active'
    if selectedMode.get() == 'automatic':
        upButton['state'] = 'disabled'
        downButton['state'] = 'disabled'
        leftButton['state'] = 'disabled'
        rightButton['state'] = 'disabled'

def off_click(): #stop the device from sending data and moving
    statusLable['text'] = 'Device status: off'
    statusLable['fg'] = 'red'
    client.publish("car/status",'off')
    offButton["state"] = 'disabled'
    onButton["state"] = 'active'
    stopButton["state"] = 'active'
    upButton['state'] = 'disabled'
    downButton['state'] = 'disabled'
    leftButton['state'] = 'disabled'
    rightButton['state'] = 'disabled'

def stop_click(): #stand-by 
    statusLable['text'] = 'Device status: stop'
    statusLable['fg'] = 'orange'
    client.publish("car/status",'stop')
    stopButton["state"] = 'disabled'
    onButton["state"] = 'active'
    offButton["state"] = 'active'
    upButton['state'] = 'disabled'
    downButton['state'] = 'disabled'
    leftButton['state'] = 'disabled'
    rightButton['state'] = 'disabled'
  
def connect_click(): #connect
    try:
        for retry in range(5):
            try:
                connectivityLable['text'] = 'Connectivity status: connectiong to broker: ' + broker
                client.connect(broker,1883,60)
                break
            except Exception as e:
                connectivityLable['text'] = 're-connecting... ' + retry
        if retry>= 5:
            connectivityLable['text'] = 'connection failure...closing'
            i=0
            while i<=2:
                i+=1
            root.destroy()
        client.subscribe("car/distance/#")
        client.subscribe("car/infrared/#")
        client.subscribe("car/status")
        client.subscribe('car/connectivity')
        client.loop_start()
    except Exception as e:
        connectivityLable['text'] = 'error'

def close_click(): #close gui window
    client.publish("car/status",'off')
    client.disconnect()
    root.destroy()

def up_click(): #send the device forward
    client.publish("car/commands",'go',2)
    
def down_click(): #send the device backward
    client.publish("car/commands",'back',2)

def left_click(): #turn left 
    client.publish("car/commands",'left',2)

def right_click(): #turn right
    client.publish("car/commands",'right',2)


broker = "test.mosquitto.org" #mqtt
client = mqtt.Client("smart_car_client")

#register call back functions
client.on_connect = on_connect 
client.on_disconnect = on_disconnect
client.on_message = on_message


#gui definitions
root = tk.Tk() 
root.title('Smart Car') 
root.geometry("680x200")
connectivityLable = Label(root, text="Connectivity status: disconnected", fg = 'red')
statusLable = Label(root, text='Device status: off', fg = 'red')
carConnectivityLabel = Label(root,text='Device not available',fg='red')
ultrasonic1Lable = Label(root, text= 'the device is sleeping')
ultrasonic2Lable = Label(root, text= 'the device is sleeping')
sensor1Lable = Label(root, text='Distance front: ')
sensor2Lable = Label(root, text='Distance back: ')
infrared_l_Lable = Label(root, text='Left Infrared: ')
infrared_r_Lable = Label(root, text='Right Infrared: ')
infrared_r_value_Lable = Label(root, text='the device is sleeping')
infrared_l_value_Lable = Label(root, text='the device is sleeping')
onButton = Button(root, text="On", command = on_click, width=10,state = 'disabled')
stopButton = Button(root, text="Stop", command = stop_click,width=10,state = 'disabled')
offButton = Button(root, text="Off", command = off_click,width=10, state = 'disabled')
connectButton = Button(root,text = "Connect", command = connect_click,width=10)
exitButton = Button(root,text = "Close",command=close_click,width=10)
upButton = Button(root,text = "⬆",command=up_click,width=10,state = 'disabled')
downButton = Button(root,text = "⬇",command=down_click,width=10,state = 'disabled')
leftButton = Button(root,text = "➡",command=left_click,width=10,state = 'disabled')
rightButton = Button(root,text = "⬅",command=right_click,width=10,state = 'disabled')


mode = ['manual','automatic']
selectedMode = StringVar()
selectedMode.set(mode[0])
modeMenu = OptionMenu(root, selectedMode, *mode)

 #add to grid
connectivityLable.grid(row = 0, column=1)
statusLable.grid(row = 0, column = 2)
carConnectivityLabel.grid(row = 0, column = 3)
onButton.grid(row=1, column=0)
stopButton.grid(row=1, column=1)
offButton.grid(row = 1, column = 2)
modeMenu.grid(row = 1, column = 3)
sensor1Lable.grid(row = 2, column = 0)
ultrasonic1Lable.grid(row = 2, column = 1)
sensor2Lable.grid(row = 2, column = 2)
ultrasonic2Lable.grid(row = 2, column = 3)
infrared_l_Lable.grid(row = 3, column = 0)
infrared_l_value_Lable.grid(row = 3, column = 1)
infrared_r_Lable.grid(row = 3, column = 2)
infrared_r_value_Lable.grid(row = 3, column = 3)
upButton.grid(row = 4, column = 1)
downButton.grid(row = 5, column = 1)
leftButton.grid(row = 4, column = 2)
rightButton.grid(row = 5, column = 2)
connectButton.grid(row =6, column = 1)
exitButton.grid(row = 6, column = 2)

root.mainloop() 






