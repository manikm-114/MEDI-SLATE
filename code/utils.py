# DatasetPaper/code/utils.py

import os
import json
import re
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from wordcloud import WordCloud
import textstat

# ------------------------------------------------------
# Create directories automatically
# ------------------------------------------------------
def ensure_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)

# ------------------------------------------------------
# Text utilities
# ------------------------------------------------------
def load_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def tokenize(text):
    return text.split()

def sentence_split(text):
    return re.split(r'[.!?]+', text)

# ------------------------------------------------------
# CT terminology (keyword-based)
# ------------------------------------------------------
CT_TERMS = [
    "ct", "sinogram", "radon", "attenuation", "convolution",
    "fourier", "reconstruction", "artifact", "noise", "dose",
    "projection", "transform", "detector", "collimator", "beam",
]

def count_technical_terms(text):
    text_lower = text.lower()
    return {term: text_lower.count(term) for term in CT_TERMS}

# ------------------------------------------------------
# Save figure helper
# ------------------------------------------------------
def save_fig(path):
    ensure_dir(Path(path).parent)
    plt.tight_layout()
    plt.savefig(path, dpi=300)
    plt.close()

# ------------------------------------------------------
# Wordcloud generator
# ------------------------------------------------------
def generate_wordcloud(text, save_path):
    wc = WordCloud(width=1600, height=900, background_color="white")
    img = wc.generate(text)
    ensure_dir(Path(save_path).parent)
    img.to_file(save_path)
