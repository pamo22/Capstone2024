from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

#Starting parameters

chrome_options = Options()
# chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--no-sandbox") # linux only
chrome_options.add_argument("--headless=new") # for Chrome >= 109
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
# chrome_options.add_argument("--headless")
# chrome_options.headless = True # also works
driver = webdriver.Chrome(options=chrome_options)

#temporary test url
temp_url1 = "https://www.adobe.com/au/legal/licenses-terms.html"
temp_url2 = ""
temp_url3 = "http://example.com"


#Scraper code
def scrape(url):
    driver.get(url)
    scraped_content = driver.page_source.encode("utf-8")
    # b'<!DOCTYPE html><html xmlns="http://www....
    driver.quit()
    print(scraped_content)
    return scraped_content

#output to text file (for now using as test assert)
def to_txt(bytes_string):
    with open("Output.txt", "wb") as text_file:
        text_file.write(bytes_string)


#Running Functions

#scrape(temp_url3)
to_txt(scrape(temp_url3))
