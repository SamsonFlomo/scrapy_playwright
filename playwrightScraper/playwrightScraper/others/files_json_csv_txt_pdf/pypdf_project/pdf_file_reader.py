from PyPDF2 import PdfReader


# Function to get metadata
PdfFile = "files/scraping_club_home_page.pdf"


# Getting Metadata


def get_pdf_metadata(pdf_path):
    with open(pdf_path, "rb") as f:
        reader = PdfReader(f)
        info = reader.metadata
    return info


pdfMetadata = get_pdf_metadata(PdfFile)
print(pdfMetadata)


# Extracting text


def extract_text_from_pdf(pdf_path):
    with open(pdf_path, "rb") as f:
        reader = PdfReader(f)
        results = []

        for i in range(0, len(reader.pages)):
            selected_page = reader.pages[i]
            text = selected_page.extract_text()
            results.append(text)

        return " ".join(results) # Convert list to a single doc.

Data = extract_text_from_pdf(PdfFile)
print(Data)

