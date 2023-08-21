import requests

data = {
    'usage_user_id': 1431,
    'usage_channel_id': 24
}

url = "http://127.0.0.1:8000/api/add_usage/"

res = requests.post(url, data=data)

print(res.text)
