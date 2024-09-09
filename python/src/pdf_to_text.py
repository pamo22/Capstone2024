import pdfplumber

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

# Example usage:
pdf_to_text("files/Appendix_1_Global_English_20231205 (11).pdf", "2.txt")