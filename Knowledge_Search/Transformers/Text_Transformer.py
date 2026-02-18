import spacy, re
from Knowledge_Search.Transformers.Transformer import Transformer

class Text_Transformer(Transformer):

    def __init__(self):
        self.nlp = spacy.load("en_core_web_lg")

    def normalize(self, s):
        return re.sub(r"\s+", " ", s.strip())

    def __extract_triples__(self, text):
        doc = self.nlp(text)
        triples = []
        for token in doc:
            if token.lemma_ == "be":
                subj = None; attr = None
                for child in token.children:
                    if child.dep_ in ("nsubj", "nsubjpass"):
                        subj = " ".join([t.text for t in child.subtree])
                    if child.dep_ in ("attr", "acomp"):
                        attr = " ".join([t.text for t in child.subtree])
                if subj and attr:
                    triples.append((self.normalize(subj), "is", self.normalize(attr)))
            if token.pos_ == "VERB":
                subj = None; obj = None
                for child in token.children:
                    if child.dep_ in ("nsubj", "nsubjpass"):
                        subj = " ".join([t.text for t in child.subtree])
                    if child.dep_ in ("dobj", "obj"):
                        obj = " ".join([t.text for t in child.subtree])
                if subj and obj:
                    triples.append((self.normalize(subj), token.lemma_, self.normalize(obj)))
        return triples

    def trasnform(self, text):
        return self.__extract_triples__(text)