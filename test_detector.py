from app.document_detector import detect_document_type


pan_text = """
INCOME TAX DEPARTMENT
RAHUL KUMAR
15/08/2000
ABCDE1234F
"""

aadhaar_text = """
GOVERNMENT OF INDIA
PRIYA SHARMA
DOB: 12/05/2001
Female
9999 8888 7777
"""

other_text = """
ABC COMPANY
Invoice Number: INV-2026-001
Total Amount: 2500
"""

print("PAN:", detect_document_type(pan_text))
print("Aadhaar:", detect_document_type(aadhaar_text))
print("Other:", detect_document_type(other_text))