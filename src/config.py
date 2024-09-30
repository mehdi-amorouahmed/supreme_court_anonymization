import os
import json

from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForTokenClassification

model = "xlm-roberta-large-finetuned-conll03-english"
tokenizer = AutoTokenizer.from_pretrained(model)
model = AutoModelForTokenClassification.from_pretrained(model)
classifier = pipeline("ner", model=model, tokenizer=tokenizer)

with open(
    os.path.join(os.getcwd(), "src", "entreprise.json"), "r", encoding="utf-8"
) as file:
    entreprises_arabe = json.load(file)
