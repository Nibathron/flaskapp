from flask import Flask, request, jsonify
import pigpio
import json
import logging
 

app = Flask(__name__)
pi = pigpio.pi()

# Log file ends up in/home/pi
logging.basicConfig(filename='record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

app.logger.info('Is this ever printed')

def hwpwm(val):
    
    pwm = abs(val)
    fwd = 0
    rev = 0
    
    if(pwm < 0.2):
    	pwm = 0
    
    pwm = int(pwm * 1e6)
    
    if(val > 0):
        fwd = 1
        rev = 0
    else:
        fwd = 0
        rev = 1

    return pwm, fwd, rev

def pwm(val):
    
    pwm = abs(val)
    fwd = 0
    rev = 0
    
    if(pwm < 0.2):
    	pwm = 0
    
    pwm = pwm * 255
    
    if(val > 0):
        fwd = 1
        rev = 0
    else:
        fwd = 0
        rev = 1

    return pwm, fwd, rev



# {{url}}/led?status=on
@app.route('/', methods=['GET'])
def led():

    #red =   int(request.args.get('red'))   if (request.args.get('red'))   else 0
    #green = int(request.args.get('green')) if (request.args.get('green')) else 0
    
    # Axis 1 left
    left = float(request.args.get('red'))
    
    # Axis 3 right
    right = float(request.args.get('green'))

    #app.logger.info('RGB LED function %f  %f' % (left, right))
    #left = left * 0.92
    
    PR,AR,BR = hwpwm(right)
    PL,AL,BL = hwpwm(left)
    app.logger.info("A B PWM val L/R  %d %d %07d %+2.7f : %d %d %07d %+2.7f" % (AL, BL, PL, left, AR, BR, PR, right))
    
    '''
				   3V3  (1) (2)  5V    
				 GPIO2  (3) (4)  5V       	Red
				 GPIO3  (5) (6)  GND      	Black
				 GPIO4  (7) (8)  GPIO14   	Purple PWM Left
				   GND  (9) (10) GPIO15
				GPIO17 (11) (12) GPIO18   	Green Forward Left
				GPIO27 (13) (14) GND   
				GPIO22 (15) (16) GPIO23
				   3V3 (17) (18) GPIO24   	Orange Forward Right
				GPIO10 (19) (20) GND   
				 GPIO9 (21) (22) GPIO25   	White Backward Right
				GPIO11 (23) (24) GPIO8 
				   GND (25) (26) GPIO7 
				 GPIO0 (27) (28) GPIO1 
				 GPIO5 (29) (30) GND   
				 GPIO6 (31) (32) GPIO12
	Yellow PWM Right	GPIO13 (33) (34) GND   
				GPIO19 (35) (36) GPIO16
				GPIO26 (37) (38) GPIO20   	Blue Backward Left
	Black	   		   GND (39) (40) GPIO21

    '''
    
    # H-bridge1 pin-setup = Yellow | White  | Gray  | Red   | Blue | Green
    
    # H-bridge2 pin-setup = 5V     | Green  | Blue  | Red   | GND
    #                       5V     | Yellow | Gray  | White | GND
    
    # Left Motor
    pi.hardware_PWM(12, 800, PL) # Purple pin 8
    pi.write(24, AL) # Orange pin 18
    pi.write(25, BL) # White pin 22

    # Right Motor
    pi.hardware_PWM(13, 800, PR) # Yellow pin 5
    pi.write(18, AR) # Green pin 12
    pi.write(20, BR) # Blue pin 38
    

    return jsonify({"red": left, "green": right, "blue": 0})
