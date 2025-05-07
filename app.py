from flask import Flask, jsonify, request
from flask_cors import CORS
from ultralytics import YOLO
from PIL import Image
import io
import os

# Fix: Set YOLO config dir to prevent libGL warning
os.environ["YOLO_CONFIG_DIR"] = "/tmp"

app = Flask(__name__)
CORS(app)

model_path = os.path.join(os.getcwd(), 'models', '80Yolov8.pt')
model = YOLO(model_path)

@app.route('/')
def home():
    return "Pothole Detection API is running."

@app.route('/ping')
def ping():
    return jsonify({"status": "ok"})

def predict_image(image_bytes):
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        results = model(image)
        predictions = results[0].boxes.data.cpu().numpy()

        prediction_list = []
        for box in predictions:
            prediction = {
                'xmin': float(box[0]),
                'ymin': float(box[1]),
                'xmax': float(box[2]),
                'ymax': float(box[3]),
                'confidence': float(box[4]),
                'class_id': int(box[5]),
            }
            prediction_list.append(prediction)

        return prediction_list
    except Exception as e:
        return {"error": str(e)}

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    image_bytes = file.read()
    result = predict_image(image_bytes)

    if isinstance(result, dict) and "error" in result:
        return jsonify(result), 500

    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)