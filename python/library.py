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

def crawl_lib():
    rsts = []
    url = "https://lib.bu.ac.kr/Board?n=notice&p=1"
    html = urlopen(url)
    back = bs(html,"html.parser")

    # 끝 번호를 알고 싶어요.
    aa = back.find('a', attrs={"class": "btn btn-default page_nation_right"})
    c = aa["href"]
    number=c.lstrip("/Board?n=notice&p=")
    number = int(number)


    for page in range(1,number+1):
        if page%10==0: print(f"page {page}")
        url = f"https://lib.bu.ac.kr/Board?n=notice&p={page}"
        page_html = urlopen(url)
        page_back = bs(page_html,"html.parser")
        dds = page_back.find_all("dd")

        for indx, dd in enumerate(dds):
            dd_text = dd.text
            dd_text = clean_str(dd_text)
            date = find_date(dd_text)
            date = clean_trash(date)
            anchor = dd.find("a")
        
            rst = {
                'title': anchor.text.strip(),
                'date' : date,
                'link' : f"https://lib.bu.ac.kr{anchor['href']}"
            }
            rsts.append(rst)
    return rsts

def upload():
    print("\n도서관 크롤링")
    datas = crawl_lib()
    client = MongoClient('mongodb+srv://SeangG:0903@mycluster.cbbabsn.mongodb.net/?retryWrites=true&w=majority')
    db = client["test"]
    db["도서관"].drop()
    db["도서관"].insert_many(datas)
