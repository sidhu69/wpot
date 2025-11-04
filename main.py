from flask import Flask, request
import requests
import json
from config import TOKEN, PHONE_NUMBER_ID

app = Flask(__name__)

VERIFY_TOKEN = "prothonbot"  # you can change this to anything you like

# ✅ Webhook verification
@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("Webhook verified successfully.")
        return challenge
    else:
        return "Verification failed", 403


# ✅ Receive messages
@app.route("/webhook", methods=["POST"])
def receive_message():
    data = request.get_json()
    print(json.dumps(data, indent=2))

    try:
        message = data["entry"][0]["changes"][0]["value"]["messages"][0]
        sender = message["from"]
        text = message["text"]["body"]

        print(f"Message from {sender}: {text}")
        send_message(sender, f"You said: {text}")
    except Exception as e:
        print("Error:", e)

    return "ok", 200


# ✅ Function to send message
def send_message(to, message):
    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": message}
    }
    response = requests.post(url, headers=headers, json=payload)
    print("Message send status:", response.status_code)
    print(response.text)


if __name__ == "_main_":
    app.run(host="0.0.0.0", port=5000, debug=True)
