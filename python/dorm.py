"""
==============
함수 정의 구간
"""
def clean_str(text):
    text = text.replace("\n","")
    text = text.replace("\r","")
    text = text.replace("\t","")
    text = text.replace("\xa0","")
    
    text = text.strip()
    return text

def find_date(text):
    idx = text.find('게시일')
    if idx!=-1:
        text = text[idx+3:]
    return text

def clean_trash(text):
    idx = text.find('/')
    if idx!=-1:
        text = text[:idx]
    text = text.strip()
    
    return text
"""
==============
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
from pymongo import MongoClient

def crawl():
    rsts = []
    # 마지막 페이지의 번호를 알기 위한 코드입니다.
    url = "https://dormitory.bu.ac.kr/board/?id=notice&p=1"
    html = urlopen(url)
    back = bs(html,"html.parser")
    divs = back.find_all("div")
    page_anchors = divs[0].find_all("a")
    for page_anchor in page_anchors:
        page_link = page_anchor["href"]
        if "/board/?id=notice&p=" in page_link:
            number= page_link.lstrip("/board/?id=notice&p=")
            number = int(number)

    # 1페이지부터 위에서 알아낸 마지막 페이지를 반복문으로 돌리며 제목과 링크를 띄워줍니다.
    for page in range(1,number+1):
        url = f"https://dormitory.bu.ac.kr/board/?id=notice&p={page}"
        page_html = urlopen(url)
        page_back = bs(page_html,"html.parser")
        tbodys = page_back.find_all("tbody")
        
        tds = []
        for tbody in tbodys:
            trs = tbody.find_all("tr")
            for tr in trs:
                td = tr.find_all('td')
                tds.append(td)
        
        for td in tds:
            date = td[3].text
            date = clean_str(date)
            anchor = td[1].find('a')
            rst = {
                'title':date,
                'date':anchor.text,
                'link':f"https://dormitory.bu.ac.kr{anchor['href']}"
            }
            rsts.append(rst)
    return rsts

def upload():
    print("\n백석생활관 크롤링")
    datas = crawl()
    client = MongoClient('mongodb+srv://SeangG:0903@mycluster.cbbabsn.mongodb.net/?retryWrites=true&w=majority')
    db = client["test"]
    db["백석생활관"].drop()
    db["백석생활관"].insert_many(datas)
