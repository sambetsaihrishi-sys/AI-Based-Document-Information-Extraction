import re


def detect_document_type(text: str) -> str:
    """
    Identify the probable document type using OCR text.
    """

    upper_text = text.upper()

    # Check for PAN-specific information
    pan_pattern = r"\b[A-Z]{5}[0-9]{4}[A-Z]\b"

    if (
        re.search(pan_pattern, upper_text)
        or "PERMANENT ACCOUNT NUMBER" in upper_text
        or "INCOME TAX DEPARTMENT" in upper_text
    ):
        return "PAN"

    # Check for Aadhaar-specific information
    aadhaar_pattern = r"(?<!\d)[2-9]\d{3}\s?\d{4}\s?\d{4}(?!\d)"

    if (
        "AADHAAR" in upper_text
        or "UIDAI" in upper_text
        or re.search(aadhaar_pattern, upper_text)
    ):
        return "AADHAAR"

    return "UNKNOWN"