import RPi.GPIO as GPIO
import time

# Gpio 11 - IR Break Beam
# Gpio 13 - Beam Broken Flag led
# Gpio 15 - Bean Broken Flag Piezo
# Gpio 19 - Mail led
# Gpio 21 - Door button

BREAK_BEAM = 11
FLAG_LED = 13
FLAG_PIEZO = 15
MAIL_LED = 19
DOOR_BUTTON = 21

GPIO.setmode(GPIO.BOARD)    
GPIO.setup(BREAK_BEAM, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(DOOR_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(FLAG_LED, GPIO.OUT)
GPIO.setup(FLAG_PIEZO, GPIO.OUT)
GPIO.setup(MAIL_LED, GPIO.OUT)

# Start with Mail Led turned off
GPIO.output(MAIL_LED, False)

def beam_callback(channel):
    if GPIO.input(BREAK_BEAM):
        print "Beam clear"
        GPIO.output(FLAG_LED, False)
        GPIO.output(FLAG_PIEZO, False)
    else:
        print "Beam Interrupted"
        # if the door is closed
        if GPIO.input(DOOR_BUTTON) == False:
            GPIO.output(FLAG_LED, True)
            GPIO.output(FLAG_PIEZO, True)
            GPIO.output(MAIL_LED, True)
            

def door_callback(channel):
    if GPIO.input(DOOR_BUTTON):
        print "Door is opened"
        GPIO.output(MAIL_LED, False)
    else:
        print "Door is closed"
    

# Add callback for IR Bream Beam
GPIO.add_event_detect(BREAK_BEAM, GPIO.BOTH, callback=beam_callback)
# Add callback for Door Button
GPIO.add_event_detect(DOOR_BUTTON, GPIO.BOTH, callback=door_callback)






while True:
    broken = GPIO.input(BREAK_BEAM) == 0

GPIO.cleanup()


