import os
import shutil

# Define your source and destination directories
src_base_dir = r"G:\My Drive\1. Studies\RPI\Thesis\1. Prof Ge Wang\1. Avatar Project\Future Directions\Comparing Models\Lectures"
dst_base_dir = r"G:\My Drive\1. Studies\RPI\Thesis\1. Prof Ge Wang\1. Avatar Project\Future Directions\DatasetPaper\Lectures"

# Define folders to copy
folders_to_copy = ['Final', 'Images', 'Texts']

for i in range(1, 24):  # Loop through Lecture 1 to Lecture 23
    lecture_src = os.path.join(src_base_dir, f"Lecture {i}")
    lecture_dst = os.path.join(dst_base_dir, f"Lecture {i}")

    # Create destination lecture folder if it doesn't exist
    os.makedirs(lecture_dst, exist_ok=True)

    for folder in folders_to_copy:
        src_folder = os.path.join(lecture_src, folder)
        dst_folder = os.path.join(lecture_dst, folder)

        if os.path.exists(src_folder):
            # Remove the destination folder if it already exists (optional)
            if os.path.exists(dst_folder):
                shutil.rmtree(dst_folder)
            
            # Copy the folder
            shutil.copytree(src_folder, dst_folder)
            print(f"Copied {src_folder} to {dst_folder}")
        else:
            print(f"Folder '{folder}' not found in {lecture_src}. Skipping...")

print("Done copying lecture folders.")
