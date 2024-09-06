# This test file aims to check the scraper is:
# 1. Handling bad urls (bad input, no access, etc)
# 2. Handling good urls appropriately
# 3. TBC

#Imports
import pytest
import scraper


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


#print(test_url_list)
#bytes strings
#expected ouput = eo
# this is the output of example.com
eo1 = """<html><head>\n    <title>Example Domain</title>\n\n    <meta charset="utf-8">\n    <meta http-equiv="Content-type" content="text/html; charset=utf-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1">\n    <style type="text/css">\n    body {\n        background-color: #f0f0f2;\n        margin: 0;\n        padding: 0;\n        font-family: -apple-system, system-ui, BlinkMacSystemFont, "Segoe UI", "Open Sans", "Helvetica Neue", Helvetica, Arial, sans-serif;\n        \n    }\n    div {\n        width: 600px;\n        margin: 5em auto;\n        padding: 2em;\n        background-color: #fdfdff;\n        border-radius: 0.5em;\n        box-shadow: 2px 3px 7px 2px rgba(0,0,0,0.02);\n    }\n    a:link, a:visited {\n        color: #38488f;\n        text-decoration: none;\n    }\n    @media (max-width: 700px) {\n        div {\n            margin: 0 auto;\n            width: auto;\n        }\n    }\n    </style>    \n</head>\n\n<body>\n<div>\n    <h1>Example Domain</h1>\n    <p>This domain is for use in illustrative examples in documents. You may use this\n    domain in literature without prior coordination or asking for permission.</p>\n    <p><a href="https://www.iana.org/domains/example">More information...</a></p>\n</div>\n\n\n</body></html>""".encode()

#run tests
scraper1 = scraper.scrape_obj();

def debug():
    eo1_scrapeout = scraper1.get_text("http://example.com")
    print(eo1_scrapeout)
    print("-------------------------------------")
    print(eo1)
    print("-------------------------------------")
    print(eo1_scrapeout == eo1)
#Test functions
class TestScrape:

    #Access to internet
    def known_result_test(self):
        assert scraper1.get_text("http://example.com") == eo1


    #To be implemented:
    """
    #Inproper input cases
    def test_url_bad_input(self):
        assert scraper1.get_text("") == 0#expected_output

    #Unexpected URL behaviour cases
    def test_url_unexpected_behaviour(self):
        assert scraper1.get_text("SOMETHING HERE") == 0#expected_output

    #Known result test
    def test_scrape_result(self):
        assert scraper1.get_text("http://example.com") == 0# expected_output
    def test_internet_access(self):
    """


