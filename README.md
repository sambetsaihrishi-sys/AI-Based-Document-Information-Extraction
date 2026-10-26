# AI-Based Document Information Extraction

A web application that extracts structured information from Indian identity documents using Optical Character Recognition (OCR) and rule-based information extraction.

Built as a technical assignment for WeMakeScholars.

## Features

- Upload JPG, JPEG, PNG, and PDF documents.
- Extract text using Tesseract OCR.
- Extract text directly from digital PDFs using PyMuPDF.
- Process scanned PDFs using OCR.
- Automatically detect PAN and Aadhaar documents.
- Extract names, dates of birth, and document-specific fields.
- Validate Aadhaar numbers using the Verhoeff checksum algorithm.
- Mask Aadhaar numbers in API responses.
- Return structured JSON responses.
- Reject unsupported, empty, corrupted, and oversized files.
- Provide a responsive web interface.
- Run automated API tests.

## Technology Stack

| Component | Technology |
|-----------|------------|
| Backend | Python, FastAPI |
| Frontend | HTML, CSS, JavaScript |
| OCR | Tesseract, pytesseract |
| Image Processing | Pillow |
| PDF Processing | PyMuPDF |
| Testing | pytest, HTTPX |
| Configuration | python-dotenv |

## Requirements

- Python 3.11 or 3.12
- Tesseract OCR installed on your system
- pip

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/sambetsaihrishi-sys/AI-Based-Document-Information-Extraction.git
cd "AI-Based Document Information Extraction"
```

Replace `<YOUR_REPOSITORY_URL>` with the actual GitHub repository URL after publishing.

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Install Tesseract OCR

Install Tesseract OCR separately.

On Windows, a typical installation path is:

```text
C:\Program Files\Tesseract-OCR\tesseract.exe
```

Tesseract can also be used through your system's PATH.

### 5. Configure Environment Variables

Copy `.env.example` to `.env`.

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Update `TESSERACT_CMD` in `.env` to match your installation.

Example:

```dotenv
TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe
```

## Running the Application

From the project root, run:

```bash
python -m uvicorn app.main:app --reload
```

Open the web application:

http://127.0.0.1:8000/app

Interactive API documentation:

http://127.0.0.1:8000/docs

## API Endpoints

### GET /

Checks whether the API is running.

### GET /app

Opens the document upload interface.

### POST /upload

Accepts an image or PDF document and returns extracted information as JSON.

Supported extensions:

- `.jpg`
- `.jpeg`
- `.png`
- `.pdf`

Maximum upload size: 5 MB.

Maximum PDF length: 5 pages.

### Example PAN Response

```json
{
  "status": "success",
  "document_type": "PAN",
  "extracted_text": null,
  "extracted_data": {
    "name": "RAHUL KUMAR",
    "date_of_birth": "15/08/2000",
    "pan_number": "ABCDE1234F"
  },
  "message": "Document processing completed"
}
```

### Example Aadhaar Response

```json
{
  "status": "success",
  "document_type": "AADHAAR",
  "extracted_text": null,
  "extracted_data": {
    "name": "PRIYA SHARMA",
    "date_of_birth": "12/05/2001",
    "gender": "Female",
    "aadhaar_number_masked": "XXXX XXXX 7777",
    "checksum_valid": false
  },
  "message": "Document processing completed"
}
```

These are abbreviated illustrative responses using synthetic test data. Actual API responses also include file metadata.

## How It Works

1. The user uploads a document through the frontend.
2. FastAPI validates the file extension, size, and signature.
3. Image files are processed using Pillow and Tesseract OCR.
4. Digital PDFs are processed using PyMuPDF.
5. Scanned PDF pages are processed using OCR.
6. The document detector identifies PAN, Aadhaar, or an unknown type.
7. Rule-based extractors identify supported fields.
8. Aadhaar checksum validation and output masking are applied.
9. The API returns structured JSON.

## Testing

Run the API tests:

```bash
python -m pytest tests/test_api.py -v
```

The latest verified run completed with:

```text
11 passed, 1 warning
```

The warning concerns a dependency deprecation notice.

## Privacy and Security

- Aadhaar numbers are masked in API responses.
- Raw OCR text is not returned.
- Files are processed in memory by the current implementation.
- Upload size and file format restrictions are enforced.
- Corrupted files are rejected with appropriate errors.
- Test samples use synthetic identity information.
- Environment secrets are excluded through `.gitignore`.

This implementation is a demonstration project and has not undergone a production security audit.

## Limitations

- OCR accuracy depends on document quality, orientation, and text clarity.
- Field extraction uses regular expressions and heuristics, not a trained document-understanding model.
- PAN and Aadhaar are the primary supported document types.
- Other documents may be classified as `UNKNOWN` without structured extraction.
- Aadhaar checksum validation does not establish whether an identity number was officially issued.
- OCR-based character correction can produce uncertain results.
- The application is not designed to verify document authenticity.
- The OCR engine must be installed separately.

## Sample Outputs

Example responses are available in:

```text
sample_outputs/pan_response.json
sample_outputs/aadhaar_response.json
```

## Future Improvements

- Support additional document types.
- Add confidence scores for extracted fields.
- Improve OCR accuracy for low-quality images.
- Add machine-learning-based document classification.
- Add more comprehensive security and performance tests.

## Assignment

Developed for the WeMakeScholars AI-Based Document Information Extraction technical assessment.