from flask import Flask, request, jsonify
from ultralytics import YOLO
import cv2
import numpy as np
from PIL import Image
import io

# mapping indeks ke nominal (sesuaikan urutan names di data.yaml)
CLASS_TO_VALUE = {
    0: 100,
    1: 200,
    2: 500,
    3: 1000,
    4: 2000,
    5: 5000,
    6: 10000,
    7: 20000,
    8: 50000,
    9: 100000
}

app = Flask(__name__)

# load model (ganti path ke model kamu)
MODEL_PATH = "model/best.pt"
model = YOLO(MODEL_PATH)

def read_image_from_bytes(bytes_data):
    img = Image.open(io.BytesIO(bytes_data)).convert("RGB")
    return np.array(img)

@app.route("/detect", methods=["POST"])
def detect():
    if "file" not in request.files:
        return jsonify({"error":"No file uploaded"}), 400

    f = request.files["file"]
    img_bytes = f.read()
    np_img = read_image_from_bytes(img_bytes)

    # inference
    results = model(np_img)  # returns list of Results objects

    # parse results[0]
    r = results[0]
    boxes = r.boxes  # Boxes object
    response_items = []
    counts = {v:0 for v in CLASS_TO_VALUE.values()}

    for box in boxes:
        cls = int(box.cls[0])          # class index
        conf = float(box.conf[0])      # confidence
        x1,y1,x2,y2 = box.xyxy[0].tolist()
        nominal = CLASS_TO_VALUE.get(cls, None)
        if nominal is None:
            continue
        counts[nominal] += 1
        response_items.append({
            "class_index": cls,
            "nominal": nominal,
            "confidence": conf,
            "bbox": [x1,y1,x2,y2]
        })

    total = sum(k*v for k,v in counts.items())

    return jsonify({
        "items": response_items,
        "counts": counts,
        "total": total
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7000, debug=True)
