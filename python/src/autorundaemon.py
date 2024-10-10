import pymongo
from bson import ObjectId
from datetime import datetime
import time
from scraper import scrape_obj
from comparison_v2 import compare_obj
import uuid

# Initialize database connection and objects

try:
    db_client = pymongo.MongoClient("mongodb://mytester2:databased1204@localhost:27017")
except pymongo.errors.ConnectionError as e:
    print(f"Database connection failed: {e}")
    exit(1)
db = db_client["testdb"]
scrape_handle = scrape_obj()
compare_handle = compare_obj()


def _now_millis():
    return round(time.time() * 1000)


def update_tracker():
    """Checks and updates items in the tracker database collection."""
    now_millis = _now_millis()
    tracker_collection = db.tracker
    licenses_collection = db.licenses

    # Hard-code the frequency to 24 hours (in milliseconds)
    frequency = 24 * 60 * 60 * 1000



    # Fetch only items that haven't been scraped yet (new trackers)

    new_tracker_count = tracker_collection.count_documents({'scraped': False})
    if new_tracker_count == 0:
        print("No new trackers found.")
        return

    not_scraped_items = tracker_collection.find({'scraped': False})
    for item in not_scraped_items:
        last_checked = int(item.get('last_checked', None))
        # frequency = int(item.get('frequency', 0))
        url = item.get('url', '')
        ref_id = item.get('_id')

        print(f"Scraping item: {item['title']}")
        # Fetch current content
        scrape_handle.get_bytes(url)
        new_bytes = scrape_handle.bytes
        if new_bytes is None:
            # tracker_collection.update_one(
            #    {'_id': ref_id},
            #    {'$set': {'last_checked': now_millis}}
            # )
            print(f"Failed to scrape {item['title']}")
            continue
        new_checksum = compare_handle.checksum_bytes(new_bytes)

        print(f"{item['title']}. Adding to licenses collection...")
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
                "changes": None  # No previous content to compare to
            }
        )
        # Mark the tracker as scraped so it won't be processed again
        tracker_collection.update_one(
            {'_id': ref_id},
            {'$set': {'scraped': True, 'last_checked': now_millis}}
        )

        # Fetch old content from the database
        old_license = licenses_collection.find_one(
            {'tracker_ref_id': ref_id},
            sort=[('created_date', pymongo.DESCENDING)]
        )
        old_checksum = old_license.get('content_checksum') if old_license else None

    # Fetch all items from the tracker collection
    items = tracker_collection.find()
    for itemm in items:
        last_checkedd = int(itemm.get('last_checked', None))
        # frequency = int(item.get('frequency', 0))
        urll = itemm.get('url', '')
        ref_idd = itemm.get('_id')
        # Check if it's time to check this item
        # print (item['title'] + ": " + str(now_millis - last_checked))
        if last_checkedd is None or now_millis - last_checkedd >= frequency:
            print(f"Checking item: {itemm['title']}")

            if new_checksum != old_checksum:
                print(f"Content has changed for {itemm['title']}. Updating database...")
                # Save new license info to the database
                generated_filename = str(uuid.uuid4())
                scrape_handle.process_text()
                new_content = scrape_handle.content
                filepath = scrape_handle.save_to_file(urll, generated_filename)

                licenses_collection.insert_one(
                    {
                        "title": itemm['title'],
                        "created_date": now_millis,
                        "url": urll,
                        "filepath": filepath[0],
                        "filetype": scrape_handle.filetype,
                        "content": new_content,
                        "file_ref_uuid": generated_filename,
                        "content_checksum": new_checksum,
                        "tracker_ref_id": ref_idd,
                        "changes": compare_handle.compare_strings(new_content,
                                                                  old_license.get('content')) if old_license else None
                    }
                )

                # Update last_checked time in the tracker collection
            tracker_collection.update_one(
                {'_id': ref_idd},
                {'$set': {'last_checked': now_millis}}
            )
        else:
            print(f"No changes detected for {itemm['title']}.")
            tracker_collection.update_one(
                {'_id': ref_idd},
                {'$set': {'last_checked': now_millis}}
            )

    print("Tracker update complete: ", datetime.fromtimestamp(_now_millis() / 1000.0))


# To run the update function periodically, you might use a loop or a scheduler
if __name__ == "__main__":
    while True:
        update_tracker()
        time.sleep(10)  # Check every 10 seconds
