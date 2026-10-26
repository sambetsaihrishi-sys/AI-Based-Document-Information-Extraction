import re
from datetime import datetime


def extract_pan_details(text: str) -> dict:
    """
    Extract PAN number, name, and date of birth
    from OCR text.
    """

    # Split OCR text into separate lines
    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    # Find PAN number and correct common OCR mistakes

    pan_number = None

    # Match possible PAN candidates containing OCR errors
    pan_pattern = r"(?<![A-Z0-9])[A-Z0-9]{10}(?![A-Z0-9])"

    # OCR may confuse letters with numbers
    letter_to_digit = {
        "O": "0",
        "I": "1",
        "L": "1",
        "S": "5",
        "B": "8",
        "Z": "2"
    }

    digit_to_letter = {
        "0": "O",
        "1": "I",
        "5": "S",
        "8": "B",
        "2": "Z"
    }

    for match in re.finditer(pan_pattern, text.upper()):

        candidate = match.group()

        # First 5 positions must be letters
        first_part = "".join(
            digit_to_letter.get(char, char)
            for char in candidate[:5]
        )

        # Next 4 positions must be digits
        middle_part = "".join(
            letter_to_digit.get(char, char)
            for char in candidate[5:9]
        )

        # Last position must be a letter
        last_part = digit_to_letter.get(
            candidate[9],
            candidate[9]
        )

        corrected_pan = first_part + middle_part + last_part

        # Validate corrected PAN format
        if re.fullmatch(r"[A-Z]{5}[0-9]{4}[A-Z]", corrected_pan):
            pan_number = corrected_pan
            break

    # Find date of birth
    dob_pattern = r"\b\d{2}[/-]\d{2}[/-]\d{4}\b"

    dob = None

    for match in re.finditer(dob_pattern, text):
        candidate = match.group()

        try:
            datetime.strptime(
                candidate.replace("-", "/"),
                "%d/%m/%Y"
            )
            dob = candidate
            break

        except ValueError:
            continue

    # Find name
    name = None

    ignored_words = [
        "INCOME TAX",
        "DEPARTMENT",
        "GOVT",
        "GOVERNMENT",
        "INDIA",
        "PERMANENT ACCOUNT",
        "CARD",
        "DOB",
        "DATE OF BIRTH"
    ]

    for line in lines:
        upper_line = line.upper()

        if any(word in upper_line for word in ignored_words):
            continue

        if pan_number and pan_number in upper_line:
            continue

        if re.search(dob_pattern, upper_line):
            continue

        if (
            re.fullmatch(r"[A-Z][A-Z .]{2,}", upper_line)
            and len(upper_line.split()) >= 2
        ):
            name = upper_line.strip()
            break

    return {
        "document_type": "PAN",
        "name": name,
        "date_of_birth": dob,
        "pan_number": pan_number
    }