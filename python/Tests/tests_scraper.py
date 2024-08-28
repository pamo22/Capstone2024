# This test file aims to check the scraper is:
# 1. Handling bad urls (bad input, no access, etc)
# 2. Handling good urls appropriately
# 3. TBC

#Import scraper


#test url variable setting
url1 = "https://www.adobe.com/au/legal/licenses-terms.html"
url2 = ""
url3 = ""

#run tests



#Test functions

def test_url(url, expected_output){
    result = scrape(url);
    return result == expected_output
}
