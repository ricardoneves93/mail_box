import datetime
from pymongo import MongoClient

client = MongoClient()
client = MongoClient('localhost', 27017)

db = client.mail


def insert_mail() :
    mail_collection = db.mail_collection
    now = datetime.datetime.now()
    print(str(now.hour) + '-' + str(now.minute))
    date = str(now.year) + '-' + str(now.month) + '-' + str(now.day)
    mail_data = {"date": date,
                "times": ['12:00', '16:45']
                }
    mail_data_id = mail_collection.insert_one(mail_data).inserted_id
    print(mail_data_id)
