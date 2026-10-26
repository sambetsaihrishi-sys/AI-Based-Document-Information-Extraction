import re


def mask_sensitive_text(text: str) -> str:
    """
    Mask Aadhaar-like numbers in OCR text.
    """

    aadhaar_pattern = (
        r"(?<!\d)[2-9]\d{3}[\s-]?\d{4}[\s-]?\d{4}(?!\d)"
    )

    def replace_aadhaar(match):
        digits = re.sub(r"\D", "", match.group())

        return "XXXX XXXX " + digits[-4:]

    return re.sub(
        aadhaar_pattern,
        replace_aadhaar,
        text
    )