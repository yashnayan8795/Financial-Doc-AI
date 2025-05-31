import spacy

nlp = spacy.load("output/model-best")

sample = """
20:XYZ9998887
32A:250530EUR750000,
50K:/987654321
ACME CORP
"""

doc = nlp(sample)
for ent in doc.ents:
    print(ent.text, ent.label_)
