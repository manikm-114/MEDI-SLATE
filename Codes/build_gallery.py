# DatasetPaper/code/build_gallery.py

import matplotlib.pyplot as plt
from PIL import Image
from load_data import load_dataset
from utils import save_fig
import random

def build_gallery():
    data = load_dataset()

    # Flatten all slides
    all_slides = []
    for slides in data.values():
        all_slides.extend(slides)

    # Sample 12 slides
    random.shuffle(all_slides)
    sample = all_slides[:12]

    fig, axes = plt.subplots(4, 3, figsize=(12, 16))

    for ax, slide in zip(axes.flatten(), sample):
        img = Image.open(slide["image_path"])
        ax.imshow(img)
        ax.set_title(slide["slide_id"])
        ax.axis("off")

    save_fig("../figures/fig_gallery.png")
    print("✔ Gallery generated.")

if __name__ == "__main__":
    build_gallery()
