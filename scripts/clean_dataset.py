#!/usr/bin/env python3
"""
Clean dataset by removing references to non-existent images
"""

import os
import shutil

def clean_annotation_file(annotation_file, image_base_dir):
    """
    Clean annotation file by removing references to non-existent images
    """
    print(f"Cleaning {annotation_file}...")
    
    # Read all lines
    with open(annotation_file, 'r') as f:
        lines = f.readlines()
    
    # Check which images exist
    existing_lines = []
    missing_count = 0
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Convert relative path to absolute path
        if line.startswith('../images/'):
            image_path = os.path.join(image_base_dir, line.replace('../images/', ''))
        elif line.startswith('./images/'):
            image_path = os.path.join(image_base_dir, line.replace('./images/', ''))
        else:
            image_path = os.path.join(image_base_dir, line)
            
        if os.path.exists(image_path):
            existing_lines.append(line)
        else:
            missing_count += 1
            print(f"  Missing: {line}")
    
    # Write back only existing images
    with open(annotation_file, 'w') as f:
        for line in existing_lines:
            f.write(line + '\n')
    
    print(f"  Removed {missing_count} missing images")
    print(f"  Kept {len(existing_lines)} existing images")
    
    return len(existing_lines), missing_count

def main():
    # Set paths
    dataset_dir = "/mnt/FASDD_CV/"
    image_dir = os.path.join(dataset_dir, "images")
    annotation_dir = os.path.join(dataset_dir, "annotations")
    
    # Clean annotation files
    for split in ['train', 'val', 'test']:
        annotation_file = os.path.join(annotation_dir, f"{split}.txt")
        if os.path.exists(annotation_file):
            existing, missing = clean_annotation_file(annotation_file, image_dir)
            print(f"✅ {split}.txt: {existing} existing, {missing} missing")
        else:
            print(f"❌ {annotation_file} not found")
    
    # Remove cache file to force regeneration
    cache_file = os.path.join(annotation_dir, "labels.cache")
    if os.path.exists(cache_file):
        os.remove(cache_file)
        print(f"🗑️  Removed cache file: {cache_file}")

if __name__ == "__main__":
    main()
