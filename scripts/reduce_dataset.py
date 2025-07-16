import os
import random
import shutil

dataset = 'dataset4gb'
images_dir = os.path.join(os.path.dirname(__file__), '..', '..', dataset, 'images')
annotations_dir = os.path.join(os.path.dirname(__file__), '..', '..', dataset, 'annotations')
labels_dir = os.path.join(os.path.dirname(__file__), '..', '..', dataset, 'labels')

def make_annotations(new_dataset_name, new_annotations_dir, both, neither, fire, smoke):

    train_percent = 0.6
    val_percent = 0.5
    test_percent = 0.4

    random.shuffle(neither)
    random.shuffle(both)
    random.shuffle(fire)
    random.shuffle(smoke)

    train_neither = neither[:int(train_percent * len(neither))]
    train_both = both[:int(train_percent * len(both))]
    train_fire = fire[:int(train_percent * len(fire))]
    train_smoke = smoke[:int(train_percent * len(smoke))]

    val_neither = train_neither[int(val_percent * len(train_neither)):]
    val_both = train_both[int(val_percent * len(train_both)):]
    val_fire = train_fire[int(val_percent * len(train_fire)):]
    val_smoke = train_smoke[int(val_percent * len(train_smoke)):]

    test_neither = neither[-int(test_percent * len(neither)):]
    test_both = both[-int(test_percent * len(both)):]
    test_fire = fire[-int(test_percent * len(fire)):]
    test_smoke = smoke[-int(test_percent * len(smoke)):]

    # Create train.txt
    with open(os.path.join(new_annotations_dir, 'train.txt'), 'w') as f:
        for img in train_neither + train_both + train_fire + train_smoke:
            f.write(f"{new_dataset_name}/images/{img}.jpg\n")

    # Create val.txt
    with open(os.path.join(new_annotations_dir, 'val.txt'), 'w') as f:
        for img in val_neither + val_both + val_fire + val_smoke:
            f.write(f"{new_dataset_name}/images/{img}.jpg\n")

    # Create test.txt
    with open(os.path.join(new_annotations_dir, 'test.txt'), 'w') as f:
        for img in test_neither + test_both + test_fire + test_smoke:
            f.write(f"{new_dataset_name}/images/{img}.jpg\n")

if __name__ == '__main__':
    # Get set of image filenames (with extension)
    image_files = {os.path.splitext(f)[0] for f in os.listdir(images_dir) if f.endswith(('.jpg', '.png'))}
    sample_size = 10

    neither = [f for f in image_files if "neitherFireNorSmoke" in f][:sample_size]
    both = [f for f in image_files if "bothFireAndSmoke" in f][:sample_size]
    fire = [f for f in image_files if "fire_" in f][:sample_size]
    smoke = [f for f in image_files if "smoke_" in f][:sample_size]

    print(f"Neither: {len(neither)}, Both: {len(both)}, Fire: {len(fire)}, Smoke: {len(smoke)}")

    # Create new dataset_sample directory structure
    new_dataset_name = f'dataset{sample_size}'
    new_dataset_dir = os.path.join(os.path.dirname(__file__), '..', '..', new_dataset_name)
    new_images_dir = os.path.join(new_dataset_dir, 'images')
    new_annotations_dir = os.path.join(new_dataset_dir, 'annotations')
    new_labels_dir = os.path.join(new_dataset_dir, 'labels')

    os.makedirs(new_images_dir, exist_ok=True)
    os.makedirs(new_annotations_dir, exist_ok=True)
    os.makedirs(new_labels_dir, exist_ok=True)

    # Copy images to new directory
    for file in neither + both + fire + smoke:
        src = os.path.join(images_dir, f"{file}.jpg")
        dst = os.path.join(new_images_dir, f"{file}.jpg")
        if os.path.exists(src):
            shutil.copy(src, dst)
        else:
            print(f"Warning: {src} does not exist, skipping.")

        src = os.path.join(labels_dir, f"{file}.txt")
        dst = os.path.join(new_labels_dir, f"{file}.txt")
        if os.path.exists(src):
            shutil.copy(src, dst)
        else:
            print(f"Warning: {src} does not exist, skipping.")

    make_annotations(new_dataset_name, new_annotations_dir, both, neither, fire, smoke)

    # Copy class.names file
    names_src = os.path.join(os.path.dirname(__file__), '..', '..', dataset, 'class.names')
    names_dst = os.path.join(new_dataset_dir, 'class.names')
    if os.path.exists(names_src):
        shutil.copy(names_src, names_dst)
    else:
        print(f"Warning: {names_src} does not exist, skipping.")

    


    