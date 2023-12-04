import os
import re
import pandas as pd
import argparse

import nltk
import pymorphy2
from nltk.corpus import stopwords

import pickle
from utils import get_stopwords_from_file

nltk.download("stopwords")
stop_words = stopwords.words("russian")
extra_stop_words = get_stopwords_from_file("stopwords.txt")
stop_words_extended = set(stop_words + extra_stop_words)

morph = pymorphy2.MorphAnalyzer()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path", type=str, help="Path to the CSV file.")

    return parser.parse_args()


def process_string(input_string, morph=morph, stop_words=stop_words_extended):
    words = re.findall(r"\b[а-яА-Я_]+\b", input_string)
    result_string = " ".join(
        [
            word if "_" in word else morph.parse(word)[0].normal_form
            for word in words
            if word not in stop_words
        ]
    )

    return result_string


def main():
    args = parse_args()
    model = pickle.load(open("best_classifier.sav", "rb"))
    df = pd.read_csv(args.csv_path)
    # Предсказания делаются отдельно для каждого диалога, в том числе для одного ucid
    df["processed"] = df["text_employer"].apply(process_string)

    df["pred"] = model.predict(df["processed"])

    df = df.drop(["processed"], axis=1)
    output_csv_path = os.path.splitext(args.csv_path)[0] + "_out.csv"
    df.to_csv(output_csv_path)
    print("Результат успешно сохранен в", output_csv_path)


if __name__ == "__main__":
    main()
