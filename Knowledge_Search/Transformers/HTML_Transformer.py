import requests
import trafilatura
from bs4 import BeautifulSoup
from Knowledge_Search.Transformers.Transformer import Transformer

class HTML_Transformer(Transformer):

    def __get_text_from_page__(self, url):
        text = ""
        try:
            html = requests.get(url).text
            text = trafilatura.extract(html)
        except Exception as e:
            print(e)
        return text

    def trasnform(self, url):
        return self.__get_text_from_page__(url)