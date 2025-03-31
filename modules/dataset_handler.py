import kagglehub
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from sklearn.model_selection import train_test_split
import os
import cv2
import numpy as np
import logging

logger = logging.getLogger(__name__)

class DatasetHandler:
    def __init__(self):
        try:
            logger.info("Initializing dataset handler...")
            self.dataset_path = kagglehub.dataset_download("ananthu017/emotion-detection-fer")
            logger.info(f"Dataset downloaded to: {self.dataset_path}")
            
            self.image_size = (48, 48)
            self.num_classes = 6  # Happy, Sad, Angry, Frustrated, Nervous, Excited
            self.model_path = "emotion_detection_model.h5"
        except Exception as e:
            logger.error(f"Error initializing dataset handler: {str(e)}")
            raise

    def load_dataset(self):
        try:
            logger.info("Loading dataset...")
            images = []
            labels = []
            
            emotion_dirs = [d for d in os.listdir(self.dataset_path) 
                          if os.path.isdir(os.path.join(self.dataset_path, d))]
            
            logger.info(f"Found emotion directories: {emotion_dirs}")
            
            for emotion in emotion_dirs:
                emotion_path = os.path.join(self.dataset_path, emotion)
                if os.path.isdir(emotion_path):
                    label = emotion.lower()
                    img_files = os.listdir(emotion_path)
                    logger.info(f"Loading {len(img_files)} images for emotion: {label}")
                    
                    for img_file in img_files:
                        img_path = os.path.join(emotion_path, img_file)
                        try:
                            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                            if img is not None:
                                img_resized = cv2.resize(img, self.image_size)
                                images.append(img_resized)
                                labels.append(label)
                        except Exception as e:
                            logger.warning(f"Could not load image {img_path}: {str(e)}")
            
            logger.info(f"Dataset loaded: {len(images)} images")
            
            if len(images) == 0:
                raise ValueError("No images were loaded from the dataset")
                
            images = np.array(images).reshape(-1, 48, 48, 1) / 255.0  # Normalize pixel values
            labels = np.array(labels)
            
            return images, labels
        except Exception as e:
            logger.error(f"Error loading dataset: {str(e)}")
            raise

    def preprocess_labels(self, labels):
        try:
            from sklearn.preprocessing import LabelEncoder
            from tensorflow.keras.utils import to_categorical
            
            encoder = LabelEncoder()
            encoded_labels = encoder.fit_transform(labels)
            categorical_labels = to_categorical(encoded_labels)
            
            return categorical_labels
        except Exception as e:
            logger.error(f"Error preprocessing labels: {str(e)}")
            raise

    def build_model(self):
        try:
            logger.info("Building model...")
            model = Sequential([
                Conv2D(32, (3, 3), activation='relu', input_shape=(48, 48, 1)),
                MaxPooling2D((2, 2)),
                Conv2D(64, (3, 3), activation='relu'),
                MaxPooling2D((2, 2)),
                Flatten(),
                Dense(128, activation='relu'),
                Dropout(0.5),
                Dense(self.num_classes, activation='softmax')
            ])
            
            model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
            logger.info("Model built successfully")
            
            return model
        except Exception as e:
            logger.error(f"Error building model: {str(e)}")
            raise

    def train_model(self):
        try:
            logger.info("Starting model training...")
            images, labels = self.load_dataset()
            categorical_labels = self.preprocess_labels(labels)
            
            X_train, X_val, y_train, y_val = train_test_split(images, categorical_labels, test_size=0.2)
            
            model = self.build_model()
            
            # Use fewer epochs for demonstration
            history = model.fit(
                X_train,
                y_train,
                validation_data=(X_val, y_val),
                epochs=5,  # Reduced for faster training
                batch_size=32,
                verbose=1
            )
            
            # Save the trained model
            model.save(self.model_path)
            logger.info(f"Model saved to {self.model_path}")
            
            # Convert history to serializable format
            history_dict = {}
            for key in history.history:
                history_dict[key] = [float(val) for val in history.history[key]]
                
            return history_dict
        except Exception as e:
            logger.error(f"Error training model: {str(e)}")
            raise

    def evaluate_model(self):
        try:
            logger.info("Evaluating model...")
            
            # Check if model exists
            if not os.path.exists(self.model_path):
                logger.warning("Model file not found. Training a new model first.")
                self.train_model()
            
            images, labels = self.load_dataset()
            categorical_labels = self.preprocess_labels(labels)
            
            _, X_val, _, y_val = train_test_split(images, categorical_labels, test_size=0.2)
            
            # Load the trained model
            model = tf.keras.models.load_model(self.model_path)
            
            metrics = model.evaluate(X_val, y_val)
            
            result = {"loss": float(metrics[0]), "accuracy": float(metrics[1])}
            logger.info(f"Evaluation results: {result}")
            
            return result
        except Exception as e:
            logger.error(f"Error evaluating model: {str(e)}")
            raise
