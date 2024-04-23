import urllib.request
import urllib.parse
import json
import ssl

# 普通爬虫  服务器 -> url
# res = urllib.request.urlopen("http://www.baidu.com")  # url, data(POST使用， 账号密码)， timeout
# print(res.read().decode("utf-8"))

# 欺骗爬虫 服务器 -> 中间层  -> url
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 "}

url = "https://biihu.cc//account/ajax/login_process/"
context = ssl.create_default_context()

data_dict = {
    "return_url": "https://biihu.cc/",
    "user_name": "xiaoshuaib@gmail.com",
    "password": "123456789",
    "_post_type": "ajax",
}
data = json.dumps(data_dict).encode("utf-8")
req = urllib.request.Request(url, data=data, headers=headers, method="POST")
print(req)
res = urllib.request.urlopen(req, context=context, timeout=1)
print(res.read().decode("utf-8"))
