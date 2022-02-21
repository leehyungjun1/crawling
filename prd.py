import requests, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

import time
import csv


def prd(keyword):
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument("window-size=1920x1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36")
    browser = webdriver.Chrome(options=options)

    url = "https://search.shopping.naver.com/search/all?query="+keyword+"&frm=NVSCPRO"
    browser.get(url)

    browser.execute_script("window.scrollTo(0,1080)")
    interval = 2
    prev_height = browser.execute_script("return document.body.scrollHeight")

    # 반복 수행
    while True:
        # 스크롤을 가장 아래로 내림.
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        # 페이지 로딩 대기
        time.sleep(interval)
        # 현재 문서 높이를 가져와서 저장.
        curr_height = browser.execute_script("return document.body.scrollHeight")
        if curr_height == prev_height:
            break
        prev_height = curr_height
        soup = BeautifulSoup(browser.page_source, "lxml")
        lists = soup.find_all("li", attrs={"class": "basicList_item__2XT81"})

        for list in lists:
            title = list.find("div", attrs={"class": "basicList_title__3P9Q7"}).get_text()
            price = list.find("span", attrs={"class": "price_num__2WUXn"}).get_text()
            store = list.find("a", attrs={"class": "basicList_mall__sbVax"})

            if store:
                store = store.get_text()
            else:
                continue

            link = list.find("a", attrs={"class": "basicList_link__1MaTN"})["href"]
            # data = (title + "/t" + price + "/t" + store + "/t" + link).split("/t")

            print(title, ",", price, ",", store, ",", link)

            file_data["title"] = title
            file_data["price"] = price
            file_data["store"] = store
            file_data["link"] = link
            file_data = [title, price, store, link]

            return jsonify({'prd' : file_data})