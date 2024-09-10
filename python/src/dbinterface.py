import pymongo
from bson import ObjectId
from bson.errors import InvalidId
from datetime import datetime
import time
import uuid
from scraper import scrape_obj
import hashlib

class dbinterface:
    def __init__(self, scraperhandle: scrape_obj):
        self.shandle = scraperhandle
        db_client = pymongo.MongoClient("mongodb://mytester2:databased1204@localhost:27017");
        self.db = db_client["testdb"]

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
                "filetype": scraped_text[2],
                "content": scraped_text[1],
                "file_ref_uuid": generated_filename,
                "content_checksum": hashlib.sha256(scraped_text[1].encode('utf-8')).hexdigest(),
                "tracker_ref_id": ref_id
             }
        )
        print(f"New Todo ID: {create_result.inserted_id}")
        return None
    def _check_license_changed(self, url):
        if (self.shandle.content == ""):
            self.shandle.get_text(url)
        new_content = self.shandle.content
        old_content_checksum = self.db.licenses.find_one(sort=[('_id', -1)]).get('content_checksum')
        if (hashlib.sha256(new_content.encode('utf-8')).hexdigest() == old_content_checksum):
            return False
        return True
        #now do stuff
    
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

    #def fetch_license(

