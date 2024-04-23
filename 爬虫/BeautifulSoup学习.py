# 代替re表达式 pip3 install beautifulsoup4


import requests
from bs4 import BeautifulSoup

html_doc = """

<html><head><title>学习python的正确姿势</title></head>
<body>
<p class="title"><b>小帅b的故事</b></p>

<p class="story">有一天，小帅b想给大家讲两个笑话
<a href="http://example.com/1" class="sister" id="link1">一个笑话长</a>,
<a href="http://example.com/2" class="sister" id="link2">一个笑话短</a> ,
他问大家，想听长的还是短的？</p>

<p class="story">...</p>

"""


def learn():
    soup = BeautifulSoup(html_doc, "lxml")
    # print(soup)
    print(soup.head.string)  # 学习python的正确姿势
    print(soup.p.string)  # 小帅b的故事
    print(soup.get_text())
    print(soup.find(id="link1"))
    print(soup.find_all("a"))
    for one_link in soup.find_all("a"):  # 牛啊
        print(one_link.get("href"))


def main(page):
    url = "http://bang.dangdang.com/books/fivestars/01.00.00.00.00.00-recent30-0-0-1-" + str(page)
    html = request_douban(url)
    if html is None:
        print("未获取到浏览器数据")
        return
    soup = BeautifulSoup(html, "lxml")
    # print(soup)
    book_list = soup.find(class_="bang_list clearfix bang_list_mode").find_all("li")
    for one_book in book_list:
        book_id = one_book.find(class_="list_num").string
        name = one_book.find(class_="name").string
        author = one_book.find(calss_="publisher_info")
        pic = one_book.find("a").get("href")
        star = one_book.find(class_="tuijian").string
        price = one_book.find(class_="price_n").string
        print(book_id, name, author, pic, star, price)
    # list = soup.find(class_='grid_view').find_all('li')


def request_douban(url: str):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None


if __name__ == '__main__':
    main(0)
