import pymupdf

from pathlib import Path

from app.pdf_extractor import extract_text_from_pdf


# Create a sample PDF
document = pymupdf.open()

page = document.new_page()

page.insert_text(
    (72, 100),
    "INCOME TAX DEPARTMENT\n"
    "RAHUL KUMAR\n"
    "15/08/2000\n"
    "ABCDE1234F",
    fontsize=14
)

# Save the PDF inside samples
sample_path = Path("samples/test_pan.pdf")
sample_path.parent.mkdir(exist_ok=True)

document.save(str(sample_path))
document.close()


# Test extraction
pdf_bytes = sample_path.read_bytes()

result = extract_text_from_pdf(pdf_bytes)

print("EXTRACTED PDF TEXT:")
print(result)