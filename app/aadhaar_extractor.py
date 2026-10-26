import re
from datetime import datetime
from app.aadhaar_validator import validate_aadhaar


def extract_aadhaar_details(text: str) -> dict:

    # Split text into lines
    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    # Find Aadhaar-like 12-digit number
    aadhaar_pattern = r"(?<!\d)[2-9]\d{3}\s?\d{4}\s?\d{4}(?!\d)"

    aadhaar_match = re.search(aadhaar_pattern, text)

    masked_aadhaar = None
    checksum_valid = None

    if aadhaar_match:
        digits = re.sub(r"\D", "", aadhaar_match.group())

        # Mask the first eight digits
        masked_aadhaar = "XXXX XXXX " + digits[-4:]

        # Check Verhoeff checksum
        checksum_valid = validate_aadhaar(digits)

    # Extract date of birth
    dob = None

    dob_pattern = r"\b\d{2}[/-]\d{2}[/-]\d{4}\b"

    for match in re.finditer(dob_pattern, text):
        candidate = match.group().replace("-", "/")

        try:
            datetime.strptime(candidate, "%d/%m/%Y")
            dob = candidate
            break

        except ValueError:
            continue

    # Extract gender
    gender = None

    if re.search(r"\bFEMALE\b", text, re.IGNORECASE):
        gender = "Female"

    elif re.search(r"\bMALE\b", text, re.IGNORECASE):
        gender = "Male"

    elif re.search(r"\bTRANSGENDER\b", text, re.IGNORECASE):
        gender = "Transgender"

    # Extract probable name
    name = None

    ignored_words = [
        "GOVERNMENT",
        "INDIA",
        "AADHAAR",
        "UIDAI",
        "DOB",
        "DATE OF BIRTH",
        "YEAR OF BIRTH",
        "FEMALE",
        "MALE",
        "TRANSGENDER",
        "ENROLMENT",
        "UNIQUE IDENTIFICATION"
    ]

    for line in lines:
        upper_line = line.upper()

        if any(word in upper_line for word in ignored_words):
            continue

        if re.search(r"\d", upper_line):
            continue

        if (
            re.fullmatch(r"[A-Z][A-Z .]{2,}", upper_line)
            and len(upper_line.split()) >= 2
        ):
            name = upper_line
            break

    return {
        "document_type": "AADHAAR",
        "name": name,
        "date_of_birth": dob,
        "gender": gender,
        "aadhaar_number_masked": masked_aadhaar,
        "checksum_valid": checksum_valid
    }