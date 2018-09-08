#!/usr/bin/env python
# coding: utf-8

import requests
from bs4 import BeautifulSoup
import ssl, urllib.request
import traceback

URL = "https://search.naver.com/search.naver"

#검색조건
values = {
    'where':'news',
    'ie':'utf8',
    'sm':'tab_hty.top',
    'query':'9와숫자들',
    'oquery':'%229와숫자들%22'
}

#https://search.naver.com/search.naver?sm=tab_hty.top&where=news&query=%229와숫자들%22&oquery=%229와숫자들%22&tqi=THKHAdpySEsssbsSh5lssssssvK-520476
#https://search.naver.com/search.naver?sm=tab_hty.top&where=news&query=9와숫자들&oquery=%229와숫자들%22&tqi=THKHydpySE4ssauFdsRssssst7R-483663

headers = {'User-Agent': 'Mozilla/5.0'}

context = ssl._create_unverified_context()

def get_html(url):
    _html = ""
    resp = requests.get(url, headers=headers)
    #print(resp)
    if resp.status_code == 200:
        _html = resp.text

    return _html

def parse_html(html):
    """
    입력받은 웹툰 페이지 html에서 회차, 제목, url을 추출하여 tuble로 만들고,
    리스트에 갯수대로 저장하여 반환한다
    :param html: string
    :return: 네이버뉴스 검색 결과가 담긴 리스트
    """
    news_list = list()
    soup = BeautifulSoup(html, 'html.parser')
    news_area = soup.find("div"
            , {"class": "news mynews section"}
            ).find_all("dl")

    for news_index in news_area:
        title_area = news_index.find("dt")
        news_info_area = news_index.find("dd", {"class":"txt_inline"})
        #_news_src = news_info_area.find("span", {"class" : "_sp_each_source"}).get_text()
        _text_area = news_index.find_all("dd")

        for _text in _text_area:
            if _text.find("span", {"class": "_sp_each_source"}) == None:
                _new_txt = _text.get_text()
            else:
                _news_src = _text.find("span", {"class": "_sp_each_source"}).get_text()

        info_soup = title_area.find("a")

        _url = info_soup["href"]
        #_text = info_soup["title"]
        _title = info_soup["title"]
        #print(_title)

        # _num = _text[0]
        # if len(_text) > 1:
        #     _title = _text[1]
        news_list.append((_title, _url, _news_src, _new_txt))
    return news_list

def do_main():
    query_string = urllib.parse.urlencode(values)
    #print(URL + '?' + query_string)
    html_data = get_html(URL + '?' + query_string)
    #print(html_data)
    res_parse = parse_html(html_data)
    print(res_parse)

if __name__ == "__main__":
    do_main()