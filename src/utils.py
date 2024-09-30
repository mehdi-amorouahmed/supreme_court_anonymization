import re


def clean_text(text: str, main: bool = False) -> str:
    lines = text.split("\n")
    if main:
        lines = lines[3:]

    pattern = re.compile(r"صفحة \d+ من \d+")
    filtered_lines = [line for line in lines if not pattern.search(line)]

    if not main:
        filtered_lines = list(dict.fromkeys(filtered_lines))

    return "\n".join(filtered_lines)


def correct_wilayas(wilaya: str) -> str:
    wilayas = {
        "الدفلى": "عين الدفلى",
        "تموشنت": "عين تموشنت",
        "بوعريريج": "برج بوعريريج",
        "بلعباس": "سيدي بلعباس",
        "سوف": "وادي سوف",
        "وزو": "تِيزي وزو",
    }
    wilaya = wilaya.replace(".", "")
    if wilaya in wilayas:
        return wilayas[wilaya]
    return wilaya


def clean_ner(ner: list) -> list:
    return [
        person
        for person in ner
        if not any(person in other and person != other for other in ner)
    ]
