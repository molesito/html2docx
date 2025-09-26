from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from io import BytesIO
from html2docx import html2docx
import os

app = FastAPI()

class ConvertRequest(BaseModel):
    html: str
    filename: str | None = "document.docx"

def safe_filename(name: str) -> str:
    cleaned = "".join(c for c in name if c.isalnum() or c in ("-", "_", "."))
    if not cleaned.lower().endswith(".docx"):
        cleaned += ".docx"
    return cleaned or "document.docx"

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/convert")
async def convert(req: ConvertRequest):
    if not req.html.strip():
        raise HTTPException(status_code=400, detail="Missing 'html' content")

    try:
        # html2docx requiere al menos html y un título
        docx_bytes = html2docx(req.html, title="Generated Document")
        buffer = BytesIO(docx_bytes)
        buffer.seek(0)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Conversion failed: {e}")

    filename = safe_filename(req.filename or "document.docx")
    headers = {"Content-Disposition": f"attachment; filename=\"{filename}\""}

    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers=headers,
    )

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
