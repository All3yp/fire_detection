#!/usr/bin/env python3
"""
Recreate annotation files from the actual images in the dataset
"""

import os
import random
from pathlib import Path

def create_annotation_files():
    """
    Create train.txt, val.txt, and test.txt files from actual images
    """
    dataset_dir = Path("/mnt/FASDD_CV")
    images_dir = dataset_dir / "images"
    annotations_dir = dataset_dir / "annotations"
    
    # Find all image files
    print("🔍 Finding all image files...")
    image_files = []
    for ext in ['*.jpg', '*.jpeg', '*.png', '*.bmp']:
        image_files.extend(list(images_dir.glob(ext)))
    
    print(f"📊 Found {len(image_files)} image files")
    
    # Convert to relative paths
    relative_paths = []
    for img_path in image_files:
        rel_path = f"images/{img_path.name}"
        relative_paths.append(rel_path)
    
    # Shuffle for random split
    random.seed(42)  # For reproducible splits
    random.shuffle(relative_paths)
    
    # Split into train/val/test (60%/25%/15%)
    total = len(relative_paths)
    train_end = int(0.6 * total)
    val_end = int(0.85 * total)
    
    train_files = relative_paths[:train_end]
    val_files = relative_paths[train_end:val_end]
    test_files = relative_paths[val_end:]
    
    print(f"📋 Split: {len(train_files)} train, {len(val_files)} val, {len(test_files)} test")
    
    # Write annotation files
    splits = {
        'train.txt': train_files,
        'val.txt': val_files,
        'test.txt': test_files
    }
    
    for filename, files in splits.items():
        filepath = annotations_dir / filename
        with open(filepath, 'w') as f:
            for file_path in files:
                f.write(file_path + '\n')
        print(f"✅ Created {filepath} with {len(files)} entries")
    
    print("🎉 Annotation files recreated successfully!")

if __name__ == "__main__":
    create_annotation_files()
