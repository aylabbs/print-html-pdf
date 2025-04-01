import logging
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import StreamingResponse
from weasyprint import HTML
import io

app = FastAPI()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/pdf")
async def generate_pdf(request: Request):
    """Accept JSON with {'html': '<html>...</html>'}."""
    logger.info("Received request to generate PDF")
    data = await request.json()
    logger.info("Parsed JSON data")
    html_content = data.get("html", "")
    logger.info("Extracted HTML content")

    pdf_bytes = HTML(string=html_content, base_url=".").write_pdf()
    logger.info("Generated PDF bytes")

    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=document.pdf"}
    )
    logger.info("Returned PDF response")

@app.post("/pdf-from-file")
async def generate_pdf_from_file(html_file: UploadFile = File(...)):
    """
    Accept a single HTML file as multipart form data.
    Example form field name: 'html_file'
    Content-Type: multipart/form-data
    """
    logger.info("Received request to generate PDF from file")
    # Read the uploaded file bytes
    uploaded_content = await html_file.read()
    logger.info("Read uploaded file bytes")
    # Decode to string (assuming UTF-8)
    html_content = uploaded_content.decode("utf-8", errors="replace")
    logger.info("Decoded HTML content")

    pdf_bytes = HTML(string=html_content, base_url=".").write_pdf()
    logger.info("Generated PDF bytes")

    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=document.pdf"}
    )
    logger.info("Returned PDF response")

@app.get("/health")
async def health():
    logger.info("Received health check request")
    return {"status": "ok"}