import requests

from Knowledge_Search.Searchers.Text_Searchers.Text_Searcher import TextSearcher

class Wikipedia_Searcher(TextSearcher):

    def __search_wikipedia_pages__(self, termino, n=5):
        url = "https://en.wikipedia.org/w/api.php"
        headers = {
            "User-Agent": "TFM-Younes/1.0 (mailto:cherno1929@gmail.com)"
        }
        params = {
            "action": "query",
            "list": "search",
            "srsearch": termino,
            "format": "json"
        }
        r = requests.get(url, params=params, headers=headers)
        data = r.json()
        results = data["query"]["search"][:n]

        return list(map(lambda x: f"https://en.wikipedia.org/wiki/{x['title'].replace(' ', '_')}", results))

    def __obtain_text_from_pages__(self, url):
        text = ""
        titulo = url.split("/wiki/")[-1]
        api_url = "https://en.wikipedia.org/w/api.php"
        headers = {"User-Agent": "TFM-Younes/1.0 (mailto:cherno1929@gmail.com)"}
        params = {
            "action": "query",
            "prop": "extracts",
            "explaintext": True,
            "titles": titulo,
            "format": "json"
        }
        data = requests.get(api_url, params=params, headers=headers).json()
        #data += reduce(lambda x, y: x['extract'] + y, data["query"]["pages"].values(), "")
        for page in data["query"]["pages"].values():
            text += page["extract"]
        return text

    def search(self, term):
        t_txt = ""
        pages = self.__search_wikipedia_pages__(term, 3)
        for page in pages:
            t_txt += self.__obtain_text_from_pages__(page)
        return self.transformer.trasnform(t_txt)