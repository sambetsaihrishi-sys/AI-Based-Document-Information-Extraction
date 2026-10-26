import pymupdf

from app.ocr import extract_text_from_image
from app.config import MAX_PDF_PAGES




def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extract text from text-based and scanned PDFs.
    """

    try:
        with pymupdf.open(
            stream=file_bytes,
            filetype="pdf"
        ) as document:

            # Reject password-protected PDFs
            if document.needs_pass:
                raise ValueError(
                    "Password-protected PDFs are not supported."
                )

            # Reject PDFs that are too long
            if document.page_count == 0:
                raise ValueError("The PDF contains no pages.")

            if document.page_count > MAX_PDF_PAGES:
                raise ValueError(
                    "PDF exceeds the 5-page limit."
                )

            extracted_pages = []

            for page in document:

                # STEP 1: Try extracting selectable text
                page_text = page.get_text("text").strip()

                # STEP 2: Use OCR if no text was extracted
                if not page_text:

                    # Convert PDF page into an image
                    pixmap = page.get_pixmap(
                        matrix=pymupdf.Matrix(2, 2),
                        colorspace=pymupdf.csRGB,
                        alpha=False
                    )

                    # Convert the image into PNG bytes
                    image_bytes = pixmap.tobytes("png")

                    # Extract text using Tesseract OCR
                    page_text = extract_text_from_image(
                        image_bytes
                    )

                extracted_pages.append(page_text)

            return "\n".join(extracted_pages).strip()

    except ValueError:
        raise

    except Exception as error:
        raise ValueError(
            "Unable to process the PDF document."
        ) from error