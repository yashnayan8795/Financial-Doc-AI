import spacy
from spacy.tokens import DocBin
import json
import os

# Create output directory if it doesn't exist
output_dir = "data/ner_training"
os.makedirs(output_dir, exist_ok=True)

# Load annotated data
with open("data/ner_training/train_data_auto.json", "r") as f:
    training_data = json.load(f)

nlp = spacy.blank("en")  # Create blank pipeline
ner = nlp.add_pipe("ner")

# Add entity labels
for _, annotations in training_data:
    for start, end, label in annotations["entities"]:
        ner.add_label(label)

# Convert to spaCy DocBin
doc_bin = DocBin()
for text, annot in training_data:
    doc = nlp.make_doc(text)
    ents = []
    for start, end, label in annot["entities"]:
        span = doc.char_span(start, end, label=label, alignment_mode="contract")
        if span:
            ents.append(span)
    doc.ents = ents
    doc_bin.add(doc)

# Save the DocBin object
spacy_file = os.path.join(output_dir, "train.spacy")
doc_bin.to_disk(spacy_file)
print(f"✅ Saved spaCy training data at {spacy_file}")
