from unittest.mock import patch
from app.services import ai

def test_classify_text_success():
    with patch.object(ai, "classifier") as mock_classifier:
        mock_classifier.return_value = {"labels": ["technical"], "scores": [0.95]}
        result = ai.classify_text("My internet is down")
        assert result["category"] == "technical"
        assert result["confidence"] == 0.95

def test_generate_summary_success():
    with patch.object(ai, "summarizer") as mock_summarizer:
        mock_summarizer.return_value = [{"summary_text": "Short summary"}]
        summary = ai.generate_summary("Long text here")
        assert summary == "Short summary"