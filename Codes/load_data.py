# DatasetPaper/code/load_data.py

from pathlib import Path
from utils import ensure_dir, load_text, clean_text

DATASET_ROOT = Path("../Lectures")

# ------------------------------------------------------
# Numeric sorting helpers
# ------------------------------------------------------
def parse_lecture_num(name):
    # "Lecture 10" → 10
    return int(name.replace("Lecture", "").strip())

def parse_slide_num(name):
    # "Slide 7" → 7
    return int(name.replace("Slide", "").strip())

# ------------------------------------------------------
# Load dataset with numeric ordering
# ------------------------------------------------------
def load_dataset():
    lectures = {}

    lecture_dirs = sorted(
        [d for d in DATASET_ROOT.iterdir() if d.is_dir()],
        key=lambda x: parse_lecture_num(x.name)
    )

    for lecture_dir in lecture_dirs:
        lecture_id = lecture_dir.name
        images_dir = lecture_dir / "Images"
        texts_dir = lecture_dir / "Texts"

        slides = []

        text_files = sorted(
            texts_dir.glob("*.txt"),
            key=lambda p: parse_slide_num(p.stem)
        )

        for txt_file in text_files:
            slide_id = txt_file.stem  # e.g., "Slide 3"
            img_file = images_dir / f"{slide_id}.jpg"

            if not img_file.exists():
                continue

            text = clean_text(load_text(txt_file))

            slides.append({
                "slide_id": slide_id,
                "slide_num": parse_slide_num(slide_id),
                "image_path": str(img_file),
                "text_path": str(txt_file),
                "text": text
            })

        lectures[lecture_id] = slides

    return lectures


if __name__ == "__main__":
    data = load_dataset()
    print("Loaded lectures (sorted):")
    print(list(data.keys()))
