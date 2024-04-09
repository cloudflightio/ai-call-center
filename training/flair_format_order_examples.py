import json
import os

import nltk
import pandas as pd

nltk.download("punkt")


def tokenize_text_with_labels(text, entities: list[tuple]) -> list:
    tokens = nltk.tokenize.word_tokenize(text)
    tags = ["O"] * len(tokens)  # O = other
    processed_indices = set()

    for entity, category in entities:
        entity_tokens = nltk.tokenize.word_tokenize(entity, language="german")
        # Label all the tokens in the text:
        for i in range(len(tokens) - len(entity_tokens) + 1):
            if tokens[i : i + len(entity_tokens)] == entity_tokens:
                if any(index in processed_indices for index in range(i, i + len(entity_tokens))):
                    continue

                tags[i] = f"B-{category}"
                tags[i + 1 : i + len(entity_tokens)] = [f"I-{category}"] * (len(entity_tokens) - 1)
                processed_indices.update(range(i, i + len(entity_tokens)))
    return list(zip(tokens, tags))


def product_entity_dicts_to_tuples(products: list[dict]):
    entities = []
    for product in products:
        for entity_type, entity_text in product.items():
            if entity_type == "sku":
                continue
            elif entity_type == "quantity_word":
                entity_type = "quantity"
            entities += [(entity_text, entity_type)]
    return entities


def format_orders_with_entities_list(folder: str):
    """Look into given folder for sentence_x.json files and process them."""
    data_tuples = []

    i = 0
    while True:
        # As long as there is a new sentence file, extract the information in it
        file_path = os.path.join(folder, f"sentence_{i}.json")
        try:
            with open(file_path, "r") as f:
                order = json.load(f)
        except FileNotFoundError:
            break

        text = order["text"]
        products = order["products"]

        entities = product_entity_dicts_to_tuples(products)
        data_tuples.append((text, entities))

        i += 1

    return data_tuples


def format_dataset_for_flair(folder_name: str):
    data_tuples = format_orders_with_entities_list(folder=f"./data/{folder_name}")
    df = pd.DataFrame(data_tuples, columns=["text", "entities"])

    # Add tokenized text to each row:
    df["tokenized_text"] = df.apply(
        lambda row: tokenize_text_with_labels(row["text"], row["entities"]), axis=1
    )

    # Store each token separately with according tag:
    token_list = []
    for idx, sentence_tokens in df.iterrows():
        for token, label in sentence_tokens["tokenized_text"]:
            token_list.append({"sentence_idx": idx, "token": token, "tag": label})

    token_data = pd.DataFrame(token_list)

    # Some jibberish:
    data = (
        token_data[token_data["sentence_idx"] != "prev-lemma"]
        .dropna(subset=["sentence_idx"])
        .reset_index(drop=True)
    )
    data["sentence_idx"] = data["sentence_idx"].apply(int)

    mask = data["sentence_idx"].ne(data["sentence_idx"].shift(-1))

    data1 = pd.DataFrame("", index=mask.index[mask] + 0.5, columns=data.columns)
    data2 = pd.concat([data, data1]).sort_index().reset_index(drop=True).iloc[:-1]

    os.makedirs("./data/flair", exist_ok=True)

    data2[["token", "tag"]].to_csv("./data/flair/train_data_flair.txt", sep=" ", index=False, header=False)

    return data2


if __name__ == "__main__":
    FOLDER = "order_examples_test"  # HINT: Folder inside the data folder containing the order examples for training
    format_dataset_for_flair(folder_name=FOLDER)
