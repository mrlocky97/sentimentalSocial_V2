from transformers import pipeline

class NLPService:
    def __init__(self):
        self._sentiment_pipeline = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english"
        )

    def analyze_sentiment(self, text: str) -> dict:
        result = self._sentiment_pipeline(text)[0]
        return {
            "label": result["label"].lower(),
            "score": result["score"] if result["label"] == "POSITIVE" else -result["score"]
        }