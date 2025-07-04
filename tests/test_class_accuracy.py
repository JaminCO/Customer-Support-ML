from scripts.seed_db import dataset, map_category
from app.services.ai import classify_text

def test_classification_accuracy():
    correct = 0
    total = 0
    for entry in dataset:
        if entry.get("language") != "en":
            continue
        text = (entry.get("subject") or "") + " " + (entry.get("body") or "")
        expected = map_category(entry.get("queue", ""))
        predicted = classify_text(text)["category"]
        if predicted == expected:
            correct += 1
        total += 1
        if total >= 10:
            break
    assert correct / total > 0.5