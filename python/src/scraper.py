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
temp_url = "https://www.adobe.com/au/legal/licenses-terms.html"


#Scraper code
def scrape(url):
    driver.get(url)
    print(driver.page_source.encode("utf-8"))
    # b'<!DOCTYPE html><html xmlns="http://www....
    driver.quit()


scrape(temp_url)
