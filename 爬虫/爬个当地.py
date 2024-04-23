import re
import requests


def main(page_id):
    url = "http://bang.dangdang.com/books/fivestars/01.00.00.00.00.00-recent30-0-0-1-" + str(page_id)
    html = request_dandan(url)
    items = parse_result(html)
    for item in items:
        print(item)


def request_dandan(url):
    try:
        res = requests.get(url)
        if res.status_code == 200:
            return res.text
    except requests.RequestException:
        return ""


def parse_result(html):
   pattern = re.compile('<li>.*?list_num.*?(\d+).</div>.*?<img src="(.*?)".*?class="name".*?title="(.*?)">.*?class="star">.*?class="tuijian">(.*?)</span>.*?class="publisher_info">.*?target="_blank">(.*?)</a>.*?class="biaosheng">.*?<span>(.*?)</span></div>.*?<p><span\sclass="price_n">&yen;(.*?)</span>.*?</li>', re.S)
   items = re.findall(pattern,html)
   for item in items:
       yield {
           'range': item[0],
           'iamge': item[1],
           'title': item[2],
           'recommend': item[3],
           'author': item[4],
           'times': item[5],
           'price': item[6]
       }


if __name__ == '__main__':
    for p_id in range(10):
        main(p_id)
