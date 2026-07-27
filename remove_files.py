#!/usr/bin/env python3

import os
import sys

def remove_file(path):
    if os.path.lexists(path):  # True even for broken symlinks
        try:
            os.remove(path)
            print(f"Removed: {path}")
        except IsADirectoryError:
            print(f"Skipped directory: {path}")
        except Exception as e:
            print(f"Failed to remove {path}: {e}")
    else:
        print(f"Not found: {path}")

def main(list_file):
    with open(list_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            # Skip empty lines and comments
            if not line or line.startswith("#"):
                continue

            parts = line.split(";SYMLINK=")

            # Remove the main file
            remove_file(parts[0])

            # Remove the symlink if present
            if len(parts) == 2:
                remove_file(parts[1])

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} file_list.txt")
        sys.exit(1)

    main(sys.argv[1])
