from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
from modules.text_analyzer import TextAnalyzer
from modules.image_analyzer import ImageAnalyzer
from modules.dataset_handler import DatasetHandler

app = Flask(__name__)
CORS(app)

# Initialize analyzers and dataset handler
text_analyzer = TextAnalyzer()
image_analyzer = ImageAnalyzer()
dataset_handler = DatasetHandler()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze/text', methods=['POST'])
def analyze_text():
    data = request.json
    text = data.get('text', '')
    result = text_analyzer.analyze(text)
    return jsonify(result)

@app.route('/analyze/image', methods=['POST'])
def analyze_image():
    data = request.json
    image_data = data.get('image', '')
    
    if not image_data:
        return jsonify({"error": "No image data provided"})
    
    try:
        result = image_analyzer.analyze_image_base64(image_data)
        return jsonify(result)
    except Exception as e:
        app.logger.error(f"Error analyzing image: {str(e)}")
        return jsonify({"error": f"An error occurred while analyzing the image: {str(e)}"})

@app.route('/train-model', methods=['POST'])
def train_model():
    try:
        history = dataset_handler.train_model()
        return jsonify({"message": "Model trained successfully", "history": history})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/evaluate-model', methods=['POST'])
def evaluate_model():
    try:
        metrics = dataset_handler.evaluate_model()
        return jsonify({"message": "Model evaluated successfully", "metrics": metrics})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
