from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os
import urllib.request
from typing import Tuple
from document_processor import doc_processor_obj


class scrape_obj:
    
    def __init__(self):
        self.content = ""
        self.bytes = ""
        self.filetype = ""
        self.p_obj = doc_processor_obj
        self.ready = False

    def _fetch_pdf(self, url: str) -> bytes:
        response = urllib.request.urlopen(url)
        content = response.read()
        return content

    def _fetch_html(self, url: str) -> bytes:
        chrome_options = Options()
        chrome_options.add_argument("--headless=new") # for Chrome >= 109
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        working_dir = os.getcwd()

#        chrome_options.add_experimental_option('prefs', {
#        "download.default_directory": (working_dir + "/files"), #Change default directory for downloads
#        "download.prompt_for_download": False, #To auto download the file
#        "download.directory_upgrade": True,
#        "plugins.always_open_pdf_externally": True #It will not show PDF directly in chrome
#        })
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)
        self.driver.get(url)
        content = self.driver.page_source.encode("utf-8")
        self.driver.quit()
        return content
    # returns a tuple with the filename[0] and content[1], and filetype[2]
    def save_to_file(self, url: str, filename: str) -> Tuple[str, str, str]:
        file_extension = url.split('.')[-1]
        to_txt(self.bytes, filename)
        return os.path.abspath(filename), str(self.content), self.filetype 

    def get_text(self, url: str) -> None:
        file_extension = url.split('.')[-1]
        if file_extension == "pdf":
            self.bytes = self._fetch_pdf(url)
            self.filetype = "pdf"
        else:
            self.bytes = self._fetch_html(url)
            self.filetype = "html"

    def process_text(self) -> str:
        if self.filetype == "pdf":
            self.content = self.p_obj.pdf_to_text(self.bytes)
            return self.content
        if self.filetype == "html":
            self.content = self.p_obj.html_converter(self.bytes)
            return self.content

#output to text file (for now using as test assert)
def to_txt(bytes_string, name):
    with open('data/' + name, "wb") as text_file:
        text_file.write(bytes_string)


