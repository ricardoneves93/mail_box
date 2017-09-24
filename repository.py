import datetime
from pymongo import MongoClient

client = MongoClient()
client = MongoClient('localhost', 27017)

db = client.mail

# Email 
def insert_mail() :
    mail_collection = db.mail_collection
    now = datetime.datetime.now()
    date = format_time(now.year) + '-' + format_time(now.month) + '-' + format_time(now.day)
    mail_data = {"date": date,
                "time": format_time(now.hour) + ':' + format_time(now.minute)
                }
    mail_data_id = mail_collection.insert_one(mail_data).inserted_id

    print(mail_data_id)

# Current states
def get_current_state() :
    current_state_collection = db.current_state_collection
    state_id = current_state_collection.find_one().get('_id')
    print("Getting current state: " + str(state_id))
    return state_id

def update_current_mail_state(mail_state) :
    current_state_collection = db.current_state_collection
    state_id = get_current_state()
    current_state_collection.update_one({'_id': state_id}, {'$set': {'mail': mail_state}})

def update_current_door_state(door_state) :
    current_state_collection = db.current_state_collection
    state_id = get_current_state()
    current_state_collection.update_one({'_id': state_id}, {'$set': {'door': door_state}})


#### Utils ####
def format_time(time_unit):
    if len(str(time_unit)) == 1:
        return '0' + str(time_unit)
    else :
        return str(time_unit)
    
