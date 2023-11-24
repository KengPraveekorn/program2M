import requests

webhook_url = "http://10.51.0.113:7030/webhook"

data_to_send = {
    "message": "Hello from the sender script!",
    "some_data": 123,
    "lot" : "23XPB0003",
    "partname": "fksahfjsahflas"
}

response = requests.post(webhook_url, json=data_to_send)

print("Webhook response:", response.text)
