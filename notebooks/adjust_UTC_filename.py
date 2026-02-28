import os
import re
import shutil
from datetime import datetime, timedelta

# === SETTINGS ===
source_root = "/Volumes/Extreme SSD/FPVA/audios/"                 # Root directory with .WAV files
destination_root = "/Volumes/Extreme SSD/FPVA/shifted/"    # Folder where renamed copies will be stored
offset = timedelta(hours=+5)      # Time shift (e.g., -5 hours)
dry_run = True                   # Set to False to actually copy files
# =================

pattern = re.compile(r"^(.*)_(\d{8})_(\d{6})\.WAV$", re.IGNORECASE)

for dirpath, dirnames, filenames in os.walk(source_root):
    # Skip hidden directories (those starting with '.')
    dirnames[:] = [d for d in dirnames if not d.startswith(".")]

    for filename in filenames:
        # Skip hidden files (those starting with '.')
        if filename.startswith("."):
            continue

        match = pattern.match(filename)
        if not match:
            continue

        prefix, date_str, time_str = match.groups()

        try:
            dt = datetime.strptime(date_str + time_str, "%Y%m%d%H%M%S")
        except ValueError:
            print(f"⚠️ Skipping {os.path.join(dirpath, filename)}: invalid datetime format.")
            continue

        dt_new = dt + offset
        new_name = f"{prefix}_{dt_new.strftime('%Y%m%d_%H%M%S')}.WAV"

        # Determine relative path to maintain subdirectory structure
        rel_dir = os.path.relpath(dirpath, source_root)
        dest_dir = os.path.join(destination_root, rel_dir)
        os.makedirs(dest_dir, exist_ok=True)

        src_path = os.path.join(dirpath, filename)
        dest_path = os.path.join(dest_dir, new_name)

        if dry_run:
            print(f"[DRY RUN] {src_path} -> {dest_path}")
        else:
            shutil.copy2(src_path, dest_path)  # copy2 preserves timestamps & metadata
            print(f"Copied: {src_path} -> {dest_path}")

print("\n✅ Done! (Dry run = {})".format(dry_run))
