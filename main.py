from flask import Flask, request, send_file, jsonify
from io import BytesIO
from docx import Document
from mathml2docx import MathML2Docx

app = Flask(__name__)

@app.route("/convert", methods=["POST"])
def convert():
    try:
        # Recibir JSON con el campo "html"
        data = request.get_json()
        if not data or "html" not in data:
            return jsonify({"error": "Missing 'html' field in JSON"}), 400

        html = data["html"]

        # Crear documento Word
        doc = Document()

        # Convertir HTML con MathML
        conv = MathML2Docx(doc)
        conv.add_html(html)

        # Guardar en memoria
        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)

        return send_file(
            buffer,
            as_attachment=True,
            download_name="output.docx",
            mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
