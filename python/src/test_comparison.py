# This test file aims to check the scraper is:
# 1. Handling bad urls (bad input, no access, etc)
# 2. Handling good urls appropriately
# 3. TBC

#Imports
import pytest
import scraper
import comparison_v2

comparehandle = compare_obj()
#test url variable setting



#expected ouput = eo
eo1

#run tests

def debug():

#Test functions
class TestCompare:

    #Access to internet
    def checksum_compare(self):
        assert scraper1.get_text("http://example.com") == eo1
        """
        print(comparehandle.checksum(file1))
        print(comparehandle.checksum(file2))
        print("COMPARING DIFF CHECKSUMS: ")
        print(comparehandle.checksum_compare(file1, file2))
        print(comparehandle.checksum_compare(file2, file1))
        assert comparehandle.checksum(file1) == comparehandle.checksum(file1)
        print("COMPARING SAME CHECKSUMS: ")
        print(comparehandle.checksum_compare(file1, file1))
        print(comparehandle.checksum_compare(file2, file2))
        """

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



