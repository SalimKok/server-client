from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os 
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

messages = []

@app.route("/messages", methods=["GET"])
def get_message():
    return jsonify(messages)

@app.route("/messages", methods=["POST"])
def add_messages():
    text = request.form.get("text", "")
    image = None
    audio = None

    if 'image' in request.files:
        img_file = request.files['image']
        if img_file.filename:
            fname = secure_filename(img_file.filename)
            img_file.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
            image = fname

    if 'audio' in request.files:
        aud_file = request.files['audio']
        if aud_file.filename:
            fname = secure_filename(aud_file.filename)
            aud_file.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
            audio = fname

    messages.append({"text":text, "image":image, "audio":audio})
    return jsonify({"status":"ok", "count": len(messages)}), 201

@app.route("/uploads/<path:filename>")
def upload_file(filename):
   return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)