#pin and pinMode

left_forward = D22 #dc motor
left_backward = D21
right_forward = D18
right_backward = D19

left_infrared = D3 #infrared sensor
right_infrared = D16

trigger = D5 #ultrasonic sensor
echo = D17
trigger_back = D23
echo_back = D2


pinMode(left_forward,OUTPUT)     #pinmode dc motors
pinMode(left_backward,OUTPUT)    
pinMode(right_forward,OUTPUT)   
pinMode(right_backward,OUTPUT)


pinMode(left_infrared,INPUT_PULLDOWN) #pinMode infrared sensors 
pinMode(right_infrared,INPUT)

pinMode(trigger,OUTPUT) #pinMode ultrasonic sensor
pinMode(echo,INPUT)
pinMode(trigger_back,OUTPUT)
pinMode(echo_back,INPUT)