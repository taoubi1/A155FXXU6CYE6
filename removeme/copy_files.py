#!/usr/bin/env python3

import os
import sys
import shutil

def copy_item(rel_path, src_root, dst_root):
    src = os.path.join(src_root, rel_path)
    dst = os.path.join(dst_root, rel_path)

    if not os.path.lexists(src):
        print(f"Not found: {src}")
        return

    os.makedirs(os.path.dirname(dst), exist_ok=True)

    try:
        if os.path.islink(src):
            target = os.readlink(src)
            if os.path.lexists(dst):
                os.remove(dst)
            os.symlink(target, dst)
            print(f"Copied symlink: {rel_path} -> {target}")
        else:
            shutil.copy2(src, dst)
            print(f"Copied: {rel_path}")
    except Exception as e:
        print(f"Failed: {rel_path}: {e}")

def main():
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <list_file> <source_dir> <dest_dir>")
        sys.exit(1)

    list_file, src_root, dst_root = sys.argv[1:]

    with open(list_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            parts = line.split(";SYMLINK=")

            copy_item(parts[0], src_root, dst_root)

            if len(parts) == 2:
                copy_item(parts[1], src_root, dst_root)

if __name__ == "__main__":
    main()
