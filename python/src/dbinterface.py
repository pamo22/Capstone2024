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
        self.shandle.get_bytes(url)
        scraped_file = self.shandle.save_to_file(url, generated_filename)
        self.shandle.process_text()
        create_result = self.db.licenses.insert_one(
            {
                "title": title, #title of license
                "created_date": self._now_millis(),
                "url": url,
                "filepath": scraped_file[0], #Full file path i.e /home/user/capstone/python/data/filename
                "filetype": self.shandle.filetype, #HTML or PDF
                "content": self.shandle.content, #Content, should be plain text
                "file_ref_uuid": generated_filename,
                "content_checksum": self.c_obj.checksum_bytes(self.shandle.bytes), #Checksum
                "tracker_ref_id": ref_id, #Foreign key to corresponding tracker item
                "tags": ['dog', 'lizard', 'lion'] #tags that the license will be searchable by
             }
        )
        print(f"New Todo ID: {create_result.inserted_id}")
        return None

    #/**** Basic user actions ****/
    def add_tracker(self, title: str, url: str, frequency: int):
        #frequency should be in hours, we store time in millis so convert it
        frequency = int(frequency) * 3600000
        ref_id = ObjectId()
        self._save_license_info(title, url, ref_id)
        self.db.tracker.insert_one(
                    {
                        "_id": ref_id,
                        "title": title, #Title of license
                        "url": url,
                        "frequency": frequency, #Frequency that license is checked in milliseconds
                        "last_checked": self._now_millis(), #This is the time that the license was last checked in milliseconds
                        "added_on": self._now_millis(), #Time that this was added to the db in milliseconds
                        "tags": ['dog', 'lizard', 'lion'] #tags that the tracker will be searchable by
                     }
                )
    
    def delete_tracker_item(self, itemid):
        return self.db.tracker.delete_one({'_id': ObjectId(itemid)})

    def view_license(self, licenseid):
        selected_license = self.db.licenses.find_one({'_id': ObjectId(licenseid)})
        for element in selected_license:
            if (element == "content"):
                print("/*** CONTENT ***/")
                toShow = selected_license[element].split('\n')
                for ele in toShow:
                    print(ele)
                print("/*** END CONTENT ***/")
                continue
            print(element, ": ", selected_license[element])


    #/**** Automated functions - these exist in TUI but wont be directly called by user in PROD ****/

    def check_license_changed(self, trackerid):
    # Checks url from tracker, scrapes it, and compares scraped checksum to most recent license checksum
    # Returns bool, and returns list of differences
        if (self.shandle.bytes == ""):
                print("getting content...")
                url = self.db.tracker.find_one({"_id": ObjectId(trackerid)}).get('url')
                self.shandle.get_bytes(url)
        old_content_checksum = self.db.licenses.find_one({'tracker_ref_id': ObjectId(trackerid)}, sort=[('_id', -1)]).get('content_checksum')
        if (self.c_obj.checksum_compare_bytes_checksum(self.shandle.bytes, old_content_checksum)):
            print("No changes found")
        else:
            print("Changes found as follows: ")
            self.shandle.process_text()
            for tup in self.c_obj.compare_strings(self.shandle.content, self.get_old_content(trackerid)):
                print("line number " + str(tup[0]) + ": " + str(tup[1]))
            self.update_license(trackerid)
    
    def update_license(self, trackerid):
        #adds a new licenses, pulling all info from its tracker (used for when license change need to be logged)
        url = self.db.tracker.find_one({"_id": ObjectId(trackerid)}).get('url')
        title = self.db.tracker.find_one({"_id": ObjectId(trackerid)}).get('title')
        id = self.db.tracker.find_one({"_id": ObjectId(trackerid)}).get('_id')
        self._save_license_info(title, url, id)
        ## MAY NEED TO UPDATE FREQUENCY

    #/**** FUNCTIONS FOR TUI ****/

    # Recieve list of trackers/licenses stored in db
    def get_tracker_list(self):    
        projection = {'_id': 1, 'title': 1, 'url':1}
        query=None
        documents = self.db.tracker.find(query, projection)
        result = list(documents)
        return result
    
    def get_licenses_list(self):    
        projection = {'_id': 1, 'title': 1, 'url':1}
        query=None
        documents = self.db.licenses.find(query, projection)
        result = list(documents)
        return result

    def get_old_content(self, trackerid) -> bytes :
        return self.db.licenses.find_one({'tracker_ref_id': ObjectId(trackerid)}, sort=[('_id', -1)]).get('content')

    #List select functions should list all options, require input from user, and return selected document
    def tracker_list_select(self, function_on_select):
        print("/**** Listing Trackers ****/")
        for i,item in enumerate(self.get_tracker_list()):
                print (str(i) + ": " + item['title'] + " | " + item['url'] )
        selection = input ("please select a license to action: ")
        for i,item in enumerate(self.get_tracker_list()):
            if (i == int(selection)):
                function_on_select(item['_id'])
    
    def licenses_list_select(self, function_on_select):
        print("/**** Listing Licenses ****/")
        for i,item in enumerate(self.get_licenses_list()):
                print (str(i) + ": " + item['title'] + " | " + item['url'] )
        selection = input ("please select a license to action: ")
        for i,item in enumerate(self.get_licenses_list()):
            if (i == int(selection)):
                function_on_select(item['_id'])

    #/**** Deprecated but kept ****/

    def check_license_changed_DEPRECATED(self, trackerid) -> tuple[bool, bytes]:
    #Gets the url from tracker, scrapes it, and compares scraped checksum to most recent license checksum. 
    # Returns bool (true if same content, false otherwise), and the scraped content in bytes
        if (self.shandle.content == ""):
            print("getting content...")
            url = self.db.tracker.find_one({"_id": ObjectId(trackerid)}).get('url')
            self.shandle.get_text(url)
        old_content_checksum = self.db.licenses.find_one({'tracker_ref_id': ObjectId(trackerid)}, sort=[('_id', -1)]).get('content_checksum')
        return self.c_obj.checksum_compare_bytes_checksum(self.shandle.content, old_content_checksum), self.shandle.content

