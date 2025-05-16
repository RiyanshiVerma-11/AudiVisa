import requests

url = "https://api.apyhub.com/sharpapi/api/v1/content/translate"
headers = {
    "apy-token": "your_real_key_here",  # Paste your key here directly
    "Content-Type": "application/json"
}
payload = {
    "content": "Hello, how are you?",
    "language": "hi",
    "voice_tone": "neutral",
    "context": ""
}

response = requests.post(url, headers=headers, json=payload)
print(response.status_code)
print(response.text)
