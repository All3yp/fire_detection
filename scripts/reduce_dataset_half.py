#!/usr/bin/env python3
"""
Reduce the FASDD dataset by 50 % per class, per split.

Current layout (src):
datasets/
├── images/
└── annotations/
    ├── train.txt  val.txt  test.txt
    └── labels/

Result layout (dst):
datasets_half/
├── images/
└── annotations/
    ├── train.txt  val.txt  test.txt
    └── labels/

Usage:
    python scripts/reduce_dataset_half.py \
        --src datasets \
        --dst datasets_half \
        --symlink          # optional; copy if omitted
"""

import argparse, random, shutil, os
from pathlib import Path
from collections import defaultdict

CLASS_PREFIXES = {
    "fire": "fire_",
    "smoke": "smoke_",
    "bothFireAndSmoke": "bothFireAndSmoke_",
    "neitherFireNorSmoke": "neitherFireNorSmoke_",
}
SPLITS = ["train", "val", "test"]

def args():
    p = argparse.ArgumentParser()
    p.add_argument("--src", required=True, help="path to original datasets folder")
    p.add_argument("--dst", required=True, help="output folder for 50-% subset")
    p.add_argument("--symlink", action="store_true", help="use symlinks instead of copies")
    p.add_argument("--seed", type=int, default=42)
    return p.parse_args()

def read_paths(list_file: Path):
    with list_file.open() as f:
        return [ln.strip() for ln in f if ln.strip()]

def group_by_class(paths):
    g = defaultdict(list)
    for p in paths:
        name = Path(p).name
        for cls, pref in CLASS_PREFIXES.items():
            if name.startswith(pref):
                g[cls].append(p); break
    return g

def select_half(grouped):
    result = []
    for cls, items in grouped.items():
        k = len(items) // 2
        result.extend(random.sample(items, k))
    return result

def link_or_copy(src, dst, use_symlink):
    dst.parent.mkdir(parents=True, exist_ok=True)
    if use_symlink:
        os.symlink(os.path.abspath(src), dst)
    else:
        shutil.copy2(src, dst)

def handle_split(split, SRC, DST, use_symlink):
    list_src = SRC / "annotations" / f"{split}.txt"
    items = read_paths(list_src)
    chosen = select_half(group_by_class(items))

    # write reduced list-file
    list_dst = DST / "annotations" / f"{split}.txt"
    list_dst.parent.mkdir(parents=True, exist_ok=True)
    list_dst.write_text("\n".join(chosen))

    # copy / link images and labels
    for rel in chosen:
        img_src = SRC / rel
        lbl_src = SRC / "annotations" / "labels" / (Path(rel).stem + ".txt")

        img_dst = DST / rel
        lbl_dst = DST / "annotations" / "labels" / lbl_src.name

        link_or_copy(img_src, img_dst, use_symlink)
        link_or_copy(lbl_src, lbl_dst, use_symlink)

def write_yaml(dst_root):
    yaml = f"""# 50 % FASDD subset
path: {dst_root}
train: annotations/train.txt
val:   annotations/val.txt
test:  annotations/test.txt
nc: 4
names: [fire, smoke, bothFireAndSmoke, neitherFireNorSmoke]
"""
    (dst_root / "fasdd_half.yaml").write_text(yaml)

def main():
    arg = args()
    random.seed(arg.seed)
    SRC, DST = Path(arg.src), Path(arg.dst)

    for split in SPLITS:
        print(f"→ processing {split}")
        handle_split(split, SRC, DST, arg.symlink)

    write_yaml(DST)
    print(f"✅ Done. Subset at: {DST}")

if __name__ == "__main__":
    main()
