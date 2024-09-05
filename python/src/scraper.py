from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os
import urllib.request

class scrape_obj:
    driver = webdriver
    content = ""
    url = ""
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless=new") # for Chrome >= 109
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        #temporary test url
        temp_url1 = "https://www.adobe.com/au/legal/licenses-terms.html"
        temp_url2 = ""
        temp_url3 = "https://www.microfocus.com/media/documentation/micro_focus_end_user_license_agreement.pdf"
        working_dir = os.getcwd()

        chrome_options.add_experimental_option('prefs', {
        "download.default_directory": (working_dir + "/files"), #Change default directory for downloads
        "download.prompt_for_download": False, #To auto download the file
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True #It will not show PDF directly in chrome
        })
        self.driver = webdriver.Chrome(options=chrome_options)

    def save_to_file(self, url:str, filename:str):
        self.driver.implicitly_wait(10)
        #is it a pdf or html
        print (url.split('.')[-1])
        if (url.split('.')[-1] == "pdf"):
            filename = filename + "pdf"
            response = urllib.request.urlopen(url)
            to_txt(response.read(), filename);
            return os.path.abspath(filename)
        else:
            self.driver.get(url)
            filename = filename + "html"
            scraped_content = self.driver.page_source.encode("utf-8")
            to_txt(scraped_content, filename)
            self.driver.quit()
            return os.path.abspath(filename)

    def get_text(self, url:str):
        self.driver.implicitly_wait(10)
        #is it a pdf or html
        print (url.split('.')[-1])
        if (url.split('.')[-1] == "pdf"):
            response = urllib.request.urlopen(url)
            return (response.read(), "pdf")
        else:
            self.driver.get(url)
            scraped_content = self.driver.page_source.encode("utf-8")
            #to_txt(scraped_content, "out.html")
            self.driver.quit()
            return (scraped_content, "html")

    def save_to_file_and_database(self, url):
        return None

#output to text file (for now using as test assert)
def to_txt(bytes_string, name):
    with open(name, "wb") as text_file:
        text_file.write(bytes_string)


