from pathlib import Path

import pymupdf

from app.pdf_extractor import extract_text_from_pdf
from app.document_detector import detect_document_type
from app.pan_extractor import extract_pan_details


# STEP 1: Locate our synthetic PAN image
image_path = Path("samples/test_image.png")

if not image_path.exists():
    raise FileNotFoundError("samples/test_image.png not found")


# STEP 2: Create a PDF containing only the image
document = pymupdf.open()

page = document.new_page(width=595, height=842)

page.insert_image(
    pymupdf.Rect(50, 100, 545, 450),
    filename=str(image_path)
)

# STEP 3: Save the scanned PDF
pdf_path = Path("samples/test_scanned_pan.pdf")

document.save(str(pdf_path))
document.close()

print("Scanned PDF created successfully!")


# STEP 4: Extract text from the scanned PDF
pdf_bytes = pdf_path.read_bytes()

extracted_text = extract_text_from_pdf(pdf_bytes)

print("\nEXTRACTED TEXT:")
print(extracted_text)


# STEP 5: Detect document type
document_type = detect_document_type(extracted_text)

print("\nDOCUMENT TYPE:")
print(document_type)


# STEP 6: Extract structured PAN details
if document_type == "PAN":
    result = extract_pan_details(extracted_text)

    print("\nEXTRACTED DETAILS:")
    print(result)