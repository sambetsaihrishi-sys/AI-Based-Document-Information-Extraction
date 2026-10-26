from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

BASE_DIR = Path(__file__).resolve().parent.parent
SAMPLES_DIR = BASE_DIR / "samples"


def test_home_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "AI-Based Document Information Extraction API is running"
    }


def test_upload_without_file():
    response = client.post("/upload")
    assert response.status_code == 422


def test_invalid_file_extension():
    response = client.post(
        "/upload",
        files={
            "file": (
                "malicious.exe",
                b"This is not a valid document",
                "application/octet-stream"
            )
        }
    )

    assert response.status_code == 400


def test_empty_file():
    response = client.post(
        "/upload",
        files={
            "file": (
                "empty.png",
                b"",
                "image/png"
            )
        }
    )

    assert response.status_code == 400


def test_file_signature_mismatch():
    response = client.post(
        "/upload",
        files={
            "file": (
                "fake.pdf",
                b"This is not actually a PDF",
                "application/pdf"
            )
        }
    )

    assert response.status_code == 400


def test_successful_pan_upload():
    image_path = SAMPLES_DIR / "test_image.png"
    image_bytes = image_path.read_bytes()

    response = client.post(
        "/upload",
        files={
            "file": (
                "test_image.png",
                image_bytes,
                "image/png"
            )
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["document_type"] == "PAN"
    assert data["extracted_data"]["name"] == "RAHUL KUMAR"
    assert data["extracted_data"]["date_of_birth"] == "15/08/2000"
    assert data["extracted_data"]["pan_number"] == "ABCDE1234F"


def test_aadhaar_privacy():
    image_path = SAMPLES_DIR / "test_aadhaar.png"
    image_bytes = image_path.read_bytes()

    response = client.post(
        "/upload",
        files={
            "file": (
                "test_aadhaar.png",
                image_bytes,
                "image/png"
            )
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["document_type"] == "AADHAAR"
    assert data["extracted_data"]["name"] == "PRIYA SHARMA"
    assert data["extracted_data"]["gender"] == "Female"

    assert (
        data["extracted_data"]["aadhaar_number_masked"]
        == "XXXX XXXX 7777"
    )

    response_text = response.text

    assert "9999 8888 7777" not in response_text
    assert "999988887777" not in response_text
    assert data["extracted_text"] is None


def test_pan_raw_text_is_hidden():
    image_path = SAMPLES_DIR / "test_image.png"

    response = client.post(
        "/upload",
        files={
            "file": (
                "test_image.png",
                image_path.read_bytes(),
                "image/png"
            )
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["extracted_text"] is None
    assert data["document_type"] == "PAN"
    assert data["extracted_data"]["name"] == "RAHUL KUMAR"


def test_corrupted_image():
    corrupted_image = (
        b"\x89PNG\r\n\x1a\n"
        + b"invalid_image_data"
    )

    response = client.post(
        "/upload",
        files={
            "file": (
                "corrupted.png",
                corrupted_image,
                "image/png"
            )
        }
    )

    assert response.status_code == 422

    data = response.json()

    assert "detail" in data
    assert isinstance(data["detail"], str)
def test_corrupted_pdf():
    corrupted_pdf = b"%PDF-1.7\ninvalid_pdf_content"

    response = client.post(
        "/upload",
        files={
            "file": (
                "corrupted.pdf",
                corrupted_pdf,
                "application/pdf"
            )
        }
    )

    assert response.status_code == 422

    data = response.json()

    assert "detail" in data
    assert isinstance(data["detail"], str)
def test_blank_image():
    import io
    from PIL import Image

    image = Image.new("RGB", (500, 300), "white")

    buffer = io.BytesIO()
    image.save(buffer, format="PNG")

    response = client.post(
        "/upload",
        files={
            "file": (
                "blank.png",
                buffer.getvalue(),
                "image/png"
            )
        }
    )

    assert response.status_code == 422

    data = response.json()

    assert data["detail"] == "No readable text found in the document."