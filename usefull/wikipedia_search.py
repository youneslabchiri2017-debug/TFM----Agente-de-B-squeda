import requests

def buscar_wikipedia_paginas(termino, n=5):
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

def obtener_texto_wikipedia(urls):
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


txt = obtener_texto_wikipedia(buscar_wikipedia_paginas("honey", n=1))

for info in txt:
    print(info)
    print()
    print()