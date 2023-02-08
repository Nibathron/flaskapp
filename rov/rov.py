from flask import Flask, request, jsonify
#import pigpio
import json
import logging
#from board import SCL, SDA
#import busio
import serial



ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=0)
"""
pca = PCA9685(i2c_bus)

# Set the PWM frequency to 60hz.
pca.frequency = 1600

# PWM on 0 and 4

motorA_PWM = 4
motorA_A   = 5
motorA_B   = 6

motorB_PWM = 0
motorB_A   = 2
motorB_B   = 1
"""
# Set the PWM duty cycle for channel zero to 50%. duty_cycle is 16 bits to match other PWM objects
# but the PCA9685 will only actually give 12 bits of resolution.

#pca.channels[0].duty_cycle = 0xffff
#time.sleep(5)

V = 1

l = 0
r = 0
"""
V = 1

aa = 0
ab = 0
ap = 0
ba = 0
bb = 0
bp = 0


pca.channels[motorA_A].duty_cycle   = 0xFFFF
pca.channels[motorA_B].duty_cycle   = 0x0000
pca.channels[motorA_PWM].duty_cycle = 0x0000

pca.channels[motorB_A].duty_cycle   = 0xFFFF
pca.channels[motorB_B].duty_cycle   = 0x0000
pca.channels[motorB_PWM].duty_cycle = 0x0000
"""




app = Flask(__name__)

#pi = pigpio.pi()

# Log file ends up in/home/pi
logging.basicConfig(filename='record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s : %(message)s')

app.logger.info('Is this ever printed')
"""
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
"""
"""
def hwpwm(val):
    
    pwm = abs(val)
    fwd = 0X0000
    rev = 0X0000
    
    if(pwm < 0.2):
    	pwm = 0X0000
    
    pwm = int(pwm * 0XFFFF)
    
    if(val > 0):
        fwd = 0XFFFF
        rev = 0X0000
    else:
        fwd = 0X0000
        rev = 0XFFFF

    return pwm, fwd, rev
"""
"""
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

"""

# {{url}}/led?status=on
@app.route('/', methods=['GET'])
def led():

    global V

    global l
    global r

    """
    global V
    
    global aa
    global ab
    global ap
    global ba
    global bb
    global bp
    """
    #red =   int(request.args.get('red'))   if (request.args.get('red'))   else 0
    #green = int(request.args.get('green')) if (request.args.get('green')) else 0
    
    # Axis 1 left
    left = float(request.args.get('red'))

    # Axis 3 right
    right = float(request.args.get('green'))
    
    
    #app.logger.info('RGB LED function %+2.7f  %+2.7f' % (left, right))
    
    """
    if left > 0.1 or left < -0.1:
        test="0," + str(int(left * 1023)) + ",s\n"
        app.logger.info(test)
        ser.write(test.encode())
    """
    V = V - 1
    if V == 0:
        V = 5

        if abs(left) < 0.09:
            left = 0
        
        if abs(right) < 0.05:
            right = 0


        #if left > 0.5 or left < -0.5:
            #l=1
        
        #if right > 0.2 or right < -0.2:
            #r=1
        #app.logger.info(right)
        
        #if l==1 or r==1:
        #test=("%s,%s,s\n" % (str(int(right * 300)), str(int(left * 300))))
        test=("%s,%s,s\n" % (str(int(right * 255)), str(int(left * 255))))
        app.logger.info(test)
        ser.write(test.encode())
            #l=0
            #r=0
        #else:
            #ser.write("0,0,s\n".encode())


    """
    left = left * 0.92
    
    PR,AR,BR = hwpwm(right)
    PL,AL,BL = hwpwm(left)
    
    app.logger.info("A B PWM val L/R  %d %d %07d %+2.7f : %d %d %07d %+2.7f  V %d" % (AL, BL, PL, left, AR, BR, PR, right, V))
    """
    
    '''
				   3V3  (1) (2)  5V    
				 GPIO2  (3) (4)  5V       	
				 GPIO3  (5) (6)  GND      	Black
				 GPIO4  (7) (8)  GPIO14   	
				   GND  (9) (10) GPIO15
				GPIO17 (11) (12) GPIO18   	Yellow Forward Left
				GPIO27 (13) (14) GND   
				GPIO22 (15) (16) GPIO23
				   3V3 (17) (18) GPIO24   	Blue Forward Right
				GPIO10 (19) (20) GND   
				 GPIO9 (21) (22) GPIO25   	Purple Backward Right
				GPIO11 (23) (24) GPIO8 
				   GND (25) (26) GPIO7 
				 GPIO0 (27) (28) GPIO1 
				 GPIO5 (29) (30) GND   
				 GPIO6 (31) (32) GPIO12	Gray PWM Left
	Orange PWM Right	GPIO13 (33) (34) GND   
				GPIO19 (35) (36) GPIO16
				GPIO26 (37) (38) GPIO20   	Green Backward Left
		   		   GND (39) (40) GPIO21

    '''
    
    
    
    #                       PWM L  | FL     | BL     | FR     | BR     | PWM R
    # H-bridge1 pin-setup = Orange | Yellow | Green  | Blue   | Purple | Gray
    
    
    #                       VCC    | PWM R  | FR     | BR     | GND
    #                       VCC    | PWM L  | FL     | BL     | GND

    # H-bridge2 pin-setup = 5V     | Gray   | Blue   | Purple | GND
    #                       5V     | Orange | Yellow | Green  | GND
    
    
    
    # Left Motor
    """
    pi.hardware_PWM(12, 20000, PL) # Purple pin 32
    pi.write(24, AL) # Orange pin 18
    pi.write(25, BL) # White pin 22
    """
    
    
    # Right Motor
    """
    pi.hardware_PWM(13, 20000, PR) # Yellow pin 5
    pi.write(18, AR) # Green pin 12
    pi.write(20, BR) # Blue pin 38
    """
    """
    V = V - 1
    if V == 0:
     V = 3
     # Left Motor
     if aa != AL:
      
      pca.channels[motorA_A].duty_cycle     = AL
      pca.channels[motorA_B].duty_cycle     = BL
      
      #app.logger.info("aa ab  ba bb  V  %d %d : %d %d  %d" % (aa, ab, ba, bb, V))
      
     aa = AL
     ab = BL
     
     if ap != 0:
      pca.channels[motorA_PWM].duty_cycle   = PL
     ap = PL
    
     # Right Motor
     if ba != AR:
     
      pca.channels[motorB_A].duty_cycle     = AR
      pca.channels[motorB_B].duty_cycle     = BR
      
      #app.logger.info("aa ab  ba bb  V  %d %d : %d %d  %d" % (aa, ab, ba, bb, V))
      
     ba = AR
     bb = BR 
     
     if bp != 0:
      pca.channels[motorB_PWM].duty_cycle   = PR
     bp = PR
    """

    return jsonify({"red": left, "green": right, "blue": 0})

