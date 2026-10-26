from pathlib import Path

from app.ocr import extract_text_from_image

image_path = Path("samples/test_image.png")

if not image_path.is_file():
    print("Please create samples/test_image.png first.")
else:
    image_bytes = image_path.read_bytes()

    result = extract_text_from_image(image_bytes)

    print("EXTRACTED TEXT:")
    print(result)