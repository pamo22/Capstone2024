from pymongo import MongoClient

client = MongoClient("mongo://127.....")

db = client.ourdatabase

dataset = db.dataset

dataset.insert_one({"licenseName": "aaa", "Url": "1111", "time": "1111"})

for data in dataset.find():
    print(data)