from fastapi import FastAPI, Response, HTTPException
from pydantic import BaseModel
import io, re
from html2docx import html2docx

app = FastAPI()

class Payload(BaseModel):
    html: str
    filename: str = "documento.docx"

SCRIPT_TAG_RE = re.compile(r"<\s*script[^>]*>.*?<\s*/\s*script\s*>", re.IGNORECASE | re.DOTALL)

@app.get("/")
def root():
    return {"status": "ok", "service": "html-to-docx"}

@app.post("/convert")
def convert(payload: Payload):
    if not payload.html.strip():
        raise HTTPException(status_code=400, detail="Campo 'html' vacío")

    cleaned_html = re.sub(SCRIPT_TAG_RE, "", payload.html)

    try:
        doc = html2docx(cleaned_html)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Error en conversión: {e}")

    buf = io.BytesIO()
    doc.save(buf)
    buf.seek(0)

    filename = payload.filename if payload.filename.endswith(".docx") else payload.filename + ".docx"

    headers = {"Content-Disposition": f'attachment; filename="{filename}"'}
    return Response(
        content=buf.read(),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers=headers
    )
