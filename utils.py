import pandas as pd
import random
from collections import defaultdict, Counter
import matplotlib.pyplot as plt
import seaborn as sns


def get_relative_freq_per_category(df: pd.DataFrame, extractor):
    word_count_per_category = defaultdict(lambda: defaultdict(int))
    total_counts_per_category = defaultdict(int)

    for index, row in df.iterrows():
        text = row["text_employer"]
        target = row["category"]

        word_list = extractor(text)
        category_counts = Counter(word_list)

        for word, count in category_counts.items():
            word_count_per_category[word][target] += count
            total_counts_per_category[target] += count

    relative_freq_per_category = defaultdict(lambda: defaultdict(float))

    for word, category_counts in word_count_per_category.items():
        for target, count in category_counts.items():
            relative_freq = count / total_counts_per_category[target]
            relative_freq_per_category[word][target] = relative_freq

    return relative_freq_per_category


def plot_relative_freq_per_category(frequency_dict: dict[dict]) -> None:
    categories = [
        "Бизнес-карта",
        "Зарплатные проекты",
        "Эквайринг",
        "Открытие банковского счета",
    ]
    palette_name = "Set3"
    category_colors = {
        word: sns.color_palette(palette_name)[i] for i, word in enumerate(categories)
    }

    num_rows = 7
    num_cols = 10
    fig, axs = plt.subplots(num_rows, num_cols, figsize=(15, 20))
    fig.tight_layout(pad=0)

    for i, (word, frequencies) in enumerate(frequency_dict.items()):
        row = i // num_cols
        col = i % num_cols

        topics = list(frequencies.keys())
        values = list(frequencies.values())

        colors = [category_colors[category] for category in frequencies.keys()]
        wedges, texts = axs[row, col].pie(
            values,
            startangle=90,
            pctdistance=2,
            wedgeprops=dict(width=0.9),
            colors=colors,
        )
        pos = -0.2 if col % 2 == 1 else 0.9
        axs[row, col].set_title(f"{word}", fontsize=9, y=pos)

    for i in range(len(frequency_dict), num_rows * num_cols):
        row = i // num_cols
        col = i % num_cols
        fig.delaxes(axs[row, col])

    fig.subplots_adjust(hspace=0.1, wspace=0.1)

    legend_labels = [
        plt.Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            markerfacecolor=category_colors[category],
            markersize=10,
            label=category,
        )
        for category in category_colors.keys()
    ]
    fig.legend(
        handles=legend_labels,
        title="Words",
        loc="upper center",
        bbox_to_anchor=(0.5, 1.05),
        ncol=len(category_colors),
    )

    plt.show()


def get_stopwords_from_file(file_path):
    word_set = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            word = line.strip()
            if word:
                word_set.append(word)

    return word_set


necessary_samples = {
    "Бизнес-карта": 0,
    "Зарплатные проекты": 6000,
    "Открытие банковского счета": 13000,
    "Эквайринг": 15000,
}


def generate_augmented_text(words, n_samples, label, min_words=50, max_words=100):
    augmented_data = []

    for _ in range(n_samples):
        num_words = random.randint(min_words, max_words)
        selected_words = random.sample(words, min(num_words, len(words)))
        text = " ".join(selected_words)
        augmented_data.append({"text_employer": text, "category": label})

    return augmented_data


def augment_data(
    df, text_col, necessary_samples=necessary_samples, min_words=50, max_words=100
):
    augmented_data = []
    grouped_data = df.groupby("category")

    for class_label, group in grouped_data:
        words = " ".join(group[text_col]).split()
        augmented_data.extend(
            generate_augmented_text(
                words, necessary_samples[class_label], class_label, min_words, max_words
            )
        )

    augmented_df = pd.concat([df, pd.DataFrame(augmented_data)], ignore_index=True)

    return augmented_df
