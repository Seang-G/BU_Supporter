from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import requests
import re
from pymongo import MongoClient

def crawl():
  # 페이지 수를 알고 싶습니다.
  url = "https://volunteer.bu.ac.kr/volunteer/2261/subview.do?page=1"
  html = urlopen(url)
  back = bs(html,"html.parser")
  aa = back.find('a', attrs={"class": "_last"})
  number = re.findall(r'\d', aa["href"])
  number= int(number[0])

  data = []
  for j in range(1,number+1):
      url = f"https://volunteer.bu.ac.kr/volunteer/2261/subview.do?page={j}"
      html = urlopen(url)
      back = bs(html,"html.parser")

      noTd = back.find_all('td',class_="_noData")
      if noTd:
          return [], 0
      trs = back.select("tbody")
      
      #headline 게시글 제거
      for tr in trs:
          trH = tr.find_all('tr',class_="headline")
      for i in range(len(trH)):
          back.find('tr',class_="headline").decompose()

      aa = back.find_all('a', attrs={"class": "artclLinkView"})
      bb = back.find_all('td', attrs={"class": "_artclTdRdate"})
      
      for i in range(len(aa)): # 중복되는 부분을 제외하고 반복문을 돌려줍니다!
          data.append({"title": aa[i].text.strip(), "link": "https://volunteer.bu.ac.kr" + aa[i]['href'], "date": bb[i].text})
  return data

def upload():
    print("\n사회봉사센터 크롤링")
    datas = crawl()
    client = MongoClient('mongodb+srv://SeangG:0903@mycluster.cbbabsn.mongodb.net/?retryWrites=true&w=majority')
    db = client["test"]
    db["사회봉사센터"].drop()
    db["사회봉사센터"].insert_many(datas)
