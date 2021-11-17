import requests
from bs4 import BeautifulSoup
import urllib.request
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
}


def img_crawling(plusurl):
    url = f"https://music.bugs.co.kr/search/integrated?q={plusurl}"
    result = requests.get(url, headers=headers)
    soup = BeautifulSoup(result.text, "html.parser")

    img = soup.find("img", {"onerror": "bugs.utils.imgError(this);"})
    img_src = img.get("src")

    title = soup.find("div", {"class": "albumTitle"})
    title = title.find("a").string

    artist = soup.find("p", {"class": "artist"})
    artist = artist.find("a").string.strip()

    img_src = img_src.replace("/50/", "/original/")
    img_src = img_src.replace("/130/", "/original/")
    cut = img_src.split("?")

    img_url = cut[0]

    filename = artist + " - " + title

    urllib.request.urlretrieve(img_url, filename + ".jpg")

    print(filename + " 이미지 저장 성공")


def start():
    plusurl = input("검색어 : ")
    text = re.compile("[^ ㄱ-ㅣ가-힣a-zA-Z0-9]")
    plusurl = text.sub("", plusurl)
    try:
        img_crawling(plusurl)
    except:
        print(plusurl + " - 검색 실패")
    start()


print("검색어를 입력하시면 결과 중 가장 상위 앨범의 커버를 원본 사이즈로 저장합니다.")
start()
