import re


def get_chunks(text: str) -> list[str]:
    """
    This function takes the text extracted from the doc and returns a list
    of chunks likely to contain names of people, including the headers
    identified using regex, as well as the grouped paragraphs of the content
    """
    texts_to_check = []
    good = False
    lines = text.split("\n")

    # Processing lines to find specific patterns and extract texts
    for i, line in enumerate(lines):
        clean_line = line.strip()
        if re.search(r"\d+:\)", clean_line):
            texts_to_check.append(re.sub(r"\d+:\)", "", clean_line))
        elif "المحامي المعتمد" in clean_line:
            texts_to_check.append(clean_line)
        if "**" in clean_line:
            break

    # Collect paragraph lines after the break or from where lines were left off
    para_lines = []
    current_paragraph = []
    for line in lines[i:]:
        clean_line = line.strip()
        clean_line = re.sub(" +", " ", clean_line)
        if (
            clean_line
            == "بــذا صـــدر القـــرار بالتـــاريـــخ المـذكـــور أعـــلاه من قبــل المـحـكـمـة العليــــــا"
        ):
            good = True
            break
        if "**" not in clean_line:
            current_paragraph.append(clean_line)
        else:
            para_lines.append(current_paragraph)
            current_paragraph = []

    # Combine lines until they form complete paragraphs ending with '.'
    for paragrapgh in para_lines:
        old_line = ""
        for line in paragrapgh:
            combined_line = (old_line + " " + line).strip()
            if combined_line.endswith("."):
                texts_to_check.append(combined_line)
                old_line = ""
            else:
                old_line = combined_line

    if not good:
        print("not good")

    # Filter out unwanted texts
    return texts_to_check
