from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_webhook():
    payload = {
        "Ticker":     "ADAUSD",
        "Interval":   "4h",
        "Time_Alert": "2025-06-04 20:00:00",
        "Order":      "buy"
    }
    r = client.post("/alarms/webhook", json=payload)
    assert r.status_code == 200
    print(r.json())


if __name__ == "__main__":
    test_webhook()
