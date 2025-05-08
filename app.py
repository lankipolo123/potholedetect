from flask import Flask, request, jsonify
from ultralytics import YOLO
import numpy as np
import cv2
import base64

app = Flask(__name__)
model = YOLO("models/80Yolov8.pt")  # or your custom .pt file

@app.route("/")
def home():
    return "YOLOv8 segmentation API is live!"

@app.route("/detect", methods=["POST"])
def detect():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    img_bytes = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(img_bytes, cv2.IMREAD_COLOR)

    # Run model
    results = model(img)[0]

    # Get detections as JSON
    detections = []
    for box in results.boxes:
        xyxy = box.xyxy.cpu().numpy().tolist()[0]
        conf = float(box.conf.cpu().numpy())
        cls = int(box.cls.cpu().numpy())
        label = model.names[cls]
        detections.append({
            "box": xyxy,
            "confidence": conf,
            "class_id": cls,
            "label": label
        })

    # Render the image with segmentation masks/labels
    plotted = results.plot()
    _, img_encoded = cv2.imencode('.jpg', plotted)
    img_base64 = base64.b64encode(img_encoded).decode('utf-8')

    return jsonify({
        "detections": detections,
        "image_base64": img_base64
    })
if __name__ == "__main__":
    app.run(debug=True, port=8000)