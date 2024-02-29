from PyPDF2 import PdfReader, PdfMerger, PdfWriter
import os


merged_pdfs_file = "./files/merged_files/final_merged_pdfs_file.pdf"

# Merging pdf files
def fetch_all_pdf_files(parent_folder: str):
    target_files = []
    for path, subdirs, files in os.walk(parent_folder):
        for name in files:
            if name.endswith(".pdf"):
                target_files.append(os.path.join(path, name))
    return target_files


pdf_list = fetch_all_pdf_files("./files/merged_files")
print(pdf_list)


def merge_pdf(list_of_pdfs, output_file_path="./files/merged_files/final_merged_pdfs_file_files.pdf"):
    merger = PdfMerger()
    with open(output_file_path, "wb") as f:
        for file in list_of_pdfs:
            merger.append(file)
            merger.write(f)


merge_pdf(pdf_list)

