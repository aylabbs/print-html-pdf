from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import StreamingResponse
from weasyprint import HTML
import io

app = FastAPI()


@app.post("/pdf")
async def generate_pdf(request: Request):
    """Accept JSON with {'html': '<html>...</html>'}."""
    data = await request.json()
    html_content = data.get("html", "")
    pdf_bytes = HTML(string=html_content, base_url=".").write_pdf()
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=document.pdf"}
    )

@app.post("/pdf-from-file")
async def generate_pdf_from_file(html_file: UploadFile = File(...)):
    """
    Accept a single HTML file as multipart form data.
    Example form field name: 'html_file'
    Content-Type: multipart/form-data
    """
    # Read the uploaded file bytes
    uploaded_content = await html_file.read()
    # Decode to string (assuming UTF-8)
    html_content = uploaded_content.decode("utf-8", errors="replace")
    pdf_bytes = HTML(string=html_content, base_url=".").write_pdf()

    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=document.pdf"}
    )

@app.get("/health")
async def health():
    return {"status": "ok"}