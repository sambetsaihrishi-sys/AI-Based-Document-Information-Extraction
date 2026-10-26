from app.aadhaar_extractor import extract_aadhaar_details


# Synthetic checksum-valid test number
sample_text = """
GOVERNMENT OF INDIA
PRIYA SHARMA
DOB: 12/05/2001
Female
2345 6789 0124
"""

result = extract_aadhaar_details(sample_text)

print("EXTRACTED AADHAAR DETAILS:")
print(result)

assert result["document_type"] == "AADHAAR"
assert result["name"] == "PRIYA SHARMA"
assert result["aadhaar_number_masked"] == "XXXX XXXX 0124"
assert result["checksum_valid"] is True

print("\nAadhaar extraction and validation passed!")