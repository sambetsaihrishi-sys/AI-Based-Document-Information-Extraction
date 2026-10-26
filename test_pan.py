from app.pan_extractor import extract_pan_details

sample_text = """
INCOME TAX DEPARTMENT
RAHUL KUMAR
15/08/2000
ABCDE1234F
"""

result = extract_pan_details(sample_text)

print(result)