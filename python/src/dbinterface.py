import pymongo
from bson import ObjectId
from bson.errors import InvalidId
from datetime import datetime

class dbinterface:
    db = ""
    def __init__(self, mongoaddress):
        db_client = pymongo.MongoClient(mongoaddress);
        self.db = db_client["testdb"]

    def create_license(self, title: str, url: str, filepath: str, content: str, uuid: str):
        create_result = self.db.licenses.insert_one(
            {
                "title": title,
                "created_date": datetime.utcnow(),
                "url": url,
                "filepath": filepath,
                "filetype": filepath.split('.')[-1],
                "content": content,
                "file_ref_uuid": uuid
             }
        )
        print(f"New Todo ID: {create_result.inserted_id}")
        return None
