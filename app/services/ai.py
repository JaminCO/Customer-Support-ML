from transformers import pipeline

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

CATEGORIES = ["general", "billing", "technical"]

def classify_text(text: str):
    try:
        result = classifier(text, CATEGORIES)
        return {
            "category": result["labels"][0],
            "confidence": round(float(result["scores"][0]), 2)
        }
    except Exception as e:
        log_error("AI_CLASSIFICATION_ERROR", str(e), "classify_text")
        return {"category": "unknown", "confidence": 0.0}

def generate_summary(text: str):
    try:
        summary = summarizer(text, max_length=30, min_length=5, do_sample=False)
        return summary[0]["summary_text"]
    except Exception as e:
        log_error("AI_SUMMARIZATION_ERROR", str(e), "generate_summary")
        return "Error generating summary."