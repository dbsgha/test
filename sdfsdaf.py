import pandas as pd
import requests
import json
import numpy as np
from operator import itemgetter


class RawDataProcessor:

    def new(cls, path: str):
        if not hasattr(cls, "_instance"):
            cls._instance = super().new(cls)
        return cls._instance

    def __init__(self, path: str):
        self.__NAMES_INDEX = None
        self.PATH = path
        self.DATA = pd.read_csv(self.PATH)
        self.DATA.reset_index(drop=True, inplace=True)

    def getBookNames(self) -> pd.Series:
        if self.NAMES_INDEX is None:
            self.NAMES_INDEX = self.DATA["original_title"].copy()

        return self.NAMES_INDEX.copy()

    def getBookInfo(self, name: str) -> pd.Series:
        return self.DATA[self.DATA["original_title"] == name]
    
    def aladin_sample():
        url = "http://www.aladin.co.kr/ttb/api/test/ItemSearch_20131101.js"
        res = requests.get(url)
        item = json.loads(res.text)['item']
        book_list = []
        for item in item:
            book = {}
            book['title'] = item['title']
            book['author'] = item['author']
            book['description'] = item['description']
            book['link'] = item['link']
            book_list.append(book)
        return book_list

#results 페이지당 출력 개수
#search_type 검색어 종류 (keyword(키워드), title(제목), Author(작가), Publisher(출판사))
#books 검색 대상 Mall (Book, Foreign, eBook, All)
#cid 카테고리 검색 https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fimage.aladin.co.kr%2Fimg%2Ffiles%2Faladin_Category_CID_20210927.xls&wdOrigin=BROWSELINK
    def aladin(results = 10, search_type = "title", books = "book", cid = 0):
        TTBKey = "afaffafasaf"  #api 키
        url = f"http://www.aladin.co.kr/ttb/api/ItemSearch.aspx?ttbkey={TTBKey}&Query=aladdin&QueryType={search_type}&MaxResults={results}&start=1&SearchTarget={books}&CategoryId={cid}&output=js&Version=20131101"
        res = requests.get(url)
        item = json.loads(res.text)['item']
        book_list = []
        for item in item:
            book_list['title'] = item['title']
            book_list['author'] = item['author']
            book_list.append(book_list)
        return book_list
    
def book_sort(book_lists):
    books = sorted(book_lists, key=itemgetter('title', 'author', 'description', 'link'))
    books = np.array(books)
    return books



print(book_sort(RawDataProcessor.aladin_sample()))


