#functions

import pin

def forward(): #all dc motors forward
    digitalWrite(pin.left_forward,HIGH)
    digitalWrite(pin.left_backward,LOW)
    digitalWrite(pin.right_forward,HIGH) 
    digitalWrite(pin.right_backward,LOW)

    
def backword(): #all dc motors backword
    digitalWrite(pin.left_forward,LOW)
    digitalWrite(pin.left_backward,HIGH)
    digitalWrite(pin.right_forward,LOW) 
    digitalWrite(pin.right_backward,HIGH)

    
def stop(): #all dc motors stop
    digitalWrite(pin.left_forward,LOW);                
    digitalWrite(pin.left_backward,LOW);
    digitalWrite(pin.right_forward,LOW);                 
    digitalWrite(pin.right_backward,LOW);

    
        
def left_turn(): #2 dc motors turn left
    digitalWrite(pin.left_forward,HIGH);                
    digitalWrite(pin.left_backward,LOW);
    digitalWrite(pin.right_forward,LOW);                 
    digitalWrite(pin.right_backward,LOW);

    
def right_turn(): #2 dc motors turn right
    digitalWrite(pin.left_forward,LOW);                
    digitalWrite(pin.left_backward,LOW);
    digitalWrite(pin.right_forward,HIGH);                 
    digitalWrite(pin.right_backward,LOW);


def infrared(): #infrared behaviour 
    lf_infrared = digitalRead(pin.left_infrared)
    rg_infrared = digitalRead(pin.right_infrared)
    if lf_infrared == LOW and rg_infrared == HIGH:
        backword()
        sleep(500)
        right_turn()
        sleep(500)
    elif rg_infrared == LOW and lf_infrared == HIGH:
        backword()
        sleep(1000)
        left_turn()
        sleep(500)
    elif lf_infrared == LOW and rg_infrared == LOW:
        stuck()
        
        
def ultrasonic(): #ultrasonic obstacles behaviour
    lf_infrared = digitalRead(pin.left_infrared)
    rg_infrared = digitalRead(pin.right_infrared)
    if lf_infrared == LOW and rg_infrared == HIGH:
        backword()
        sleep(500)
        right_turn()
        sleep(500)
    elif rg_infrared == LOW and lf_infrared == HIGH:
        backword()
        sleep(500)
        left_turn()
        sleep(500)
    else:
        stuck()

        
def stuck(): #when device can't go anywhere else or there aren't enought information
    backword()
    sleep(500)
    left_turn()
    sleep(500)

        

