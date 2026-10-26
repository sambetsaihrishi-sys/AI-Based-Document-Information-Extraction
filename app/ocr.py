import io
import pytesseract

from PIL import Image, ImageOps, UnidentifiedImageError
from app.config import TESSERACT_CMD


pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD

MAX_IMAGE_PIXELS = 20_000_000

Image.MAX_IMAGE_PIXELS = MAX_IMAGE_PIXELS


def extract_text_from_image(file_bytes: bytes) -> str:
    try:
        with Image.open(io.BytesIO(file_bytes)) as image:

            if image.width * image.height > MAX_IMAGE_PIXELS:
                raise ValueError(
                    "Image dimensions are too large."
                )

            image.load()

            image = ImageOps.exif_transpose(image)

            image = image.convert("L")

            extracted_text = pytesseract.image_to_string(
                image,
                lang="eng",
                config="--psm 3",
                timeout=20
            )

        return extracted_text.strip()

    except (UnidentifiedImageError, OSError) as error:
        raise ValueError(
            "Invalid or corrupted image file."
        ) from error

    except Image.DecompressionBombError as error:
        raise ValueError(
            "Image dimensions exceed the safety limit."
        ) from error

    except pytesseract.TesseractNotFoundError as error:
        raise ValueError(
            "Tesseract OCR is not installed or configured."
        ) from error

    except (pytesseract.TesseractError, RuntimeError) as error:
        raise ValueError(
            "OCR processing failed."
        ) from error