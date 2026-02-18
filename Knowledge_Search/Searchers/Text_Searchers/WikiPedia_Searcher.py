import requests
from Knowledge_Search.Searchers.Text_Searchers.Text_Searcher import TextSearcher

class Wikipedia_Searcher(TextSearcher):

    def __search_wikipedia_pages__(termino, n=5):
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
        results = data["query"]["search"]

        return list(map(lambda x: f"https://en.wikipedia.org/wiki/{x['title'].replace(' ', '_')}", results))

    def __obtain_text_from_pages__(urls):
        text_list = []
        for url in urls:
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
            text_list += list(map(lambda x: x['extract'], data["query"]["pages"].values()))
        return text_list

    def search(self, term):
        t_txt = ""
        for page in self.search_wikipedia_pages(term, 3):
            t_txt += self.obtain_text_from_pages(page)
        return self.transformer.trasnform(t_txt)