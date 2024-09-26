import os
import urllib.request, time, chardet, hashlib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse
from bson import ObjectId  # Import ObjectId for MongoDB


class ScrapeObj:

    def __init__(self, db):
        self.content = ""
        self.filetype = ""
        self.ready = False
        self.db = db

    def _fetch_pdf(self, url: str) -> bytes:
        response = urllib.request.urlopen(url)
        content = response.read()
        return content

    def _fetch_html(self, url: str) -> bytes:
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 ...")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)
        self.driver.get(url)
        content = self.driver.page_source.encode("utf-8")
        self.driver.quit()
        return content

    def create_scraper(self, url: str, title: str, frequency: int, tags: list) -> dict:
        # Extract the filename from the URL
        filenames = self.extract_filename_from_url(url)

        # Download the file directly from the URL
        file_path = self.download_file(url, filenames, directory="static/scraped_files")

        # Calculate checksum (for example, using MD5) for content verification
        content_checksum = "checksum"

        # Create an entry in the 'tracker' collection and get the ObjectId (tracker_ref_id)
        tracker_ref_id = self.create_license(title, url, file_path, content_checksum, tags)

        scraped_data = {
            "l_id": tracker_ref_id,
            "title": title,
            "url": url,
            "frequency": frequency,  # Frequency the license is checked in milliseconds
            "last_checked": self.now_millis(),  # Time the license was last checked in milliseconds
            "added_on": self.now_millis(),  # Time this was added to the db in milliseconds
            "tags": tags  # List of tags that will make the license searchable
        }
        self.db.scraper.insert_one(scraped_data)

        return scraped_data

    def create_license(self, title: str, url: str, file_path: str, checksum: str, tags: list) -> ObjectId:
        # Use chardet to detect encoding
        detected_encoding = chardet.detect(self.content)['encoding']

        # If no encoding is detected, fallback to a default
        if detected_encoding is None:
            detected_encoding = 'utf-8'  # Fallback to utf-8, or use 'ISO-8859-1' if needed

        self.content = self.content.decode(detected_encoding, errors='replace')

        license_data = {
            "title": title,
            "created_date": self.now_millis(),
            "url": url,
            "filepath": file_path,  # Full path of the file
            "file_ref_uuid": "ObjectId",
            "filetype": self.filetype,  # HTML or PDF
            'content': self.content,
            "content_checksum": checksum,  # Store checksum for validation
            "tags": tags
        }

        # Insert into the 'licenses' collection and return the inserted ObjectId
        result = self.db.licenses.insert_one(license_data)
        return result.inserted_id

    def extract_filename_from_url(self, url: str) -> str:
        parsed_url = urlparse(url)
        path = parsed_url.path

        # Get the last part of the path (the filename)
        filename = os.path.basename(path)

        # If the path doesn't have a valid filename, provide a default one
        if not filename:
            filename = f"file_{int(time.time())}"  # Default file name if not present in URL

        return filename

    def download_file(self, url: str, filename: str, directory: str = "static/scraped_files"):
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Define the full file path (directory + filename)
        file_path = os.path.join(directory, filename)

        try:
            # Download the file and save it to the directory
            print(f"Downloading file from {url}...")
            urllib.request.urlretrieve(url, file_path)
            print(f"File downloaded and saved at: {file_path}")
        except Exception as e:
            print(f"Failed to download file: {e}")

    def now_millis(self) -> int:
        """
        Return the current time in milliseconds.
        """
        return int(time.time() * 1000)

    def get_text(self, url: str) -> None:
        file_extension = url.split('.')[-1]
        if file_extension == "pdf":
            self.content = self._fetch_pdf(url)
            self.filetype = "pdf"
        else:
            self.content = self._fetch_html(url)
            self.filetype = "html"
