# DatasetPaper/code/generate_tables.py

import pandas as pd
from utils import ensure_dir

def generate_tables():
    ensure_dir("../data/tables")

    df_lec = pd.read_csv("../data/per_lecture_stats.csv")

    # --------------------------------------------------
    # Table 1: Dataset summary
    # --------------------------------------------------
    summary = pd.DataFrame({
        "Total Lectures": [df_lec.shape[0]],
        "Total Slides": [df_lec["num_slides"].sum()],
        "Total Tokens": [df_lec["num_tokens"].sum()],
        "Avg Slides per Lecture": [df_lec["num_slides"].mean()],
        "Avg Tokens per Lecture": [df_lec["num_tokens"].mean()]
    })

    summary.to_latex("../data/tables/table_summary.tex", index=False)

    # --------------------------------------------------
    # Table 2: Per-lecture stats
    # --------------------------------------------------
    df_lec.to_latex("../data/tables/table_per_lecture.tex", index=False)

    print("✔ Tables generated.")

if __name__ == "__main__":
    generate_tables()
