from flask import Flask, request, jsonify
from flask_cors import CORS
from ultralytics import YOLO
import numpy as np
import cv2
import base64
from PIL import Image
import io

app = Flask(__name__)
CORS(app)
model = YOLO("80Yolov8.pt")

@app.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No image provided"}), 400

    file = request.files["image"]
    img = Image.open(file.stream).convert("RGB")
    img_array = np.array(img)

    results = model(img_array)
    detections = []

    for box in results[0].boxes:
        conf = float(box.conf[0])
        cls = int(box.cls[0])
        detections.append({"class_id": cls, "confidence": conf})

    img_annotated = results[0].plot()
    _, buffer = cv2.imencode(".jpg", img_annotated)
    encoded_image = base64.b64encode(buffer).decode("utf-8")

    return jsonify({"detections": detections, "annotated_image": encoded_image})
