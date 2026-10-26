// Get HTML elements
const uploadForm = document.getElementById("uploadForm");
const documentFile = document.getElementById("documentFile");
const uploadButton = document.getElementById("uploadButton");
const statusMessage = document.getElementById("statusMessage");
const resultSection = document.getElementById("resultSection");
const jsonOutput = document.getElementById("jsonOutput");

// Maximum file size: 5 MB
const MAX_FILE_SIZE = 5 * 1024 * 1024;

// Supported file extensions
const ALLOWED_EXTENSIONS = [".jpg", ".jpeg", ".png", ".pdf"];

// Handle form submission
uploadForm.addEventListener("submit", async function (event) {

    // Prevent the browser from refreshing
    event.preventDefault();

    // Get the selected file
    const file = documentFile.files[0];

    // Hide previous results
    resultSection.hidden = true;
    jsonOutput.textContent = "";
    statusMessage.textContent = "";

    // Check whether a file was selected
    if (!file) {
        statusMessage.textContent = "Please select a document.";
        return;
    }

    // Check file extension
    const extension = "." + file.name.split(".").pop().toLowerCase();

    if (!ALLOWED_EXTENSIONS.includes(extension)) {
        statusMessage.textContent = "Unsupported file format.";
        return;
    }

    // Check file size
    if (file.size > MAX_FILE_SIZE) {
        statusMessage.textContent = "File size must not exceed 5 MB.";
        return;
    }

    if (file.size === 0) {
        statusMessage.textContent = "The selected file is empty.";
        return;
    }

    // Prepare the file for uploading
    const formData = new FormData();

    formData.append("file", file);

    // Disable button during processing
    uploadButton.disabled = true;
    uploadButton.textContent = "Processing...";

    statusMessage.textContent = "Extracting document information...";

    try {

        // Send document to FastAPI
        const response = await fetch("/upload", {
            method: "POST",
            body: formData
        });

        // Read JSON response
        const data = await response.json();

        // Handle API errors
        if (!response.ok) {
            throw new Error(
                typeof data.detail === "string"
                    ? data.detail
                    : "Document processing failed."
            );
        }

        // Display extraction results
        jsonOutput.textContent = JSON.stringify(data, null, 4);

        resultSection.hidden = false;

        statusMessage.textContent = "Document processed successfully!";

    } catch (error) {

        statusMessage.textContent =
            error.message || "Unable to process document.";

    } finally {

        // Re-enable button
        uploadButton.disabled = false;
        uploadButton.textContent = "Extract Information";
    }
});