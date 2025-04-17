from transformers import pipeline
import re

class NLPService:
    def __init__(self):
        self._sentiment_pipeline = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english"
        )
    
    def clean_text(self, text: str) -> str:
        # Limpieza básica de texto
        text = re.sub(r"http\S+", "", text)  # Eliminar URLs
        text = re.sub(r"@\w+", "", text)     # Eliminar menciones
        text = re.sub(r"#", "", text)        # Eliminar hashtags
        return text.strip()
    
    def analyze_sentiment(self, text: str) -> dict:
        cleaned_text = self.clean_text(text)
        result = self._sentiment_pipeline(cleaned_text)[0]
        return {
            "label": result["label"].lower(),
            "score": result["score"] if result["label"] == "POSITIVE" else -result["score"]
        }