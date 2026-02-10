import requests
import trafilatura
from bs4 import BeautifulSoup

def get_text_from_web(url):
    text = ""
    try:
        html = requests.get(url).text
        text = trafilatura.extract(html)
    except Exception as e:
        print(e)
    return text

def get_imgs(url):
    imgs = []
    try:
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html.parser')
        for img in soup.find_all('img'):
            imgs.append(img['src'])
    except Exception as e:
        print(e)
    return imgs

'''
for img in get_imgs("https://es.pinterest.com/samkellyth/pikachu/"):
    print(img)
'''