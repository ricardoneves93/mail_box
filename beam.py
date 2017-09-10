import RPi.GPIO as GPIO
import time
import requests
from websocket_server import WebsocketServer

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

NEW_MAIL_MSG = "new_mail"
OPEN_DOOR_MSG = "open_door"
CLOSE_DOOR_MSG = "close_door"
RESET_MSG = "reset_mail"

GPIO.setmode(GPIO.BOARD)    
GPIO.setup(BREAK_BEAM, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(DOOR_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(FLAG_LED, GPIO.OUT)
GPIO.setup(FLAG_PIEZO, GPIO.OUT)
GPIO.setup(MAIL_LED, GPIO.OUT)

# Start with Mail Led turned off
GPIO.output(MAIL_LED, False)

# Start with Pioze turned off
GPIO.output(FLAG_PIEZO, False)

number_received_mails = 0

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
            global number_received_mails
            number_received_mails += 1
            server.send_message_to_all(NEW_MAIL_MSG + '_' + str(number_received_mails))
            

def door_callback(channel):
    if GPIO.input(DOOR_BUTTON):
        print "Door is opened"
        global number_received_mails
        number_received_mails = 0
        GPIO.output(MAIL_LED, False)
        server.send_message_to_all(OPEN_DOOR_MSG)
    else:
        print "Door is closed"
        server.send_message_to_all(CLOSE_DOOR_MSG)
    

# Add callback for IR Bream Beam
GPIO.add_event_detect(BREAK_BEAM, GPIO.BOTH, callback=beam_callback)
# Add callback for Door Button
GPIO.add_event_detect(DOOR_BUTTON, GPIO.BOTH, callback=door_callback)



#################################

# Called for every client connecting (after handshake)
def new_client(client, server):
	print("New client connected and was given id %d" % client['id'])
	server.send_message_to_all("Hey all, a new client has joined us")


# Called for every client disconnecting
def client_left(client, server):
	print("Client(%d) disconnected" % client['id'])


# Called when a client sends a message
def message_received(client, server, message):
	if len(message) > 200:
		message = message[:200]+'..'
	print("Client(%d) said: %s" % (client['id'], message))


PORT=8081
HOST="0.0.0.0"
server = WebsocketServer(PORT, HOST)
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
server.run_forever()



##################################

