import pymongo
from bson import ObjectId
from bson.errors import InvalidId
from datetime import datetime
import time
import uuid
from scraper import scrape_obj
import hashlib
from comparison_v2 import compare_obj

class dbinterface:
    def __init__(self, scraperhandle: scrape_obj):
        self.shandle = scraperhandle
        db_client = pymongo.MongoClient("mongodb://mytester2:databased1204@localhost:27017");
        self.db = db_client["testdb"]
        self.c_obj = compare_obj()

    def _now_millis(self):
        return round(time.time() * 1000)

    def _save_license_info(self, title: str, url: str, ref_id):
        generated_filename = str(uuid.uuid4())
        self.shandle.get_text(url)
        scraped_text = self.shandle.save_to_file(url, generated_filename)
        create_result = self.db.licenses.insert_one(
            {
                "title": title,
                "created_date": self._now_millis(),
                "url": url,
                "filepath": scraped_text[0],
                "filetype": self.shandle.filetype,
                "content": self.shandle.content,
                "file_ref_uuid": generated_filename,
                "content_checksum": self.c_obj.checksum_bytes(self.shandle.content),
                "tracker_ref_id": ref_id
             }
        )
        print(f"New Todo ID: {create_result.inserted_id}")
        return None
    def check_license_changed(self, trackerid) -> bool:
        if (self.shandle.content == ""):
            print("gettign congteht")
            url = self.db.tracker.find_one({"_id": ObjectId(trackerid)}).get('url')
            self.shandle.get_text(url)
        old_content_checksum = self.db.licenses.find_one({'tracker_ref_id': ObjectId(trackerid)}, sort=[('_id', -1)]).get('content_checksum')
        return self.c_obj.checksum_compare_bytes_checksum(self.shandle.content, old_content_checksum)
    
    def add_license(self, title: str, url: str, frequency: int):
        #frequency should be in hours, we store time in millis so convert it

        frequency = int(frequency) * 3600000
        ref_id = ObjectId()
        self._save_license_info(title, url, ref_id)
        self.db.tracker.insert_one(
                    {
                        "_id": ref_id,
                        "title": title,
                        "url": url,
                        "frequency": frequency,
                        "last_checked": self._now_millis()
                     }
                )

    def get_licenses_list(self):    
        projection = {'_id': 1, 'title': 1, 'url':1}
        query=None
        documents = self.db.tracker.find(query, projection)
        result = list(documents)
        return result

    #def fetch_license(

