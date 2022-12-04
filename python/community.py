import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

def notices(targetUrl,page_index):
    check=0
    rsts = []
    #targetURL
    base_url=targetUrl

    #post param
    post_params = {'page':page_index}
    
    #응답 값은 response에
    res = requests.post(base_url,data=post_params)

    #응답에 실패하면
    if res.status_code != 200:
        #그냥 print
        print("Can't")
    #응답에 성공하면
    else:
        #BeautifulSoup 생성해서 soup으로 사용
        soup=BeautifulSoup(res.text,"html.parser")
        #td태그들 값을 저장(find_all)
        noTd = soup.find_all('td',class_="_noData")
        if noTd:
            return [], 0
        trs = soup.select("tbody")
        
        #headline 게시글 제거
        for tr in trs:
            trH = tr.find_all('tr',class_="headline")
        for i in range(len(trH)):
            soup.find('tr',class_="headline").decompose()
        
        tds = soup.select("td._artclTdTitle")
        tds2 = soup.select("td._artclTdRdate")
        for td, td2 in zip(tds, tds2):
            #td 중 a태그 추출
            anchors = td.find_all('a')
            #추출한 a태그 정제
            for anchor in anchors:
            
                if anchor['href'][0]=='h':
                    link = anchor['href']
                else:
                    link = f"https://www.bu.ac.kr{anchor['href']}"

                #a태그 속 title이 저장된 span태그 find하기
                title = anchor.find('span')
                if not title: continue
                date = td2.text
                rst={
                    'title':title.string,
                    'link':link,
                    'date':date
                }
                rsts.append(rst)
                check = 1
    return rsts, check

def upload():
  dic = {
    "대학공지사항" : ["web", 3484],
    "학사공지사항" : ["web", 4782],
    "취업진로지원처 공지사항" : ["web", 4784],
    "장학 공지사항" : ["web", 4785],
    "코로나19관련 공지사항" : ["web", 4886],
    "상담센터":["coun",2368],
    "기독교학부":["cfcu", 2652],
    "어문학부":["language", 2596],
    "사회복지학부":["welfare", 2526],
    "경찰학부":["lawpublic", 2396],
    "경상학부":["biz", 2322],
    "관광학부":["tourism", 2264],
    "사범학부":["education", 2123],
    "유아교육과":["infant", 2051],
    "특수체육교육과":["sports", 1962],
    "컴공 학사공지":["info", 1787],
    "컴공 학부공지":["info", 1788],
    "물리치료학과":["dpt", 1919],
    "안경광학과":["opt", 1896],
    "응급구조학과":["emt", 4544],
    "간호학과":["nurse", 1856],
    "치위생학과":["dental", 4580],
    "작업치료학과":["dot", 1829],
    "디영 학부공지":["design", 1733],
    "디영 공모전":["design", 1734],
    "스포츠과학부":["sports_sci", 1694],
    "문화예술학부":["art2", 1633],
    "혁신융합학부":["iis", 1601],
    "첨단IT학부":["smartit", 6301]
  }
  client = MongoClient('mongodb+srv://SeangG:0903@mycluster.cbbabsn.mongodb.net/?retryWrites=true&w=majority')
  db = client["test"]
  for k, v in dic.items():
    print(f"\n학부공지 크롤링 ({k})")
    
    datas = []
    i=1
    while i<=50:
        if i%10==0: print(f"page {i}")
        data, check = notices(f"https://community.bu.ac.kr/{v[0]}/{v[1]}/subview.do",i)
        
        if check == 1:
            datas+=data
            i+=1
        else:
            break
    db[k].drop()
    db[k].insert_many(datas)