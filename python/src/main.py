from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

chrome_options = Options()
# chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--no-sandbox") # linux only
chrome_options.add_argument("--headless=new") # for Chrome >= 109
# chrome_options.add_argument("--headless")
# chrome_options.headless = True # also works
driver = webdriver.Chrome(options=chrome_options)
start_url = "https://www.adobe.com/au/legal/licenses-terms.html"
driver.get(start_url)
time.sleep(5)
print(driver.page_source.encode("utf-8"))
# b'<!DOCTYPE html><html xmlns="http://www....
driver.quit()
