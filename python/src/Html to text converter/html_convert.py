# Html to Text converter
# Takes a html file input and returns a txt file input,
# processed appropriately for compare text function.
# Author: Benedikt Matthews
# Last Updated: 03/09/2024


# importing the library
from bs4 import BeautifulSoup


# Conversion Function, takes a local html file
# and converts the document into more readable text
# for further operations
def html_converter(html_file):
    # Opens the html file in read mode
    file = open(html_file, "r", encoding="utf-8")
    # Uses BeautifulSoup to output the raw content from the html file
    raw = BeautifulSoup(file, "html.parser")
    # Formats the soup object into a properly nested structure
    formatted = (raw.prettify(encoding="utf-8"))
    # Creates another soup object from the prettified content
    output = BeautifulSoup(formatted, "html.parser")
    # Retrieves the text from the output soup object
    text = output.get_text()

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


# Define example variable here

fLicense = "Adobe General Terms of Use.html"
nLicense = "Adobe"

# Convert html file to text
lText = html_converter(fLicense)

# Write text to file with appropriate name
writefile(nLicense, lText)
