import os
from bs4 import BeautifulSoup
from src.utils import clean_text


def extract_text_from_html(file_path, utf=False):
    with open(file_path, "r", encoding="Windows-1256") as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, "html.parser")
    margin = []
    main = []

    for tr in soup.find_all("tr"):
        tr = BeautifulSoup(
            "<tr" + str(tr).split("<tr")[1]
        )  # si on prend le tr comme il est on prend tous les tr qui le suivent

        # Traitement des cas spéciaux
        _tds = []
        for i, td in enumerate(tr.find_all("td")):
            if (
                td == BeautifulSoup("<td>\n</td>").find("td")
                and not tr.find_all("td")[i - 1].text.strip()
            ):  # Pour les textes page >=2
                _tds.append(BeautifulSoup('<td colspan="5"> </td>').find("td"))
            else:
                _tds.append(td)
        tds = [td for td in _tds if td.get("colspan") or td.get("width")]

        text_tds = [td for td in tds if td.text.strip()]

        if text_tds:
            for i, text_td in enumerate(text_tds):
                text_content = text_td.text.strip()

                if text_content:
                    non_text_tds = len(
                        [td for td in tds[: tds.index(text_td)] if not td.text.strip()]
                    )  # Nombre de td sans texte avant le td actuel

                    if non_text_tds == 0 or (
                        non_text_tds == 1 and tds[0].get("colspan") == "2"
                    ):
                        margin.append(text_content)
                    elif (
                        non_text_tds == 1
                        and tds[0].get("colspan")
                        and int(tds[0]["colspan"]) > 2
                    ):
                        main.append(text_content)
                    elif i == 0 and non_text_tds > 1:
                        main.append(text_content)
                    elif (
                        sum(
                            [
                                int(td["colspan"])
                                for td in tds[: tds.index(text_td)]
                                if td.get("colspan")
                            ]
                        )
                        > 8
                    ):
                        main.append(text_content)
                    elif (
                        sum(
                            [
                                int(td["colspan"])
                                for td in tds[: tds.index(text_td)]
                                if td.get("colspan") and not td.text.strip()
                            ]
                        )
                        < 5
                    ):
                        margin.append(text_content)
                    else:
                        main.append(text_content)

    margin_text = "\n".join(margin)
    main_text = "\n".join(main)
    return clean_text(margin_text), clean_text(main_text, main=True)


if __name__ == "__main__":
    for file_name in os.listdir("data"):
        if file_name.endswith(".html"):
            file_path = os.path.join("data", file_name)
            margin, main = extract_text_from_html(file_path)
            out_path = os.path.join("output_text", file_name.split(".")[0] + ".txt")
            with open(out_path, "w", encoding="utf-8") as file:
                file.write(f"# Marge:\n{margin}\n\n# Contenu:\n{main}")
