import requests
from flask import Flask, request

app = Flask(_name_)

ACCESS_TOKEN = "EAAkg8OnHOPQBPwFdD57KZAV95h7F9i9SlDu0Og66klZBv9z8V9HfIGRmIcVdnZBlcQnGGft0m0UE7caZAMQsWv6IovpjhMphKTHI5xVEQLkHgOYXZBTWEFejanz9vfZAZBk07uAzjjflT3ZCuBCdT6IVEpmgJfxbll1GYHvDCqVXZBicDTe0lpCqTsCyuU7OZBXytr7p9jFV6RpSpNUsQOncVkRtZCZA3IInqTXkabCJNqlccFYTEupRkOQtFTXT0grXbCugbMJGhOEpEiPO3uZB9ZCn6HAy2m"
VERIFY_TOKEN = "prothonbot"
PHONE_NUMBER_ID = "851654494696380"

def send_whatsapp_message(to, text):
    url = f"https://graph.facebook.com/v21.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text}
    }
    response = requests.post(url, headers=headers, json=data)
    print("Message sent:", response.status_code, response.text)

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
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
                    send_whatsapp_message(phone, "Hello World 🌍")

    return "OK", 200

if _name_ == "_main_":
    app.run(host="0.0.0.0", port=5000, debug=True)
