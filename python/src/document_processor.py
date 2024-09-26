import io
from bs4 import BeautifulSoup
import pdfplumber

class doc_processor_obj:

    def html_converter(self, html_bytes):
        # Opens the html file in read mode
        text = html_bytes.decode(encoding="utf-8")
        # Uses BeautifulSoup to output the raw content from the html file
        raw = BeautifulSoup(text, "html.parser")

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
    
    def pdf_to_text(self, pdf_bytes):
        #save pdf file to temp
        temp = io.BytesIO()
        temp.write(pdf_bytes)
        with pdfplumber.open(temp) as pdf:
            all_text = ""
            # Loop through each page of the PDF
            for page_number, page in enumerate(pdf.pages, start=1):
                # Extract text from the current page
                page_text = page.extract_text()
                if page_text:
                    all_text += f"\n--- Page {page_number} ---\n"
                    all_text += page_text
        return all_text
