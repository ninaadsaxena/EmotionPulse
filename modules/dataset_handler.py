import kagglehub
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from sklearn.model_selection import train_test_split
import os
import cv2
import numpy as np

class DatasetHandler:
    def __init__(self):
        print("Downloading dataset...")
        self.dataset_path = kagglehub.dataset_download("ananthu017/emotion-detection-fer")
        print("Dataset downloaded to:", self.dataset_path)
        
        self.image_size = (48, 48)
        self.num_classes = 6  # Happy, Sad, Angry, Frustrated, Nervous, Excited

    def load_dataset(self):
        images = []
        labels = []
        
        for emotion in os.listdir(self.dataset_path):
            emotion_path = os.path.join(self.dataset_path, emotion)
            if os.path.isdir(emotion_path):
                label = emotion.lower()
                for img_file in os.listdir(emotion_path):
                    img_path = os.path.join(emotion_path, img_file)
                    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                    img_resized = cv2.resize(img, self.image_size)
                    images.append(img_resized)
                    labels.append(label)
        
        images = np.array(images).reshape(-1, 48, 48, 1) / 255.0  # Normalize pixel values
        labels = np.array(labels)
        
        return images, labels

    def preprocess_labels(self, labels):
        from sklearn.preprocessing import LabelEncoder
        from tensorflow.keras.utils import to_categorical
        
        encoder = LabelEncoder()
        encoded_labels = encoder.fit_transform(labels)
        categorical_labels = to_categorical(encoded_labels)
        
        return categorical_labels

    def build_model(self):
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
        
        return model

    def train_model(self):
        images, labels = self.load_dataset()
        categorical_labels = self.preprocess_labels(labels)
        
        X_train, X_val, y_train, y_val = train_test_split(images, categorical_labels, test_size=0.2)
        
        model = self.build_model()
        
        history = model.fit(
            X_train,
            y_train,
            validation_data=(X_val, y_val),
            epochs=10,
            batch_size=32,
            verbose=1
        )
        
        # Save the trained model
        model.save("emotion_detection_model.h5")
        
        return history.history

    def evaluate_model(self):
        images, labels = self.load_dataset()
        categorical_labels = self.preprocess_labels(labels)
        
        X_train, X_val, y_train, y_val = train_test_split(images, categorical_labels, test_size=0.2)
        
        # Load the trained model
        model = tf.keras.models.load_model("emotion_detection_model.h5")
        
        metrics = model.evaluate(X_val, y_val)
        
        return {"loss": metrics[0], "accuracy": metrics[1]}
