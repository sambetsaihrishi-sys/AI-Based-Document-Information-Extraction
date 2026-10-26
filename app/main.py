import os
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.ocr import extract_text_from_image
from app.pdf_extractor import extract_text_from_pdf
from app.pan_extractor import extract_pan_details
from app.aadhaar_extractor import extract_aadhaar_details
from app.document_detector import detect_document_type
from app.privacy import mask_sensitive_text
from app.config import APP_NAME, MAX_FILE_SIZE


# ==========================================
# STEP 1: CREATE FASTAPI APPLICATION
# ==========================================

app = FastAPI(
    title=APP_NAME,
    description="Extract structured information from PAN, Aadhaar, and other documents.",
    version="1.0.0"
)


# ==========================================
# STEP 2: CONFIGURE FRONTEND
# ==========================================

# Locate the main project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Locate the frontend folder
FRONTEND_DIR = BASE_DIR / "frontend"

# Serve CSS and JavaScript files
app.mount(
    "/static",
    StaticFiles(directory=str(FRONTEND_DIR)),
    name="static"
)


# ==========================================
# STEP 3: FILE UPLOAD CONFIGURATION
# ==========================================



# Supported file formats
ALLOWED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".pdf"
}


# ==========================================
# STEP 4: HOME API
# ==========================================

@app.get("/")
def home():
    return {
        "message": "AI-Based Document Information Extraction API is running"
    }


# ==========================================
# STEP 5: FRONTEND WEBSITE
# ==========================================

@app.get("/app")
def frontend_home():
    """
    Display the frontend website.
    """
    return FileResponse(FRONTEND_DIR / "index.html")


# ==========================================
# STEP 6: DOCUMENT UPLOAD API
# ==========================================

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    # Check whether a file was selected
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Please select a file."
        )

    # Check the file extension
    extension = os.path.splitext(file.filename)[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only JPG, JPEG, PNG, and PDF are allowed."
        )

    # Read the uploaded file (up to 5 MB + 1 byte)
    contents = await file.read(MAX_FILE_SIZE + 1)
    await file.close()

    # Check the file size
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File size exceeds the 5 MB limit."
        )

    # Reject empty files
    if not contents:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty."
        )

    # ==========================================
    # STEP 7: VALIDATE FILE SIGNATURE
    # ==========================================

    is_pdf = contents.startswith(b"%PDF-")

    is_png = contents.startswith(
        b"\x89PNG\r\n\x1a\n"
    )

    is_jpg = contents.startswith(
        b"\xff\xd8\xff"
    )

    valid_signature = (
        (extension == ".pdf" and is_pdf)
        or (extension == ".png" and is_png)
        or (extension in {".jpg", ".jpeg"} and is_jpg)
    )

    if not valid_signature:
        raise HTTPException(
            status_code=400,
            detail="File contents do not match the selected file type."
        )

    # ==========================================
    # STEP 8: EXTRACT TEXT FROM DOCUMENT
    # ==========================================

    try:

        # PDF document
        if extension == ".pdf":
            extracted_text = extract_text_from_pdf(contents)

        # JPG, JPEG, or PNG document
        else:
            extracted_text = extract_text_from_image(contents)

    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error)
        ) from error

    if not extracted_text or not extracted_text.strip():
        raise HTTPException(
            status_code=422,
            detail="No readable text found in the document."
        )

    # ==========================================
    # STEP 9: DETECT DOCUMENT TYPE
    # ==========================================

    document_type = "UNKNOWN"
    extracted_data = None

    if extracted_text:

        document_type = detect_document_type(extracted_text)

        # PAN card extraction
        if document_type == "PAN":

            extracted_data = extract_pan_details(
                extracted_text
            )

        # Aadhaar document extraction
        elif document_type == "AADHAAR":

            extracted_data = extract_aadhaar_details(
                extracted_text
            )

        # Other documents
        else:

            extracted_data = {
                "document_type": "UNKNOWN",
                "message": "Document type not recognized"
            }

    # STEP 10: PROTECT SENSITIVE INFORMATION

    # Do not expose raw OCR text in API responses.
    # Raw text is processed internally only.
    safe_extracted_text = None
    

    # ==========================================
    # STEP 11: RETURN STRUCTURED JSON
    # ==========================================

    return {
        "status": "success",
        "filename": file.filename,
        "file_type": extension,
        "file_size_bytes": len(contents),
        "document_type": document_type,
        "extracted_text": safe_extracted_text,
        "extracted_data": extracted_data,
        "message": "Document processing completed"
    }