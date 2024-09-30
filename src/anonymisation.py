import re
from src.utils import correct_wilayas


def anonymize_text(text: str, ner: dict) -> str:
    text = re.sub(r"(\(|\))", r" \1 ", text).replace("( ة )", "(ة)")
    anonymized_text = re.sub(r" +", " ", text)

    # Anonymize persons
    for person in ner["persons"]:
        anonyma = '"' + ".".join([name[0] for name in person.split(" ") if name]) + '"'
        pattern = r"\s*".join(re.sub(r"\s+", " ", person))
        person_pattern = re.sub(r"[إ|ا|أ]", "[إ|ا|أ]", pattern)
        person_pattern = rf"(\s|>)({person_pattern})(\s|<|.)"
        if person_pattern:
            anonymized_text = re.sub(person_pattern, rf"\1{anonyma}\3", anonymized_text)

    # Anonymize addresses
    for address in ner["addresses"]:
        anonyma = correct_wilayas(address.split(" ")[-1])
        anonymized_text = anonymized_text.replace(address, anonyma)

    # En cas où le nom est coupé entre deux pages ou deux td
    for person in ner["persons"]:
        anonyma = '"' + ".".join([name[0] for name in person.split(" ") if name]) + '"'
        names = [name for name in person.split(" ") if name]
        if len(names) > 1:
            name = re.sub(r"[إ|ا|أ]", "[إ|ا|أ]", names[0])
            pattern = rf"(\s|>)({name})(\s|<|.)"
            if re.search(pattern, anonymized_text):
                i = 0
                for name in names[1:]:
                    end = re.search(pattern, anonymized_text).end() - 1
                    name = re.sub(r"[إ|ا|أ]", "[إ|ا|أ]", name)
                    pat = rf"(\s|>)({name})(\s|<|.)"
                    if re.search(pat, anonymized_text[end:]):
                        i += 1
                        anonymized_text = anonymized_text[:end] + re.sub(
                            pat, r"\1\3", anonymized_text[end:]
                        )
                if i > 0:
                    anonymized_text = re.sub(
                        pattern, rf"\1{anonyma}\3", anonymized_text
                    )

    return anonymized_text
