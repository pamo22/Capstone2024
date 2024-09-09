from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os
import urllib.request
from typing import Tuple


class scrape_obj:
    def __init__(self):
        return None
    def _fetch_pdf(self, url: str) -> Tuple[bytes, str]:
        response = urllib.request.urlopen(url)
        content = response.read()
        return content

    def _fetch_html(self, url: str) -> Tuple[bytes, str]:
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

    def save_to_file(self, url: str, filename: str) -> Tuple[str, str]:
        file_extension = url.split('.')[-1]
        if file_extension == "pdf":
            content = self._fetch_pdf(url)
            filename += ".pdf"
            to_txt(content, filename)
            return os.path.abspath(filename), str(content)
        else:
            content = self._fetch_html(url)
            filename += ".html"
            to_txt(content, filename )
            return os.path.abspath(filename), str(content)

    def get_text(self, url: str) -> Tuple[bytes, str]:
        file_extension = url.split('.')[-1]
        if file_extension == "pdf":
            return self._fetch_pdf(url)
        else:
            return self._fetch_html(url)

#output to text file (for now using as test assert)
def to_txt(bytes_string, name):
    with open('data/' + name, "wb") as text_file:
        text_file.write(bytes_string)


