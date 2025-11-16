# DatasetPaper/code/compute_statistics.py

import pandas as pd
from collections import Counter
from utils import (
    ensure_dir, tokenize, sentence_split, count_technical_terms,
    generate_wordcloud
)
from load_data import load_dataset, parse_lecture_num, parse_slide_num

def compute_statistics():
    data = load_dataset()

    per_slide = []
    per_lecture = []

    global_vocab = Counter()
    combined_text = ""

    # ----------------------------------------------
    # Compute per-slide + per-lecture statistics
    # ----------------------------------------------
    for lecture_id, slides in data.items():

        lecture_num = parse_lecture_num(lecture_id)
        lecture_token_count = 0
        lecture_vocab = Counter()

        for slide in slides:
            text = slide["text"]
            tokens = tokenize(text)
            sentences = sentence_split(text)
            tech_terms = count_technical_terms(text)

            global_vocab.update(tokens)
            lecture_vocab.update(tokens)
            combined_text += " " + text

            per_slide.append({
                "lecture": lecture_id,
                "lecture_num": lecture_num,
                "slide_id": slide["slide_id"],
                "slide_num": slide["slide_num"],
                "num_tokens": len(tokens),
                "num_sentences": len(sentences),
                **tech_terms
            })

            lecture_token_count += len(tokens)

        per_lecture.append({
            "lecture": lecture_id,
            "lecture_num": lecture_num,
            "num_slides": len(slides),
            "num_tokens": lecture_token_count,
            "vocab_size": len(lecture_vocab),
        })

    # ----------------------------------------------
    # Convert to sorted DataFrames
    # ----------------------------------------------
    df_slide = pd.DataFrame(per_slide).sort_values(
        ["lecture_num", "slide_num"]
    )
    df_lecture = pd.DataFrame(per_lecture).sort_values(
        ["lecture_num"]
    )

    # ----------------------------------------------
    # Save outputs
    # ----------------------------------------------
    ensure_dir("../data")
    df_slide.to_csv("../data/per_slide_stats.csv", index=False)
    df_lecture.to_csv("../data/per_lecture_stats.csv", index=False)

    with open("../data/vocabulary_stats.json", "w", encoding="utf-8") as f:
        import json
        json.dump(dict(global_vocab), f, indent=2)

    # ----------------------------------------------
    # Generate word cloud
    # ----------------------------------------------
    generate_wordcloud(combined_text, "../figures/fig_wordcloud.png")

    print("✔ Statistics computed successfully.")


if __name__ == "__main__":
    compute_statistics()
