from bs4 import BeautifulSoup

@app.post("/convert")
def convert(payload: Payload):
    if not payload.html.strip():
        raise HTTPException(status_code=400, detail="Campo 'html' vacío")

    # 1) Limpiar scripts
    cleaned_html = re.sub(SCRIPT_TAG_RE, "", payload.html)

    # 2) Extraer solo el body
    soup = BeautifulSoup(cleaned_html, "html.parser")
    body = soup.body or soup  # si no hay body, usamos todo
    html_content = str(body)

    # 3) Crear doc y convertir
    try:
        doc = Document()
        html2docx(html_content, doc)
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
