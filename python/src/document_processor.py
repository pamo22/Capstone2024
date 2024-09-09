
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