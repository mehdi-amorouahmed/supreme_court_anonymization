from src.get_chunks import get_chunks
from src.config import classifier


def _extract_ner(text):
    entities = classifier(text)
    if not entities:
        return []

    def merge_entities(entity, next_entity, text):
        """Helper function to merge two entities."""
        entity["word"] += (
            " "
            if entity["end"] == next_entity["start"] - 1
            and text[next_entity["start"] - 1] == " "
            else ""
        ) + next_entity["word"]
        entity["end"] = next_entity["end"]
        entity["score"] = (entity["score"] + next_entity["score"]) / 2
        return entity

    merged_entities = []
    current_entity = entities[0]

    for i in range(1, len(entities)):
        next_entity = entities[i]
        if current_entity["end"] == next_entity["start"] or (
            current_entity["end"] == next_entity["start"] - 1
            and text[next_entity["start"] - 1] == " "
        ):
            current_entity = merge_entities(current_entity, next_entity, text)
        else:
            current_entity["word"] = current_entity["word"].replace("▁", "")
            merged_entities.append(current_entity)
            current_entity = next_entity

    # Append the last entity after processing
    current_entity["word"] = current_entity["word"].replace("▁", "")
    merged_entities.append(current_entity)

    # Use list comprehension to format the output
    return [
        {"token": entity["word"], "label": entity["entity"].split("-")[1]}
        for entity in merged_entities
    ]


def hf_ner_extractor(text: str) -> dict[str, set]:
    res = {"persons": set()}
    samples = get_chunks(text)
    for sample in samples:
        ents = _extract_ner(text=sample)
        for ent in ents:
            if ent["label"] == "PER":
                res["persons"].add(ent["token"])
    return res
