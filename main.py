from flask import Flask, request, send_file, jsonify
from io import BytesIO
import subprocess
import tempfile
import os

app = Flask(__name__)

@app.route("/convert", methods=["POST"])
def convert():
    try:
        data = request.get_json()
        if not data or "html" not in data:
            return jsonify({"error": "Missing 'html' field in JSON"}), 400

        html_content = data["html"]

        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_html:
            tmp_html.write(html_content.encode("utf-8"))
            tmp_html.flush()

            output_docx = tmp_html.name.replace(".html", ".docx")

            # Usar pandoc para convertir
            subprocess.run(
                ["pandoc", tmp_html.name, "-o", output_docx],
                check=True
            )

            with open(output_docx, "rb") as f:
                buffer = BytesIO(f.read())

        # Limpiar temporales
        os.remove(tmp_html.name)
        os.remove(output_docx)

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
