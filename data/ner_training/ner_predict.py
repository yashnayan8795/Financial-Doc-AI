# ner_predict.py
import spacy

nlp = spacy.load("output/model-best")  # Or wherever your trained model lives

def extract_entities_from_text(text):
    doc = nlp(text)
    entities = {}
    for ent in doc.ents:
        entities[ent.label_] = ent.text
    return entities
