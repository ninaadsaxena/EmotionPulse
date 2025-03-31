from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import os
import logging
from modules.text_analyzer import TextAnalyzer
from modules.image_analyzer import ImageAnalyzer
from modules.dataset_handler import DatasetHandler

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize analyzers
text_analyzer = TextAnalyzer()
image_analyzer = ImageAnalyzer()
dataset_handler = DatasetHandler()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze/text', methods=['POST'])
def analyze_text():
    try:
        data = request.json
        text = data.get('text', '')
        result = text_analyzer.analyze(text)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error analyzing text: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/analyze/image', methods=['POST'])
def analyze_image():
    try:
        data = request.json
        image_data = data.get('image', '')
        
        if not image_data:
            return jsonify({"error": "No image data provided"})
        
        result = image_analyzer.analyze_image_base64(image_data)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error analyzing image: {str(e)}")
        return jsonify({"error": f"Error analyzing image: {str(e)}"}), 500

@app.route('/sample_images/<path:filename>')
def sample_image(filename):
    return send_from_directory('sample_images', filename)

@app.route('/train-model', methods=['POST'])
def train_model():
    try:
        logger.info("Starting model training...")
        history = dataset_handler.train_model()
        logger.info("Model training completed successfully")
        return jsonify({"message": "Model trained successfully", "history": history})
    except Exception as e:
        logger.error(f"Error during model training: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/evaluate-model', methods=['POST'])
def evaluate_model():
    try:
        logger.info("Starting model evaluation...")
        metrics = dataset_handler.evaluate_model()
        logger.info("Model evaluation completed successfully")
        return jsonify({"message": "Model evaluated successfully", "metrics": metrics})
    except Exception as e:
        logger.error(f"Error during model evaluation: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Create necessary directories if they don't exist
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    os.makedirs('sample_images', exist_ok=True)
    
    # Start the Flask app
    logger.info("Starting EmotionPulse server...")
    app.run(debug=True, port=5000)
