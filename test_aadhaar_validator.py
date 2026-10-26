from app.aadhaar_validator import validate_aadhaar

# Invalid examples
assert validate_aadhaar("1234 5678 9012") is False
assert validate_aadhaar("0000 0000 0000") is False
assert validate_aadhaar("9999 8888 7777") is False

# Incorrect length
assert validate_aadhaar("234567890") is False

# Letters should not be accepted
assert validate_aadhaar("ABCD EFGH IJKL") is False

print("Aadhaar validation tests passed!")
from app.aadhaar_validator import D, P, validate_aadhaar


def generate_test_number(first_11_digits):
    """
    Generate a synthetic number with a valid Verhoeff checksum.
    """

    for check_digit in range(10):
        candidate = first_11_digits + str(check_digit)

        if validate_aadhaar(candidate):
            return candidate

    raise ValueError("Could not generate a valid test number.")


# Generate a fictional checksum-valid number
test_number = generate_test_number("23456789012")

print("Synthetic test number:", test_number)

# Verify that the number passes validation
assert validate_aadhaar(test_number) is True

# Change the last digit to make the checksum invalid
invalid_last_digit = str((int(test_number[-1]) + 1) % 10)
invalid_number = test_number[:-1] + invalid_last_digit

assert validate_aadhaar(invalid_number) is False

print("Valid and invalid checksum tests passed!")