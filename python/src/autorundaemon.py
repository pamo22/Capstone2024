import pymongo
from bson import ObjectId
from datetime import datetime
import time
from scraper import scrape_obj
from comparison_v2 import compare_obj
import uuid 
import os
from pymongo import MongoClient
import sys

# Initialize database connection and objects
mongo_uri = os.getenv("MONGO_URI", "mongodb://mytester2:databased1204@mongodb:27017/testdb")
db_client = MongoClient(mongo_uri)
db = db_client["testdb"]
scrape_handle = scrape_obj()
compare_handle = compare_obj()

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def _now_millis():
    return round(time.time() * 1000)

def update_tracker():
    """Checks and updates items in the tracker database collection."""
    now_millis = _now_millis()
    tracker_collection = db.tracker
    licenses_collection = db.licenses
    
    # Fetch all items from the tracker collection
    items = tracker_collection.find()
    

    for item in items:
        #print (item)
        last_checked = int(item.get('last_checked', 0))
        frequency = int(item.get('frequency', 0))
        url = item.get('url', '')
        ref_id = item.get('_id')

        # Check if it's time to check this item
        #print (item['title'] + ": " + str(now_millis - last_checked))
        if now_millis - last_checked >= frequency:
            eprint(f"Checking item: {item['title']}")

            # Fetch current content
            scrape_handle.get_bytes(url)
            new_bytes = scrape_handle.bytes
            if (new_bytes == None):
                tracker_collection.update_one(
                    {'_id': ref_id},
                    {'$set': {'last_checked': now_millis}}
                )
                continue
            new_checksum = compare_handle.checksum_bytes(new_bytes)
            
            # Fetch old content from the database
            old_license = licenses_collection.find_one(
                {'tracker_ref_id': ref_id},
                sort=[('created_date', pymongo.DESCENDING)]
            )
            old_checksum = old_license.get('content_checksum') if old_license else None
            
            if new_checksum != old_checksum:
                eprint(f"Content has changed for {item['title']}. Updating database...")
                # Save new license info to the database
                generated_filename = str(uuid.uuid4())
                scrape_handle.process_text()
                new_content = scrape_handle.content
                filepath = scrape_handle.save_to_file(url, generated_filename)
                
                licenses_collection.insert_one(
                    {
                        "title": item['title'],
                        "created_date": now_millis,
                        "url": url,
                        "filepath": filepath[0],
                        "filetype": scrape_handle.filetype,
                        "content": new_content,
                        "file_ref_uuid": generated_filename,
                        "content_checksum": new_checksum,
                        "tracker_ref_id": ref_id,
                        "changes": compare_handle.compare_strings(new_content, old_license.get('content')) if old_license else None
                    }
                )
                
                
                # Update last_checked time in the tracker collection
                tracker_collection.update_one(
                    {'_id': ref_id},
                    {'$set': {'last_checked': now_millis}}
                )
            else:
                eprint(f"No changes detected for {item['title']}.")
                tracker_collection.update_one(
                    {'_id': ref_id},
                    {'$set': {'last_checked': now_millis}}
                )
    
    eprint("Tracker update complete: ",datetime.fromtimestamp(_now_millis()/1000.0))

# To run the update function periodically, you might use a loop or a scheduler
if __name__ == "__main__":
    while True:
        update_tracker()
        time.sleep(10)  # Check every 10 seconds
