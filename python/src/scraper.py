from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os
import urllib.request

#Starting parameters

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

driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(10)
#Scraper code
def scrape(url):
    #is it a pdf or html
    print (url.split('.')[-1])
    if (url.split('.')[-1] == "pdf"):
        response = urllib.request.urlopen(url)    
        to_txt(response.read(), "out.pdf");
    else:
        driver.get(url)
        scraped_content = driver.page_source.encode("utf-8")
        to_txt(scraped_content, "out.html")
        driver.quit()
        return scraped_content

#output to text file (for now using as test assert)
def to_txt(bytes_string, name):
    with open(name, "wb") as text_file:
        text_file.write(bytes_string)


#Running Functions

#scrape(temp_url3)
scrape(temp_url1)
