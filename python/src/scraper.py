from selenium import webdriver
import selenium
import os
import errno
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
        self.p_obj = doc_processor_obj()
        self.ready = False

    def _fetch_pdf(self, url: str) -> bytes:
        response = urllib.request.urlopen(url)
        content = response.read()
        return content

    def _fetch_html(self, url: str) -> bytes:
        try:
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
        except (selenium.common.exceptions.InvalidArgumentException, selenium.common.exceptions.WebDriverException):
            print('\033[93m' + "WARNING: '" + url + "' is either invalid, or the remote server has changed!" + '\033[0m')
            return None
        return content
    # returns a tuple with the filename[0] and content[1], and filetype[2]
    def save_to_file(self, url: str, filename: str) -> Tuple[str, str]:
        file_extension = url.split('.')[-1]
        to_txt(self.bytes, filename)
        return os.path.abspath(filename), self.filetype 

    def get_bytes(self, url: str) -> None:
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
    make_sure_path_exists('data')
    with open('data/' + name, "wb") as text_file:
        text_file.write(bytes_string)



def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


