from fastapi import FastAPI, Response, HTTPException
from pydantic import BaseModel
import io, re
from html2docx import html2docx
from docx import Document

app = FastAPI(title="HTML → DOCX")

class Payload(BaseModel):
    html: str
    filename: str = "documento.docx"

# Regex simple para quitar <script> (seguridad)
SCRIPT_TAG_RE = re.compile(r"<\s*script[^>]*>.*?<\s*/\s*script\s*>", re.IGNORECASE | re.DOTALL)

@app.get("/")
def root():
    return {"status": "ok", "service": "html-to-docx", "endpoint": "/convert"}

@app.post("/convert")
def convert(payload: Payload):
    if not payload.html.strip():
        raise HTTPException(status_code=400, detail="Campo 'html' vacío")

    # 1) Limpiar HTML
    cleaned_html = re.sub(SCRIPT_TAG_RE, "", payload.html)

    # 2) Crear documento y convertir HTML
    try:
        doc = Document()
        html2docx(cleaned_html, doc)   # ✅ sin "title"
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Error en conversión: {e}")

    # 3) Guardar en memoria
    buf = io.BytesIO()
    doc.save(buf)
    buf.seek(0)

    # 4) Nombre final
    filename = payload.filename if payload.filename.endswith(".docx") else payload.filename + ".docx"
    headers = {"Content-Disposition": f'attachment; filename="{filename}"'}

    return Response(
        content=buf.read(),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers=headers
    )
