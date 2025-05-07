from flask import Flask, request, jsonify
from flask_cors import CORS
from ultralytics import YOLO
import cv2
import numpy as np
import os

app = Flask(__name__)
CORS(app)

# Load model
model_path = os.path.join("model", "80Yolov8.pt")
model = YOLO(model_path)

@app.route("/predict", methods=["POST"])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)

    results = model.predict(source=image, verbose=False)
    detections = []

    for box in results[0].boxes:
        detections.append({
            "confidence": float(box.conf.item()),
            "bbox": box.xyxy[0].tolist(),
            "class_id": int(box.cls.item())
        })

    return jsonify({"detections": detections})
