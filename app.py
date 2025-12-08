from flask import Flask, request, jsonify
from ultralytics import YOLO
from PIL import Image, UnidentifiedImageError
import numpy as np
import io

app = Flask(__name__)

MODEL_PATH = "runs/classify/train/weights/best.pt"
model = YOLO(MODEL_PATH)

CLASS_TO_VALUE = { 
                    0: 100000,
                    1: None
                  }

THRESH = 0.75


def read_img(byte_data):
    img = Image.open(io.BytesIO(byte_data)).convert("RGB")
    return np.array(img)


@app.route("/detect", methods=["POST"])
def detect():
    # cek parameter file
    if "file" not in request.files:
        return jsonify({"detected": False, "error": "no file uploaded"}), 400

    f = request.files["file"]

    # baca bytes
    img_bytes = f.read()
    if len(img_bytes) == 0:
        return jsonify({"detected": False, "error": "empty file"}), 400

    # convert jpg to numpy
    try:
        img = read_img(img_bytes)
    except UnidentifiedImageError:
        return jsonify({"detected": False, "error": "invalid image"}), 400

    # inference
    results = model(img)
    r = results[0]

    probs = r.probs
    cls_id = int(probs.top1)
    conf = float(probs.top1conf)

    if conf < THRESH:
        return jsonify({
            "detected": False,
            "confidence": conf
        })

    nominal = CLASS_TO_VALUE.get(cls_id)

    return jsonify({
        "detected": True,
        "class_index": cls_id,
        "nominal": nominal,
        "confidence": conf
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
