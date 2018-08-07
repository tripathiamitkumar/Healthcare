#import the libraries that will be needed
import webiopi
from time import sleep
from webiopi import deviceInstance
import datetime
import RPi.GPIO as GPIO
#from webiopi.devices.sensor import DS18B20
#DS18b20=10-00080062d1e6  w1_bus_master1

#Enable debug output
webiopi.setDebug()

#set GPIO as a shortcut for webiopi.GPIO
#GPIO = webiopi.GPIO
HR = 17 #GPIO pin 17 using BCM numbering
#GPIO.setmode(GPIO.BOARD)	# for RPi numbering
#GPIO.setup(HR, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#GPIO.setup(HR, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setmode(GPIO.BCM)		# for CPU numbering
#GPIO.setup(HR, GPIO.IN)

global tmp,celsius
global BPM, flag, Count, Pulse
flag = 0
Count = 0
Pulse = 0

def HR_callback (HR):
    global flag, BPM, Pulse
    global t1, t2, now
    Pulse = Pulse + 1
    now = datetime.datetime.now()
    t1 = now.microsecond
    t1 = t1/1000
    #t1 = now.second
    if (flag == 0):
        flag = 1
        t1 = now.microsecond
        #t1 = now.second
        t2 = t1
    if t2>t1:
        #BPM = (t2 - t1)
        flag = 1
    else:
        #BPM = (t1 - t2)
        flag = 1
    #BPM = 20
    t2 = t1
    
    

# setup function is automatically called at WebIOPi startup
def setup():
    global tmp, celsius, BPM, flag
    flag = 0
    BPM = 0
    tmp = webiopi.deviceInstance("temp2") # retrieve the device named "mcp" in the configuration
    #GPIO.setFunction(HR, GPIO.IN) #Set the pin to be an Input
    #GPIO.setup(HR, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(HR, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(HR, GPIO.RISING, callback = HR_callback)
    webiopi.debug("HR script - Setup")

#loop function is repeatedly called by WebIOPi
def loop():
    global tmp, celsius, flag, Count, Pulse, BPM
    Count = Count + 1
    tmp = webiopi.deviceInstance("temp2")
    celsius = "%.2f" % (tmp.getCelsius()) # retrieve current temperature
    print (celsius)
    print (BPM)
    #print("Temperature: %0.2f" % celsius)
    #GPIO.add_event_detect(HR, GPIO.RISING, callback=hr_callback, bouncetime=000)
    # gives CPU some time before looping again
    webiopi.sleep(1)
    if (Count > 10):
        print (Pulse)
        BPM = Pulse * 3
        Count = 0
        Pulse = 0
        
    #BPM=0

# destroy function is called at WebIOPi shutdown
def destroy():
    webiopi.debug("HEALTH - Destroy")
    GPIO.setFunction(HR, GPIO.OUT)


# -------------------------------------------------- #
# Macro definition part #
# -------------------------------------------------- #

# Macro called by WebIOPi to retreve DS18B20 Temp sensors

@webiopi.macro
def getTemp():
    global a, celsius
    a = 0
    #BPM = a
    print (celsius)
    print ( BPM )
    celsius = "%.2f" % (tmp.getCelsius())
    #BPM = 82
    return "%s %s" % (celsius, BPM)

