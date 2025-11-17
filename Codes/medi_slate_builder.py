"""
MEDI-SLATE Dataset Builder and Analyzer
---------------------------------------

This single script performs ALL dataset preparation steps:

1. Traverse dataset
2. Read slide images and text
3. Compute statistics
4. Compute vocabulary + imaging terminology
5. Generate all figures (safe fallback if data missing)
6. Generate tables
7. Generate gallery
8. Generate pipeline diagram
9. Save logs

Run:
    python medi_slate_builder.py
"""

import os
import re
import json
import random
import logging
from pathlib import Path
from collections import Counter

import matplotlib.pyplot as plt
from wordcloud import WordCloud
from PIL import Image
from graphviz import Digraph

# ============================================================
# CONFIG
# ============================================================

DATASET_ROOT = Path("..")  # correct
OUTPUT_ROOT = Path("../outputs")

FIG_DIR = OUTPUT_ROOT / "figures"
TABLE_DIR = OUTPUT_ROOT / "tables"
GALLERY_DIR = OUTPUT_ROOT / "gallery"
LOG_FILE = OUTPUT_ROOT / "pipeline.log"

# create all directories
for d in [OUTPUT_ROOT, FIG_DIR, TABLE_DIR, GALLERY_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# ============================================================
# LOGGING
# ============================================================

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logging.info("=== Starting MEDI-SLATE Build Script ===")

# ============================================================
# GENERAL MEDICAL IMAGING KEYWORD LIST
# ============================================================

IMAGING_TERMS = [
    # General imaging physics
    "signal", "image", "contrast", "noise", "resolution", "artifact",
    "filter", "sampling", "frequency", "detector", "photon", "attenuation",
    "dose", "scatter", "amplitude", "phase", "modulation",

    # Reconstruction & transforms
    "fourier", "transform", "ifft", "fft", "radon", "inverse", "projection",
    "reconstruction", "iterative", "analytic", "backprojection",
    "regularization", "optimization",

    # CT-related
    "ct", "sinogram", "beam", "collimator", "fan", "cone",

    # MRI-related
    "mri", "kspace", "k-space", "gradient", "coil", "relaxation",
    "t1", "t2", "precession", "spin", "magnetization", "pulse", "sequence",

    # PET/SPECT
    "pet", "spect", "emission", "annihilation", "radioisotope",
    "coincidence", "decay",

    # Ultrasound
    "ultrasound", "transducer", "echo", "beamforming", "acoustic",
    "impedance", "doppler",

    # General modality principles
    "tomography", "imaging", "system", "modality", "instrumentation",
]

IMAGING_TERMS = list(set(IMAGING_TERMS))

# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def clean_text(text):
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    return text

def tokenize(text):
    return text.lower().split()

def count_imaging_terms(text):
    tokens = tokenize(text)
    return sum(token in IMAGING_TERMS for token in tokens)

def numeric_sort_key(path):
    nums = re.findall(r"\d+", str(path))
    return int(nums[-1]) if nums else 0

# ============================================================
# LOAD DATASET
# ============================================================

def load_dataset():
    lectures_folder = DATASET_ROOT / "Lectures"
    if not lectures_folder.exists():
        print("ERROR: Dataset/Lectures folder not found!")
        exit()

    lectures = sorted(lectures_folder.glob("Lecture *"), key=numeric_sort_key)
    dataset = []

    for lecture in lectures:
        images = sorted((lecture / "Images").glob("*.jpg"), key=numeric_sort_key)
        texts  = sorted((lecture / "Texts").glob("*.txt"), key=numeric_sort_key)

        for img, txt in zip(images, texts):
            text = clean_text(Path(txt).read_text(encoding="utf-8"))
            dataset.append({
                "lecture": lecture.name,
                "image": str(img),
                "text": text
            })

    logging.info(f"Loaded dataset with {len(dataset)} slide-text pairs")
    return dataset, lectures

dataset, lectures = load_dataset()

# ============================================================
# STATISTICS
# ============================================================

def compute_statistics():
    per_slide = []
    per_lecture = {}
    vocabulary = Counter()
    imaging_keyword_counts = Counter()

    for item in dataset:
        lecture_name = item["lecture"]
        text = item["text"]

        tokens = tokenize(text)
        sentences = [s for s in re.split(r"[.!?]", text) if s.strip()]
        vocab = set(tokens)

        imaging_count = count_imaging_terms(text)

        per_slide.append({
            "lecture": lecture_name,
            "tokens": len(tokens),
            "sentences": len(sentences),
            "vocab_size": len(vocab),
            "imaging_terms": imaging_count
        })

        vocabulary.update(tokens)
        imaging_keyword_counts.update([t for t in tokens if t in IMAGING_TERMS])

        if lecture_name not in per_lecture:
            per_lecture[lecture_name] = {
                "slides": 0,
                "tokens": 0,
                "vocab": set(),
            }

        per_lecture[lecture_name]["slides"] += 1
        per_lecture[lecture_name]["tokens"] += len(tokens)
        per_lecture[lecture_name]["vocab"].update(vocab)

    for lec in per_lecture:
        per_lecture[lec]["vocab_size"] = len(per_lecture[lec]["vocab"])
        del per_lecture[lec]["vocab"]

    return per_slide, per_lecture, vocabulary, imaging_keyword_counts

per_slide, per_lecture, vocabulary, imaging_keyword_counts = compute_statistics()

# ============================================================
# SAVE TABLES
# ============================================================

def save_tables():
    total_slides = len(per_slide)
    total_tokens = sum(s["tokens"] for s in per_slide)
    total_vocab = len(vocabulary)

    summary_tex = TABLE_DIR / "table_summary.tex"
    summary_tex.write_text(
        "\\begin{tabular}{lc}\n"
        "\\toprule\n"
        "Statistic & Value \\\\\n"
        "\\midrule\n"
        f"Total Slides & {total_slides} \\\\\n"
        f"Total Tokens & {total_tokens} \\\\\n"
        f"Vocabulary Size & {total_vocab} \\\\\n"
        "\\bottomrule\n"
        "\\end{tabular}"
    )

    perlec_tex = TABLE_DIR / "table_per_lecture.tex"
    with perlec_tex.open("w") as f:
        f.write("\\begin{tabular}{lccc}\n")
        f.write("\\toprule\nLecture & Slides & Tokens & Vocabulary Size \\\\\n\\midrule\n")
        for lec, stats in per_lecture.items():
            f.write(f"{lec} & {stats['slides']} & {stats['tokens']} & {stats['vocab_size']} \\\\\n")
        f.write("\\bottomrule\n\\end{tabular}")

save_tables()

# ============================================================
# FIGURES
# ============================================================

def plot_hist(data, title, xlabel, filename):
    plt.figure(figsize=(10,6))
    plt.hist(data, bins=40, color="steelblue")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(FIG_DIR / filename)
    plt.close()

def generate_figures():

    plot_hist(
        [s["tokens"] for s in per_slide],
        "Token Distribution per Slide",
        "Tokens",
        "fig_token_distribution.png"
    )

    plot_hist(
        [s["sentences"] for s in per_slide],
        "Sentence Distribution per Slide",
        "Sentences",
        "fig_sentence_distribution.png"
    )

    # tokens per lecture
    plt.figure(figsize=(12,6))
    lectures_list = list(per_lecture.keys())
    tokens_list = [per_lecture[l]["tokens"] for l in lectures_list]
    plt.bar(lectures_list, tokens_list, color="seagreen")
    plt.xticks(rotation=60, ha="right")
    plt.title("Token Count per Lecture")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "fig_tokens_per_lecture.png")
    plt.close()

    # slides per lecture
    plt.figure(figsize=(12,6))
    slides_list = [per_lecture[l]["slides"] for l in lectures_list]
    plt.bar(lectures_list, slides_list, color="purple")
    plt.xticks(rotation=60, ha="right")
    plt.title("Slides per Lecture")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "fig_slides_per_lecture.png")
    plt.close()

    # imaging terminology distribution (Safe Fallback)
    plt.figure(figsize=(12,8))
    common_terms = imaging_keyword_counts.most_common(20)

    if len(common_terms) == 0:
        plt.bar(["no-imaging-terms-found"], [1], color="gray")
        plt.title("No Recognized Imaging Terms Detected")
        plt.ylabel("Count")
    else:
        labels, values = zip(*common_terms)
        plt.bar(labels, values)
        plt.xticks(rotation=75, ha="right")
        plt.title("Top Imaging Terms in the Dataset")

    plt.tight_layout()
    plt.savefig(FIG_DIR / "fig_topic_distribution.png")
    plt.close()

    # word cloud
    wc = WordCloud(width=1600, height=900, background_color="white").generate(
        " ".join(vocabulary.keys())
    )
    wc.to_file(str(FIG_DIR / "fig_wordcloud.png"))

