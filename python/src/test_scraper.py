# This test file aims to check the scraper is:
# 1. Handling bad urls (bad input, no access, etc)
# 2. Handling good urls appropriately
# 3. TBC

#Imports
import pytest
from scraper import scrape


#test url variable setting
url1 = "https://www.adobe.com/au/legal/licenses-terms.html"
url2 = "http://example.com"
url3 = "https://www.adobe.com/content/dam/cc/en/legal/licenses-terms/pdf/CS6.pdf" # This is a big one, 471 pages

eg_badinput1 = "" #Nothing / Invalid link
eg_badinput2 = 1234567890 # not string
eg_badinput3 = "thisisnotalink*%^&(!*@&###!*(     .com" #ends with .com but isnt a link
eg_badinput4 = "" #
eg_badinput5 = "" #

test_url_list = [
    url1,
    url2,
    url3 ,
    eg_badinput1,
    eg_badinput2,
    eg_badinput3,
    eg_badinput4,
    eg_badinput5
]


print(test_url_list)
#bytes strings
#   expected ouput = eo
eo1 = b""

#run tests



#Test functions
class TestScrape:

    #Access to internet
    def test_internet_access(self):
        assert scrape("http://example.com") == expected_output

    #Inproper input cases
    def test_url_bad_input(self):
        assert scrape("") == expected_output

    #Unexpected URL behaviour cases
    def test_url_unexpected_behaviour(self):
        assert scrape("SOMETHING HERE") == expected_output

    #Known result test
    def test_scrape_result(self):
        assert scrape("http://example.com") == expected_output



