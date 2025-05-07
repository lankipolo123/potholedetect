from flask import Flask, request, jsonify
from flask_cors import CORS
from ultralytics import YOLO
from PIL import Image
import io

app = Flask(__name__)
CORS(app)

# Load the YOLOv9 segmentation model
model = YOLO('models/80Yolov8.pt')

@app.route('/')
def home():
    return "✅ YOLOv9 Segmentation API is running!"

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    image = Image.open(io.BytesIO(file.read())).convert("RGB")

    results = model(image)

    # Return predictions as JSON
    return jsonify(results[0].tojson())
