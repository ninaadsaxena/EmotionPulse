from transformers import pipeline
import time
import logging

logger = logging.getLogger(__name__)

class TextAnalyzer:
    def __init__(self):
        logger.info("Loading text sentiment analysis model...")
        start_time = time.time()
        
        try:
            # Initialize the sentiment analysis pipeline
            self.sentiment_analyzer = pipeline("sentiment-analysis")
            
            # Initialize the emotion classification pipeline
            self.emotion_classifier = pipeline(
                "text-classification", 
                model="j-hartmann/emotion-english-distilroberta-base", 
                return_all_scores=True
            )
            
            logger.info(f"Text models loaded in {time.time() - start_time:.2f} seconds")
        except Exception as e:
            logger.error(f"Error loading text analysis models: {str(e)}")
            raise
    
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
            return {"error": "Empty text provided"}
        
        try:
            sentiment = self.analyze_sentiment(text)
            emotions = self.analyze_emotion(text)
            
            # Find the dominant emotion
            dominant_emotion = max(emotions.items(), key=lambda x: x[1])
            
            # Create a breakdown of emotions in the text
            emotion_breakdown = []
            words = text.split()
            for i, word in enumerate(words):
                if len(word) > 3:  # Only analyze words with more than 3 characters
                    try:
                        word_emotions = self.analyze_emotion(word)
                        max_emotion = max(word_emotions.items(), key=lambda x: x[1])
                        if max_emotion[1] > 0.6:  # Only include if emotion score is significant
                            emotion_breakdown.append({
                                "word": word,
                                "position": i,
                                "emotion": max_emotion[0],
                                "score": max_emotion[1]
                            })
                    except Exception as e:
                        logger.warning(f"Could not analyze word '{word}': {str(e)}")
            
            return {
                "sentiment": {
                    "label": sentiment["label"],
                    "score": sentiment["score"]
                },
                "emotions": emotions,
                "dominant_emotion": {
                    "label": dominant_emotion[0],
                    "score": dominant_emotion[1]
                },
                "emotion_breakdown": emotion_breakdown
            }
        except Exception as e:
            logger.error(f"Error analyzing text: {str(e)}")
            return {"error": str(e)}
