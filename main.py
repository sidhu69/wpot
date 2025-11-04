import requests
from flask import Flask, request
from features.check_link import check_link_safety

app = Flask(_name_)

ACCESS_TOKEN = "EAAkg8OnHOPQBPwFdD57KZAV95h7F9i9SlDu0Og66klZBv9z8V9HfIGRmIcVdnZBlcQnGGft0m0UE7caZAMQsWv6IovpjhMphKTHI5xVEQLkHgOYXZBTWEFejanz9vfZAZBk07uAzjjflT3ZCuBCdT6IVEpmgJfxbll1GYHvDCqVXZBicDTe0lpCqTsCyuU7OZBXytr7p9jFV6RpSpNUsQOncVkRtZCZA3IInqTXkabCJNqlccFYTEupRkOQtFTXT0grXbCugbMJGhOEpEiPO3uZB9ZCn6HAy2m"
VERIFY_TOKEN = "prothonbot"
PHONE_NUMBER_ID = "851654494696380"

def send_whatsapp_message(to, text):
    url = f"https://graph.facebook.com/v24.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "text": {"body": text}
    }
    requests.post(url, headers=headers, json=data)

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return "Invalid verification token"

    data = request.get_json()
    if data and "entry" in data:
        for entry in data["entry"]:
            for change in entry.get("changes", []):
                value = change.get("value", {})
                messages = value.get("messages", [])
                for message in messages:
                    phone = message["from"]
                    text = message.get("text", {}).get("body", "").lower()

                    if text.startswith("check "):
                        url = text.split("check ", 1)[1]
                        reply = check_link_safety(url)
                        send_whatsapp_message(phone, reply)

    return "OK"
