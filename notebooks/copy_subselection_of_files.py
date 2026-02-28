import os
import re
import shutil

# === SETTINGS ===
source_root = "/Volumes/Extreme SSD/FPVA/audios/G24/"              # Folder to start from
destination_root = "/Volumes/Extreme SSD/FPVA/audios/G24_filtered/"  # Where to copy selected files
dry_run = False                 # Set to False to actually copy
# =================

# Matches PREFIX_YYYYMMDD_HHMMSS.WAV (case-insensitive)
pattern = re.compile(r"^(.*)_(\d{8})_(\d{6})\.WAV$", re.IGNORECASE)

for dirpath, dirnames, filenames in os.walk(source_root):
    # Skip hidden directories
    dirnames[:] = [d for d in dirnames if not d.startswith(".")]

    for filename in filenames:
        # Skip hidden files
        if filename.startswith("."):
            continue

        match = pattern.match(filename)
        if not match:
            continue

        prefix, date_part, time_part = match.groups()
        hour = time_part[0:2]
        minute = time_part[2:4]
        second = time_part[4:6]

        # Keep only files at :00:00 or :30:00
        if (minute in ("00", "30")) and second == "00":
            src_path = os.path.join(dirpath, filename)
            rel_dir = os.path.relpath(dirpath, source_root)
            dest_dir = destination_root
            os.makedirs(dest_dir, exist_ok=True)
            dest_path = os.path.join(dest_dir, filename)

            if dry_run:
                print(f"[DRY RUN] Would copy: {src_path} -> {dest_path}")
            else:
                shutil.copy2(src_path, dest_path)
                print(f"Copied: {src_path} -> {dest_path}")

print(f"\n✅ Done! (Dry run = {dry_run})")