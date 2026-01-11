import argparse
import os
import shutil
import sys
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description='Backup files with timestamp.')
    parser.add_argument('--out', required=True, help='Output directory for backups')
    parser.add_argument('--timestamp', required=True, help='Timestamp string')
    parser.add_argument('file', help='File to backup')

    args = parser.parse_args()

    src_file = Path(args.file)
    if not src_file.exists():
        print(f"Error: Source file {src_file} does not exist.")
        sys.exit(1)

    # Structure: out_dir/timestamp/original_path_structure
    # e.g. .ci-translation-backups/20231010-120000/source/intro/psr.rst

    dest_dir = Path(args.out) / args.timestamp / src_file.parent
    dest_dir.mkdir(parents=True, exist_ok=True)

    dest_file = dest_dir / src_file.name

    try:
        shutil.copy2(src_file, dest_file)
        print(f"Backed up {src_file} to {dest_file}")
    except Exception as e:
        print(f"Error backing up file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
