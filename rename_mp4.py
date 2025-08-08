# python3 rename_mp4.py

import os
import re

for root, dirs, files in os.walk("."):
    folder_name = os.path.basename(root).strip()

    if folder_name == "":
        continue

    for file in files:
        if file.lower().endswith(".mp4"):
            match = re.match(r"(\d+)\.mp4$", file, re.IGNORECASE)
            if match:
                number = match.group(1)
                new_name = f"{folder_name} - {number}.mp4"
                old_path = os.path.join(root, file)
                new_path = os.path.join(root, new_name)

                if old_path != new_path:
                    os.rename(old_path, new_path)
                    print(f"Renamed: {old_path} -> {new_path}")
