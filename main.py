from flask import Flask, request, send_file, jsonify
from io import BytesIO
from mathml2docx import convert_html

app = Flask(__name__)

@app.route("/convert", methods=["POST"])
def convert():
    try:
        html = request.data.decode("utf-8")  # recibe el HTML puro del body

        # Crear un buffer para el DOCX
        buffer = BytesIO()

        # Convertir el HTML con MathML a DOCX
        convert_html(html, buffer)

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
