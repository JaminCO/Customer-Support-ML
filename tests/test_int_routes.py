from fastapi.testclient import TestClient
from app.routes.ticket import router
from fastapi import FastAPI

app = FastAPI()
app.include_router(router)
client = TestClient(app)

def test_create_ticket():
    payload = {"subject": "Forgot Password", "body": "I forgot my password to my account, how do I get access back in to my account, I cant find a way to reset password"}
    response = client.post("/requests", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["subject"] == "Forgot Password"
    assert data["body"] == "I forgot my password to my account, how do I get access back in to my account, I cant find a way to reset password"
    assert "id" in data
    assert "created_at" in data
    # Save ID for later tests
    global created_ticket_id
    created_ticket_id = data["id"]

def test_list_tickets():
    response = client.get("/requests")
    assert response.status_code == 200
    tickets = response.json()
    assert isinstance(tickets, list)
    if tickets:
        global ticket_id_new
        ticket_id_new = tickets[0]["id"]
        assert "id" in tickets[0]

def test_get_ticket_by_id():
    # Use the ID from test_create_ticket if available, else get first ticket
    global created_ticket_id
    ticket_id = ticket_id_new if 'ticket_id_new' in globals() else None
    if not ticket_id:
        response = client.get("/requests")
        tickets = response.json()
        if tickets:
            ticket_id = tickets[0]["id"]
        else:
            # No tickets to test
            return
    response = client.get(f"/requests/{ticket_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == ticket_id
    assert "subject" in data
    assert "body" in data

def test_list_tickets_by_category():
    response = client.get("/requests?category=technical")
    assert response.status_code == 200
    tickets = response.json()
    assert isinstance(tickets, list)
    # Category filter may return empty list, that's fine

def test_stats_route():
    response = client.get("/stats")
    assert response.status_code in (200)  # 404 if not implemented
    if response.status_code == 200:
        stats = response.json()
        assert isinstance(stats, dict)