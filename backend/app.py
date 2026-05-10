"""
AutoDoc Align - Flask backend
Run:
    pip install flask flask-cors opencv-python numpy
    python app.py
Server: http://localhost:5000
"""
import os
import cv2
import numpy as np
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from io import BytesIO

from utils import scan_document

app = Flask(__name__)
CORS(app)  # allow requests from the React frontend

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "AutoDoc Align"})


@app.route("/process-document", methods=["POST"])
def process_document():
    if "image" not in request.files:
        return jsonify({"error": "No image file provided."}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "Empty filename."}), 400

    try:
        file_bytes = np.frombuffer(file.read(), np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        if img is None:
            return jsonify({"error": "Invalid or empty image."}), 400

        scanned = scan_document(img)
        if scanned is None:
            return jsonify(
                {"error": "Document not detected properly. Try a clearer image."}
            ), 422

        ok, encoded = cv2.imencode(".jpg", scanned)
        if not ok:
            return jsonify({"error": "Failed to encode output image."}), 500

        return send_file(
            BytesIO(encoded.tobytes()),
            mimetype="image/jpeg",
            as_attachment=False,
            download_name="scanned.jpg",
        )
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )