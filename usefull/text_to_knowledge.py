import spacy, re

nlp = spacy.load("en_core_web_lg")

def normalize(s):
    return re.sub(r"\s+", " ", s.strip())

def extract_spacy_triples(text):
    doc = nlp(text)
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
                triples.append((normalize(subj), "is", normalize(attr)))
        if token.pos_ == "VERB":
            subj = None; obj = None
            for child in token.children:
                if child.dep_ in ("nsubj", "nsubjpass"):
                    subj = " ".join([t.text for t in child.subtree])
                if child.dep_ in ("dobj", "obj"):
                    obj = " ".join([t.text for t in child.subtree])
            if subj and obj:
                triples.append((normalize(subj), token.lemma_, normalize(obj)))
    return triples

