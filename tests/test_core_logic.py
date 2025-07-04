from scripts.seed_db import map_category

def test_map_category_technical():
    assert map_category("Technical Support") == "technical"
    assert map_category("IT Support") == "technical"

def test_map_category_billing():
    assert map_category("Billing") == "billing"
    assert map_category("Payments") == "billing"

def test_map_category_general():
    assert map_category("General Inquiry") == "general"
    assert map_category("") == "general"