from flask import Flask, request
import requests
from config import TOKEN, PHONE_NUMBER_ID, VERIFY_TOKEN

app = Flask(__name__)

def send_whatsapp_message(to, text):
    """Send a WhatsApp message using Meta API"""
    url = f"https://graph.facebook.com/v21.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "text": {"body": text}
    }
    response = requests.post(url, headers=headers, json=data)
    print("Message sent:", response.status_code, response.text)


@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    """Handle webhook verification and messages"""
    if request.method == "GET":
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return "Invalid verification token", 403

    data = request.get_json()
    print("Incoming data:", data)

    if data and "entry" in data:
        for entry in data["entry"]:
            for change in entry.get("changes", []):
                value = change.get("value", {})
                messages = value.get("messages", [])
                for message in messages:
                    phone = message["from"]
                    text = message.get("text", {}).get("body", "").lower()

                    # Simple command-based system
                    if text == "hello":
                        send_whatsapp_message(phone, "Hello! I’m alive 😊")
                    elif text.startswith("weather"):
                        send_whatsapp_message(phone, "Weather feature coming soon 🌤️")
                    elif text.startswith("news"):
                        send_whatsapp_message(phone, "News feature coming soon 🗞️")
                    else:
                        send_whatsapp_message(phone, "I didn’t understand that command 🤔")

    return "OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
