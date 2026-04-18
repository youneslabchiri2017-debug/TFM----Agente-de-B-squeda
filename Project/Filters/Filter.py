
class Filter:

    def __init__(self):
        pass

    def filter(self, terms):
        for term in terms.data.values():
            for tup in term:
                if not (terms.term in tup[0] or terms.term in tup[2]):
                    terms.filtered_data.append(tup)