# DatasetPaper/code/generate_figures.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils import save_fig, ensure_dir

def generate_all_figures():
    ensure_dir("../figures")

    df_lec = pd.read_csv("../data/per_lecture_stats.csv")
    df_slide = pd.read_csv("../data/per_slide_stats.csv")

    # --------------------------------------------------
    # Figure 1: Slides per lecture
    # --------------------------------------------------
    plt.figure(figsize=(12,5))
    sns.barplot(x="lecture_num", y="num_slides", data=df_lec, palette="viridis")
    plt.xticks(df_lec["lecture_num"], df_lec["lecture"], rotation=90)
    plt.title("Slides per Lecture")
    save_fig("../figures/fig_slides_per_lecture.png")

    # --------------------------------------------------
    # Figure 2: Token distribution
    # --------------------------------------------------
    plt.figure(figsize=(10,5))
    sns.histplot(df_slide["num_tokens"], bins=40, kde=True, color="blue")
    plt.title("Token Distribution per Slide")
    save_fig("../figures/fig_token_distribution.png")

    # --------------------------------------------------
    # Figure 3: Technical term distribution
    # --------------------------------------------------
    tech_cols = [
        c for c in df_slide.columns 
        if c in ["ct","sinogram","radon","attenuation","convolution","fourier",
                 "reconstruction","artifact","noise","dose","projection",
                 "transform","detector","collimator","beam"]
    ]

    term_counts = df_slide[tech_cols].sum()

    plt.figure(figsize=(14,6))
    sns.barplot(x=term_counts.index, y=term_counts.values)
    plt.title("Technical Term Frequency")
    plt.xticks(rotation=90)
    save_fig("../figures/fig_topic_distribution.png")

    # --------------------------------------------------
    # Figure 4: Sentence count distribution
    # --------------------------------------------------
    plt.figure(figsize=(10,5))
    sns.histplot(df_slide["num_sentences"], bins=30, kde=True, color="green")
    plt.title("Sentence Count Distribution per Slide")
    save_fig("../figures/fig_sentence_distribution.png")

    # --------------------------------------------------
    # Figure 5: Tokens per lecture
    # --------------------------------------------------
    plt.figure(figsize=(10,5))
    sns.barplot(x="lecture_num", y="num_tokens", data=df_lec)
    plt.xticks(df_lec["lecture_num"], df_lec["lecture"], rotation=90)
    plt.title("Tokens per Lecture")
    save_fig("../figures/fig_tokens_per_lecture.png")

    print("✔ All figures generated successfully.")

if __name__ == "__main__":
    generate_all_figures()
