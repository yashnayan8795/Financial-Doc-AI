import spacy
nlp = spacy.blank("en")
try:
    nlp = spacy.load("data/ner_training/model-best") # Replace with actual path if model is saved elsewhere
except:
    print("⚠️ Warning: Trained model not found, loading blank 'en' model.")

def extract_entities_from_text(text):
    """
    Uses spaCy NER model to extract entities from input text.
    Returns a dictionary of entities.
    """
    doc = nlp(text)
    extracted = {}
    for ent in doc.ents:
        extracted[ent.label_] = ent.text
        return extracted