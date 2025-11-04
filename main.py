import requests

ACCESS_TOKEN = "EAAkg8OnHOPQBPwFdD57KZAV95h7F9i9SlDu0Og66klZBv9z8V9HfIGRmIcVdnZBlcQnGGft0m0UE7caZAMQsWv6IovpjhMphKTHI5xVEQLkHgOYXZBTWEFejanz9vfZAZBk07uAzjjflT3ZCuBCdT6IVEpmgJfxbll1GYHvDCqVXZBicDTe0lpCqTsCyuU7OZBXytr7p9jFV6RpSpNUsQOncVkRtZCZA3IInqTXkabCJNqlccFYTEupRkOQtFTXT0grXbCugbMJGhOEpEiPO3uZB9ZCn6HAy2m"
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
