
class doc_processor_obj():

    def html_converter(self, html_file):
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
    
    def pdf_to_text(pdf_path, text_output_path):
    # Open the PDF file
    with pdfplumber.open(pdf_path) as pdf:
        all_text = ""
        # Loop through each page of the PDF
        for page_number, page in enumerate(pdf.pages, start=1):
            # Extract text from the current page
            page_text = page.extract_text()
            if page_text:
                all_text += f"\n--- Page {page_number} ---\n"
                all_text += page_text

    # Write the extracted text to a text file
    with open(text_output_path, 'w', encoding='utf-8') as text_file:
        text_file.write(all_text)
        print(f"Text extracted and saved to {text_output_path}")