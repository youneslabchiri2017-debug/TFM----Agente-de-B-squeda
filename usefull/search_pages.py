from ddgs import DDGS

def seach_pages(term, max_res=5):
    with DDGS() as ddgs:
        results = ddgs.text(term, max_results=max_res)
    return list(map(lambda x: x['href'], results))

print(seach_pages("pokemon definition"))