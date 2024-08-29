# This test file aims to check the scraper is:
# 1. Handling bad urls (bad input, no access, etc)
# 2. Handling good urls appropriately
# 3. TBC

#Imports
import pytest
from scraper import scrape


#test url variable setting
url1 = "https://www.adobe.com/au/legal/licenses-terms.html"
url2 = ""
url3 = ""

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



