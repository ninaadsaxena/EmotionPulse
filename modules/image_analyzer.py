from deepface import DeepFace
import cv2
import numpy as np
import base64
import os
import time
from PIL import Image
import io

class ImageAnalyzer:
    def __init__(self):
        print("Initializing image sentiment analysis...")
        # No need to initialize models as DeepFace loads them on demand
        
    def analyze_image_path(self, image_path):
        """Analyze emotions in an image from a file path."""
        try:
            result = DeepFace.analyze(image_path, actions=['emotion'], enforce_detection=False)
            return self._process_result(result)
        except Exception as e:
            return {"error": f"Error analyzing image: {str(e)}"}
    
    def analyze_image_base64(self, base64_image):
        """Analyze emotions in an image from base64 string."""
        try:
            # Decode base64 image
            if "base64," in base64_image:
                base64_image = base64_image.split("base64,")[1]
            
            image_data = base64.b64decode(base64_image)
            image = Image.open(io.BytesIO(image_data))
            
            # Save to a temporary file
            temp_path = "temp_image.jpg"
            image.save(temp_path)
            
            # Analyze the image
            result = DeepFace.analyze(temp_path, actions=['emotion'], enforce_detection=False)
            
            # Clean up
            if os.path.exists(temp_path):
                os.remove(temp_path)
                
            return self._process_result(result)
        except Exception as e:
            return {"error": f"Error analyzing image: {str(e)}"}
    
    def _process_result(self, result):
        """Process the DeepFace result to a standardized format."""
        if isinstance(result, list):
            result = result[0]
        
        emotions = result.get('emotion', {})
        
        # Find the dominant emotion
        dominant_emotion = max(emotions.items(), key=lambda x: x[1])
        
        return {
            "emotions": emotions,
            "dominant_emotion": {
                "label": dominant_emotion[0],
                "score": dominant_emotion[1]
            }
        }
