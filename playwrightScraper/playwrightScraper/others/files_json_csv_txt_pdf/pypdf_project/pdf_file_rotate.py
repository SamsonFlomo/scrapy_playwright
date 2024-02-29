from PyPDF2 import PdfReader, PdfWriter
import os


pdf_file = "./files/Last_scraping_club_home_page.pdf"
# Rotation function


def rotate_pdf_file(pdf_path, page_num, rotation: int = 90):
    with open(pdf_path, "rb") as f:
        reader = PdfReader(f)
        writer = PdfWriter()
        writer.add_page(reader.pages[page_num])
        # Rotate
        writer.pages[page_num].rotate(rotation)
        file_name = os.path.splitext(pdf_path)[0]
        outputFileName = f"{file_name}_{rotation}_degree_rotated.pdf"
        # Write the file
        with open(outputFileName, "wb") as out:
            writer.write(out)
    print(f"Created rotated pdf file: {outputFileName}")


rotate_pdf_file(pdf_file, 0, 90)
