from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import os
import base64
import json
from modules.text_analyzer import TextAnalyzer
from modules.image_analyzer import ImageAnalyzer

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize analyzers
text_analyzer = TextAnalyzer()
image_analyzer = ImageAnalyzer()

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
    
    result = image_analyzer.analyze_image_base64(image_data)
    return jsonify(result)

@app.route('/sample_images/<path:filename>')
def sample_image(filename):
    return send_from_directory('sample_images', filename)

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    # Create necessary directories if they don't exist
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    os.makedirs('sample_images', exist_ok=True)
    
    # Start the Flask app
    print("Starting EmotionPulse server...")
    app.run(debug=True, port=5000)
