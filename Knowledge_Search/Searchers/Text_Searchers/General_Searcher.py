from ddgs import DDGS
from Knowledge_Search.Searchers.Text_Searchers.Text_Searcher import TextSearcher
from Knowledge_Search.Transformers.HTML_Transformer import HTML_Transformer

class General_Searcher(TextSearcher):

    def __init__(self):
        super(General_Searcher, self).__init__()
        self.web_scrapper = HTML_Transformer()

    def __search_pages__(self, term, max_res=5):
        with DDGS() as ddgs:
            results = ddgs.text(term, max_results=max_res)
        return list(map(lambda x: x['href'], results))

    def search(self, term):
        t_txt = ""
        for url in self.__search_pages__(term):
            txt = self.web_scrapper.trasnform(url)
            if txt:
                t_txt += txt
        return self.transformer.trasnform(t_txt)