

class Term():

    def __init__(self, term=""):
        self.term = term
        self.term_categories = []
        self.filtered_data = {}
        self.data = {}
        self.visited_urls = []
        self.ontologyes = {}

    def __str__(self):
        return f"Term: {self.term}\nCategories: {self.term_categories}"

    def set_categories(self, categories):
        self.term_categories = categories
        for i in range(len(categories)):
            if categories[i] in self.data:
                f_cat = categories[:i].count(categories[i])
                self.data[categories[i] + f'-{f_cat+1}'] = {}
            else:
                self.data[categories[i]] = {}
