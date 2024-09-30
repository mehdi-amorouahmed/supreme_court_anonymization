import re
from src.config import entreprises_arabe


def regex_ner_extractor(text: str) -> dict[str, set]:
    ner = {"persons": set(), "addresses": set()}
    text = re.sub(r"(\(|\))", r" \1 ", text)
    text = re.sub(r" +", " ", text)
    lines = text.split("\n")

    for i, line in enumerate(lines):
        if "**" in line:
            break
        # Extract persons
        if re.search(r"\d+:\s\)", line):  # Personnes pas entreprises
            line = re.sub(r"\d+:\s\)\s", "", line)
            if "شركاء" in line:
                line = line[: re.search("شركاء", line).start()]
            line = re.sub(r"(?:\bأرمل(?:ته?)?\b|\bو?أبناء?(?:ؤ?ه?)?\b)", "", line)

            if re.search(r"ورثة\s+(\S+)\s+(\S+)", line):
                ner["persons"].add(
                    " ".join(re.search(r"ورثة\s+(\S+)\s+(\S+)", line).groups())
                )
            if "أرملة" in line:
                names = [name.strip() for name in line.split("أرملة")]
                ner["persons"].update(names)
            elif all(
                keyword not in line
                for keyword in (entreprises_arabe + ["ممثلة", "النيابة العامة"])
            ):
                if ":" in line:
                    line = " ".join(line.split(":")[1:])
                if re.search(r"-|،", line):
                    names = [
                        name.strip() for name in re.split(r"-|،", line) if name.strip()
                    ]
                    ner["persons"].update(names)
                else:
                    name = line.strip()
                    ner["persons"].add(name)
            elif re.search("السيد", line):
                name = line[re.search(r"السيدة?", line).end() + 1 :].strip()
                ner["persons"].add(name)

        elif re.search("المحامي المعتمد", line):  # Avocats
            line = line.replace(" المحامي المعتمد لدى المحكمة العليا", "")
            if "+" in line:
                names = [name.strip() for name in line.split("+") if name.strip()]
                ner["persons"].update(names)
            else:
                ner["persons"].add(line.strip())
        # Extract addresses
        elif re.search("الساكن :", line) or re.search("الكائن مقره بـ :", line):
            if i + 1 < len(lines):
                ner["addresses"].add(
                    re.sub(r"غير ممثلي?ن?ة?", "", lines[i + 1].replace("ـ", ""))
                    .strip()
                    .replace("..", ".")
                )
    for j, line in enumerate(lines[i:]):
        j += i
        if re.search("السادة :", line):  # Membres de la chambre
            member_lines = lines[j + 1 :][:-3]
            to_remove = [
                member
                for member in member_lines
                if "بحــــــضـــور" in member or "بمســـاعـــد ة" in member
            ]
            for member in to_remove:
                member_lines.remove(member)
            ner["persons"].update(
                [
                    item.strip()
                    for index, item in enumerate(member_lines)
                    if index % 2 == 0
                ]
            )

    return ner
