import os
import re

from src.utils import clean_ner
from src.extract_ner_hf_model import hf_ner_extractor
from src.extract_ner_regex import regex_ner_extractor
from src.anonymisation import anonymize_text
from html_to_text import extract_text_from_html


def extract_ner(text: str):
    res = {}

    regex_ner = regex_ner_extractor(text)
    model_ner = hf_ner_extractor(text)

    res["persons"] = set(
        clean_ner(
            [
                re.sub(r"[^\u0600-\u06FF\s]+", "", person).strip()
                for person in (regex_ner["persons"] | model_ner["persons"])
            ]
        )
    )
    res["addresses"] = regex_ner["addresses"]
    return res


def hybrid_anonymiser(file_path, out_path):
    with open(file_path, "r", encoding="Windows-1256") as file:
        html = file.read()
    text = extract_text_from_html(file_path)[1]
    ner = extract_ner(text)
    anonymized_html = anonymize_text(html, ner)
    with open(out_path, "w", encoding="utf-8") as file:
        file.write(anonymized_html)


if __name__ == "__main__":
    for file_name in os.listdir("data"):
        if file_name.endswith(".html") and "ano" not in file_name:
            file_path = os.path.join("data", file_name)
            out_path = os.path.join(
                "output_anonyma_hybride", file_name.split(".")[0] + "_ano.html"
            )
            hybrid_anonymiser(file_path, out_path)
