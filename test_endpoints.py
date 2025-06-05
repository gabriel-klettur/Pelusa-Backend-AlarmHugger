"""
Script to test API endpoints for AlarmHugger.
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8001"


def test_health():
    url = f"{BASE_URL}/server/status-server"
    try:
        resp = requests.get(url)
        print("Health status:", resp.status_code)
        print(json.dumps(resp.json(), indent=2))
    except Exception as e:
        print("Health check failed:", e)


def test_webhook():
    url = f"{BASE_URL}/alarms/webhook"
    headers = {"Content-Type": "application/json"}
    payload = {
        "Ticker": "BTCUSDT",
        "Interval": "1h",
        "Quantity": "0.01",
        "Price_Alert": "50000",
        "Time_Alert": "2025-06-05T10:00:00",
        "Order": "buy",
        "Strategy": "test_strategy"
    }
    try:
        resp = requests.post(url, headers=headers, json=payload)
        print("Webhook response:", resp.status_code)
        print(json.dumps(resp.json(), indent=2))
    except Exception as e:
        print("Webhook test failed:", e)


if __name__ == "__main__":
    print("\n--- Testing Health Endpoint ---")
    test_health()
    print("\n--- Testing Webhook Endpoint ---")
    test_webhook()
