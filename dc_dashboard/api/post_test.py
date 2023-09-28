import requests

data = {
    'usage_user_id': 1431,
    'usage_channel_id': 24
}

data = {
    'channel_id': 1
}
print(data)
url = "http://127.0.0.1:8000/api/get_cookie/"

res = requests.post(url)

print(res.text)