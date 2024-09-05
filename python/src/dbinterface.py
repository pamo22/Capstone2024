import pymongo
from bson import ObjectId
from bson.errors import InvalidId

class dbinterface:
    db = ""
    def __init__(self, mongoaddress):
        db_client = pymongo.MongoClient(mongoaddress);
        self.db = db_client["testdb"]

    def create_license(self, title: str) -> None:
        create_result = self.db.licenses.insert_one(
            {"title": title, "completed": False, "created_date": datetime.utcnow()}
        )
        print(f"New Todo ID: {create_result.inserted_id}")
        return None
