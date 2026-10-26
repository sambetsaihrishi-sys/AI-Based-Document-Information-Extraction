from app.privacy import mask_sensitive_text

sample_text = """
GOVERNMENT OF INDIA
PRIYA SHARMA
DOB: 12/05/2001
Female
9999 8888 7777
"""

masked_text = mask_sensitive_text(sample_text)

print("MASKED TEXT:")
print(masked_text)

assert "9999 8888 7777" not in masked_text
assert "XXXX XXXX 7777" in masked_text

print("\nPrivacy test passed!")