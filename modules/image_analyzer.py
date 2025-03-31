from deepface import DeepFace
import cv2
import numpy as np
import base64
import os
import time
from PIL import Image
import io
import logging
import json

logger = logging.getLogger(__name__)

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.float32, np.float64, np.int64, np.int32)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NumpyEncoder, self).default(obj)

class ImageAnalyzer:
    def __init__(self):
        logger.info("Initializing image sentiment analysis...")
        
    def analyze_image_base64(self, base64_image):
        try:
            logger.info("Analyzing image from base64 string")
            
            if "base64," in base64_image:
                base64_image = base64_image.split("base64,")[1]
            
            image_data = base64.b64decode(base64_image)
            image = Image.open(io.BytesIO(image_data))
            
            temp_path = "temp_image.jpg"
            image.save(temp_path)
            logger.info(f"Temporary image saved to {temp_path}")
            
            try:
                result = DeepFace.analyze(img_path=temp_path, actions=['emotion'], enforce_detection=False)
                logger.info("Image analysis completed successfully")
                processed_result = self._process_result(result)
            except Exception as e:
                logger.error(f"DeepFace analysis error: {str(e)}")
                processed_result = {"error": f"No face detected in the image or analysis failed: {str(e)}"}
            
            if os.path.exists(temp_path):
                os.remove(temp_path)
                logger.info(f"Temporary file {temp_path} removed")
                
            return processed_result
        except Exception as e:
            logger.error(f"Error analyzing image from base64: {str(e)}")
            if os.path.exists("temp_image.jpg"):
                os.remove("temp_image.jpg")
            return {"error": f"Error analyzing image: {str(e)}"}
    
    def _process_result(self, result):
        try:
            if isinstance(result, list):
                result = result[0]
            
            emotions = result.get('emotion', {})
            
            # Convert NumPy values to Python native types
            emotions_dict = {}
            for emotion, value in emotions.items():
                emotions_dict[emotion] = float(value)
            
            dominant_emotion = max(emotions_dict.items(), key=lambda x: x[1])
            
            logger.info(f"Dominant emotion detected: {dominant_emotion[0]} ({dominant_emotion[1]:.2f})")
            
            processed_result = {
                "emotions": emotions_dict,
                "dominant_emotion": {
                    "label": dominant_emotion[0],
                    "score": float(dominant_emotion[1])
                }
            }
            
            # Use the custom JSON encoder to handle NumPy types
            return json.loads(json.dumps(processed_result, cls=NumpyEncoder))
        except Exception as e:
            logger.error(f"Error processing analysis result: {str(e)}")
            return {"error": f"Error processing result: {str(e)}"}