generate_figures()

# ============================================================
# GALLERY
# ============================================================
def build_gallery(n=25):
    all_images = [item["image"] for item in dataset]
    chosen = random.sample(all_images, min(n, len(all_images)))

    cols = 5
    rows = (len(chosen) + cols - 1) // cols

    fig, axes = plt.subplots(rows, cols, figsize=(20,12))
    axes = axes.flatten()

    for ax, img_path in zip(axes, chosen):
        img = Image.open(img_path)
        ax.imshow(img)
        ax.axis("off")

    for ax in axes[len(chosen):]:
        ax.axis("off")

    plt.tight_layout()
    plt.savefig(GALLERY_DIR / "fig_gallery.png")   # <-- FIXED
    plt.close()


build_gallery()

# ============================================================
# PIPELINE DIAGRAM
# ============================================================

def build_pipeline_diagram():

    dot = Digraph(comment="MEDI-SLATE Pipeline", format="png")

    dot.node("A", "Classroom\nRecording")
    dot.node("B", "Slide Export")
    dot.node("C", "ASR Transcription")
    dot.node("D", "Text Refinement")
    dot.node("E", "Slide–Text Alignment")
    dot.node("F", "Dataset Construction")
    dot.node("G", "Statistics + Figures")
    dot.node("H", "Public Release")

    dot.edge("A", "C")
    dot.edge("A", "B")
    dot.edge("C", "D")
    dot.edge("B", "E")
    dot.edge("D", "E")
    dot.edge("E", "F")
    dot.edge("F", "G")
    dot.edge("G", "H")

    dot.render(str(FIG_DIR / "fig_pipeline_diagram"), cleanup=True)

build_pipeline_diagram()

# ============================================================
# FINISH
# ============================================================

logging.info("=== MEDI-SLATE Build Complete ===")
print("MEDI-SLATE build completed successfully!")
