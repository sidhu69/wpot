import requests

ACCESS_TOKEN = "EAAkg8OnHOPQBP46ZAtk9KyirSfo37Gv5NZBx5ZCitR7DgEXAMj1ALseLkN3vaGDm4N2ZC6GfiRIIVHZA7tm3plgZC4DQQHyi0ciONt0D5dU8hvzsZAHwwW8u5IaHteesPYFUP9JnuP1vuY8KZCzfb1e1ZBiHAZCJauto8ZAWiJDZBxg0UGZB6WML0OlZBn80DrD4kMQZBSJmwZDZD"
PHONE_NUMBER_ID = "851654494696380"
TO = "919478372154"  # 👈 your WhatsApp number with country code (no +)

url = f"https://graph.facebook.com/v21.0/{PHONE_NUMBER_ID}/messages"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

data = {
    "messaging_product": "whatsapp",
    "to": TO,
    "type": "text",
    "text": {"body": "Hello World!"}
}

response = requests.post(url, headers=headers, json=data)
print(response.status_code)
print(response.text)
