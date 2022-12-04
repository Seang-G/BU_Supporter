import requests
from bs4 import BeautifulSoup as bs
from pymongo import MongoClient

def crwal_bee():
    # 비교과 목록 url
    url = "https://best.bu.ac.kr/Career/CareerDevelop/ProgramList.aspx"

    # 로그인/세션을 위한 헤더와 데이터
    headers = {
        "Referer": "https://best.bu.ac.kr/Main/default.aspx",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
    }
    data = {
        "pro": "1",
        "rUserid": "20171880",
        "rPW": "jiown0903!"
    }
    # 페이지(POST)
    data_page = {
        "rp":1,
    }
    # 세션 생성
    session = requests.session()
    # 요청
    session.post("https://best.bu.ac.kr/main/loginPro.aspx", headers=headers, data=data)
    res = session.post(url, data=data_page)
    
    # 비교과 프로그램 url크롤링 (12.02)
    base_link = f"https://best.bu.ac.kr/Career/CareerDevelop/ProgramView.aspx"
    datas = []
    page = 1
    data_page["rp"] = page
    res = session.post(url, data=data_page)
    soup = bs(res.text, "html.parser")
    tbody = soup.select("div.group_list")

    while tbody and page<=50:
        if page%10==0:
            print(f"page {page}")
        for tr in tbody:
            onclick = tr.attrs["onclick"].split("\'")
            title = tr.select_one("h3").text
            link = f"{base_link}?pgdx={onclick[1]}&subnum={onclick[3]}"
            date = tr.select_one("li").text.replace("신청기간 : ", "")
            datas.append({"title":title, "link":link, "date":date})

        page += 1
        data_page["rp"] = page
        res = session.post(url, data=data_page)
        soup = bs(res.text, "html.parser")
        tbody = soup.select("div.group_list")
    return datas

def upload():
    print(f"\n비교과 크롤링")
    lst = crwal_bee()
    try:
        client = MongoClient('mongodb+srv://SeangG:0903@mycluster.cbbabsn.mongodb.net/?retryWrites=true&w=majority')
        db = client.test
        db["비교과"].drop()
        db["비교과"].insert_many(lst)
        return True
    except: return False
