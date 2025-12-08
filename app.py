from flask import Flask, request, jsonify
import cv2
import numpy as np
import os

from utils.compare import compare

app = Flask(__name__)

TEMPLATES_PATH = "./templates"

# minimal score diterima
MIN_ACCEPT = 82   # nanti kamu tuning sendiri


@app.route("/detect", methods=["POST"])
def detect():
    if "file" not in request.files:
        return jsonify({"detected": False, "error": "no file"})

    # read binary → convert ke numpy cv2
    file = request.files["file"].read()
    img_np = cv2.imdecode(np.frombuffer(file, np.uint8), cv2.IMREAD_COLOR)


    best_score = 0
    best_class = None


    # loop semua template
    for filename in os.listdir(TEMPLATES_PATH):
        if not filename.lower().endswith(".png"):
            continue

        nominal = filename.split("_")[0]
        template = cv2.imread(f"{TEMPLATES_PATH}/{filename}")

        score = compare(img_np, template)

        # debug
        print(f"{filename}: {score}")

        if score > best_score:
            best_score = score
            best_class = nominal


    # jika tidak ada kecocokan
    if best_class is None or best_score < MIN_ACCEPT:
        return jsonify({
            "detected": False,
            "score": best_score,
            "value": None
        })


    # jika berhasil disamakan
    return jsonify({
        "detected": True,
        "score": best_score,
        "value": best_class
    })


if __name__ == "__main__":
    app.run("0.0.0.0", 5050, debug=True)
