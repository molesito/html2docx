from fastapi import FastAPI, Response
from pydantic import BaseModel
import pypandoc
import tempfile
import os

app = FastAPI()

class HtmlPayload(BaseModel):
    html: str

@app.post("/convert")
def convert_html(payload: HtmlPayload):
    # Crear archivo temporal de salida
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_out:
        output_path = tmp_out.name

    try:
        # Convertir HTML -> DOCX
        pypandoc.convert_text(
            payload.html,
            "docx",
            format="html",
            outputfile=output_path,
            extra_args=["--standalone"]
        )

        # Leer contenido generado
        with open(output_path, "rb") as f:
            content = f.read()

        return Response(
            content,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": "attachment; filename=documento.docx"}
        )
    finally:
        if os.path.exists(output_path):
            os.remove(output_path)
