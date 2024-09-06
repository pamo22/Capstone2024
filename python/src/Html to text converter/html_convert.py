# Html to Text converter
# Function takes a html file input and returns a txt file input,
# processed appropriately for compare text function.
# Author: Benedikt Matthews
# Last Updated: 06/09/2024


# importing the library
from bs4 import BeautifulSoup

from python.src.scraper import scrape_obj


# Conversion Function, takes a local html file
# and converts the document into more readable text
# for further operations

def html_converter(html_file):
    # Opens the html file in read mode
    file = open(html_file, "r", encoding="utf-8")
    # Uses BeautifulSoup to output the raw content from the html file
    raw = BeautifulSoup(file, "html.parser")

    # Rips out button text, which should practically never be relevant
    # Can add more tags here if necessary
    for script in raw(["button"]):
        script.extract()

    # Formats the soup object into a properly nested structure
    formatted = (raw.prettify(encoding="utf-8"))
    # Creates another soup object from the prettified content
    output = BeautifulSoup(formatted, "html.parser")
    # Retrieves the text from the output soup object
    text = output.get_text()

    # Breaks text into lines and removes trailing gaps
    lines = (line.strip() for line in text.splitlines())

    # Drop blank lines
    text = '\n'.join(line for line in lines if line)

    return text


# Simple file write function using the license name and retrieved text
def writefile(name, text):
    # Opens the output text file with utf-8 encoding,
    # file is named based on name input
    txtfile = open((name + ".txt"), "w", encoding="utf-8")
    # Write the text to file
    txtfile.write(text)
    # Closes file
    txtfile.close()


# Test URL
url = "https://www.oracle.com/downloads/licenses/no-fee-license.html"
# License name
name = "Oracle"

# Creates Scraper object
file = scrape_obj()

# Retrieves website information from the test_Url
html, content = file.save_to_file(url, name)

# Convert html file to text
lText = html_converter(html)

# Write text to file with appropriate name
writefile(name, lText)
