from transformers import pipeline
import time

class TextAnalyzer:
    def __init__(self):
        # Print loading message
        print("Loading text sentiment analysis model...")
        start_time = time.time()
        
        # Initialize the sentiment analysis pipeline
        self.sentiment_analyzer = pipeline("sentiment-analysis")
        
        # Initialize the emotion classification pipeline
        self.emotion_classifier = pipeline("text-classification", 
                                          model="j-hartmann/emotion-english-distilroberta-base", 
                                          return_all_scores=True)
        
        print(f"Text models loaded in {time.time() - start_time:.2f} seconds")
    
    def analyze_sentiment(self, text):
        """Analyze the sentiment of the given text."""
        result = self.sentiment_analyzer(text)
        return result[0]
    
    def analyze_emotion(self, text):
        """Analyze the emotion in the given text."""
        result = self.emotion_classifier(text)
        emotions = {item['label']: item['score'] for item in result[0]}
        return emotions
    
    def analyze(self, text):
        """Perform complete text analysis including sentiment and emotion."""
        if not text or text.strip() == "":
            return {
                "error": "Empty text provided"
            }
        
        try:
            sentiment = self.analyze_sentiment(text)
            emotions = self.analyze_emotion(text)
            
            # Find the dominant emotion
            dominant_emotion = max(emotions.items(), key=lambda x: x[1])
            
            return {
                "sentiment": {
                    "label": sentiment["label"],
                    "score": sentiment["score"]
                },
                "emotions": emotions,
                "dominant_emotion": {
                    "label": dominant_emotion[0],
                    "score": dominant_emotion[1]
                }
            }
        except Exception as e:
            return {
                "error": str(e)
            }
