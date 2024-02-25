import argparse
import os
import shutil
from PyPDF2 import PdfReader, PdfWriter
from docx import Document
from PIL import Image

def embed_file_into_pdf(exe_path, pdf_path, output_path):
    # Create a new PDF file with PyPDF2
    pdf_writer = PdfWriter()

    # Read the existing PDF file
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)

        # Add each page from the existing PDF to the new PDF
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            pdf_writer.add_page(page)

        # Add the executable file to the new PDF as an attachment
        with open(exe_path, 'rb') as exe_file:
            pdf_writer.add_attachment(os.path.basename(exe_path), exe_file.read())

        # Save the new PDF
        with open(output_path, 'wb') as output_pdf:
            pdf_writer.write(output_pdf)

def embed_file_into_docx(exe_path, docx_path, output_path):
    # Copy the docx file to avoid modifications to the original
    shutil.copy(docx_path, output_path)

    # Add the executable file inside the Word document
    with open(output_path, 'ab') as docx_file:
        docx_file.write(b'\n\n')  # Add a blank line for clarity
        with open(exe_path, 'rb') as exe_file:
            docx_file.write(exe_file.read())

def embed_file_into_jpg(exe_path, jpg_path, output_path):
    # Open the existing image
    image = Image.open(jpg_path)

    # Create a new image file
    with open(output_path, 'wb') as output_jpg:
        # Add the executable file to the JPEG image metadata
        output_jpg.write(image.tobytes())
        with open(exe_path, 'rb') as exe_file:
            output_jpg.write(exe_file.read())

def main():
    parser = argparse.ArgumentParser(description='Embed an executable file into various file formats.')
    parser.add_argument('exe_path', type=str, help='Path to the executable file.')
    parser.add_argument('input_path', type=str, help='Path to the input file (PDF, DOCX, or JPG).')
    parser.add_argument('-o', '--output', type=str, help='Output path for the new file.', default='output.pdf')
    parser.add_argument('-f', '--format', choices=['pdf', 'docx', 'jpg'], default='pdf', help='Output file format.')
    args = parser.parse_args()

    # Check if the executable file exists
    if not os.path.exists(args.exe_path):
        print(f"Executable file '{args.exe_path}' not found.")
        return

    # Check if the input file exists
    if not os.path.exists(args.input_path):
        print(f"Input file '{args.input_path}' not found.")
        return

    # Embed the executable file into the specified file
    if args.format == 'pdf':
        if not args.input_path.lower().endswith('.pdf'):
            print("PDF format specified, but input file is not a PDF.")
            return
        embed_file_into_pdf(args.exe_path, args.input_path, args.output)
    elif args.format == 'docx':
        if not args.input_path.lower().endswith('.docx'):
            print("DOCX format specified, but input file is not a DOCX.")
            return
        embed_file_into_docx(args.exe_path, args.input_path, args.output)
    elif args.format == 'jpg':
        if not args.input_path.lower().endswith('.jpg'):
            print("JPG format specified, but input file is not a JPG.")
            return
        embed_file_into_jpg(args.exe_path, args.input_path, args.output)
    else:
        print("Unsupported output format specified.")
        return

    print(f"Executable '{args.exe_path}' embedded into '{args.input_path}'. New file saved as '{args.output}'.")

if __name__ == "__main__":
    main()
