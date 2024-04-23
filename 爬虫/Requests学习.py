import requests

url = "https://api.github.com/events"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 "}
data = "key: value"

res = requests.get(url, headers=headers)   # 假装自己是浏览器
# print(res.text)
# print(res.json())
# print(res.raw.read())  # bytes 流
# print(res.headers)   # headers

requests.post('https://httpbin.org/post', data={'key': 'value'})
r = requests.put('https://httpbin.org/put', data={'key': 'value'})
print(r.text)
