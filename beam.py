import RPi.GPIO as GPIO
import time
#import threading
import requests
import repository
from websocket_server import WebsocketServer
from pyfcm import FCMNotification

push_service = FCMNotification(api_key="AAAA8Er9Crw:APA91bFPCIKjFBN2LqqIstFM2YmGPt60qhHmH8t57sWV7QN2hqvxJqQMSV-LRx3e3Fxwe1hqpyE5vqHk8UKYSolXWHlkIJRSUE0_rGLWGEmbCRLkNEkzPgEYEQw0sFzajpvxX4o6UZJa")
registration_id = "fRplp7bigAo:APA91bGabmUBUd44o95JShIxobCXNa5AIiRF4HS-Hla6xUHvCUf9_YH1M0d6L31aRGefDIkVKIXAIc9T4STdC95_d3mzzFFN2zxSddAbrY2DB7Es6RspzoMAUFHYHBt1YlM2qbzbkH_6"
registration_id_phone = "esSnDu-G0Ws:APA91bFLt06tXbxHnN71z1Yq9rrAxmp8Kng_T_aMfV1vrjDx1vOzKp-w963POXrC3nmbmibiaiugMd_BPGbnDfzpjgn3atU_3Y4_LGdzXp209w2qFugeBk-4Lwr77nDDlFspto67Jqbq"
message_title = "Correio recebido"
message_body = "Foi recebido correio"
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

CLOSED_DOOR_STATE = "closed"
OPENED_DOOR_STATE = "opened"
EMPTY_MAIL_STATE = "empty"
HAS_MAIL_STATE = "has_mail"

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
#e = threading.Event()

repository.update_current_mail_state(EMPTY_MAIL_STATE)
repository.update_current_door_state(CLOSED_DOOR_STATE)

def beam_callback(channel):
    if GPIO.input(BREAK_BEAM):
        print "Beam clear"
        GPIO.output(FLAG_LED, False)
        GPIO.output(FLAG_PIEZO, False)
    else:
        print "Beam Interrupted"
        # if the door is closed
        if GPIO.input(DOOR_BUTTON) == False:
            #t = threading.Thread(name='non-block', target=flashLed, args=(e, 2))
            #t.start()
            GPIO.output(FLAG_LED, True)
            GPIO.output(FLAG_PIEZO, True)
            GPIO.output(MAIL_LED, True)
            global number_received_mails
            repository.insert_mail()
            repository.update_current_mail_state(HAS_MAIL_STATE)
            number_received_mails += 1
            server.send_message_to_all(NEW_MAIL_MSG + '_' + str(number_received_mails))
            #result = push_service.notify_single_device(registration_id=registration_id_phone, message_title=message_title, message_body=NEW_MAIL_MSG)
            result = push_service.notify_topic_subscribers(topic_name="mail", message_body=NEW_MAIL_MSG)
            #print result
            

def door_callback(channel):
    if GPIO.input(DOOR_BUTTON):
        print "Door is opened"
        global number_received_mails
        number_received_mails = 0
        GPIO.output(MAIL_LED, False)
        repository.update_current_door_state(OPENED_DOOR_STATE)
        repository.update_current_mail_state(EMPTY_MAIL_STATE)
        #e.set()
        server.send_message_to_all(OPEN_DOOR_MSG)
        result = push_service.notify_topic_subscribers(topic_name="mail", message_body=OPEN_DOOR_MSG)
        #print result
        result = push_service.notify_topic_subscribers(topic_name="mail", message_body=RESET_MSG)
        #print result
    else:
        print "Door is closed"
        repository.update_current_door_state(CLOSED_DOOR_STATE)
        server.send_message_to_all(CLOSE_DOOR_MSG)
        result = push_service.notify_topic_subscribers(topic_name="mail", message_body=CLOSE_DOOR_MSG)
        #print result


def flashLed(e, t):
    print "flash the specified led every second"
    while not e.isSet():
        GPIO.output(MAIL_LED, True)
        time.sleep(0.5)
        event_is_set = e.wait(t)
        if event_is_set:
            GPIO.output(MAIL_LED, False)
            print "stop led from flashing"
        else:
            GPIO.output(MAIL_LED, False)
            "leds off"
            time.sleep(0.8)
    

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
    if message == "ping":
        server.send_message(client, "pong")



PORT=8081
HOST="0.0.0.0"
server = WebsocketServer(PORT, HOST)
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
server.run_forever()



##################################

