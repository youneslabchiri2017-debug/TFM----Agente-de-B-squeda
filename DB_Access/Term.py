

class Term():

    def __init__(self, term=""):
        self.term = term
        self.term_categories = []
        self.data = {}
        self.visited_urls = []

    def __str__(self):
        return f"Term: {self.term}\nCategories: {self.term_categories}"