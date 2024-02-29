import os
from PyPDF2 import PdfWriter, PdfReader, PdfMerger


PdfFile = "scraping_club_home_page.pdf"

# split pdf into multiple pages


def split_pdf(pdf_path):
    with open(pdf_path, "rb") as f:
        reader = PdfReader(f)
        # Get all the pages
        for page_num in range(0, len(reader.pages)):
            selected_page = reader.pages[page_num]
            # Writer to Write
            writer = PdfWriter()
            writer.add_page(selected_page) # add/embed pages
            file_name = os.path.splitext(pdf_path)[0]
            outputFileName = f"{file_name}_{page_num + 1}.pdf"
            with open(outputFileName, "wb") as out:
                writer.write(out)

            print("Created a pdf: {}".format(outputFileName))


# Splitting pdf up to a page


def split_pdf_upto(pdf_path, start_page: int=0, stop_page: int=0):
    with open(pdf_path, "rb") as f:
        reader = PdfReader(f)
        writer = PdfWriter()
        for page_num in range(start_page, stop_page):
            selected_page = reader.pages[page_num]
            writer.add_page(selected_page)
            file_name = os.path.splitext(pdf_path)[0]
            outputFileName = f"{file_name}_from_{start_page}_to_{stop_page}.pdf"
            # Write the file
            with open(outputFileName, "wb") as out:
                writer.write(out)
                print(f"Created file: {outputFileName}")


# Getting last pdf page


def get_last_pdf_page(pdf_path):
    with open(pdf_path, "rb") as f:
        reader = PdfReader(f)
        writer = PdfWriter()
        selected_page = reader.pages[len(reader.pages)-1]
        writer.add_page(selected_page)
        file_name = os.path.splitext(pdf_path)[0]
        outputFileName = f"Last_{file_name}.pdf"
        # Write the file
        with open(outputFileName, "wb") as out:
            writer.write(out)
    print(f"Created File: {outputFileName}")


get_last_pdf_page(PdfFile)


# Getting any page


def get_specific_pdf_page(pdf_path, page_num: int=0):
    with open(pdf_path, "rb") as f:
        reader = PdfReader(f)
        writer = PdfWriter()
        selected_page = reader.pages[page_num]
        writer.add_page(selected_page)
        file_name = os.path.splitext(pdf_path)[0]
        outputFileName = f"{file_name}_{page_num + 1}.pdf"
        # Write the file
        with open(outputFileName, "wb") as out:
            writer.write(out)
    print(f"Created File: {outputFileName}")
