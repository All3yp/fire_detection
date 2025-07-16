import os
import cv2
import random

def load_class_names(names_path):
    with open(names_path, 'r') as f:
        return [line.strip() for line in f.readlines()]

def draw_yolo_boxes(img, label_path, class_names):
    h, w = img.shape[:2]
    if not os.path.exists(label_path):
        return img
    with open(label_path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) < 5:
                continue
            cls, x, y, bw, bh = map(float, parts[:5])
            cls = int(cls)
            x1 = int((x - bw/2) * w)
            y1 = int((y - bh/2) * h)
            x2 = int((x + bw/2) * w)
            y2 = int((y + bh/2) * h)
            color = (0, 255, 0)
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
            label = class_names[cls] if cls < len(class_names) else str(cls)
            cv2.putText(img, label, (x1, y1-5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    return img

def view(dataset_name, folder):
    base_dir = os.path.join(os.path.dirname(__file__), '..', '..')
    train_txt = os.path.join(base_dir, f'{dataset_name}/annotations/{folder}.txt')
    labels_dir = os.path.join(base_dir, f'{dataset_name}/labels')
    names_path = os.path.join(base_dir, f'{dataset_name}/class.names')
    out_dir = os.path.join(base_dir, f'{dataset_name}/annotations/visualized_{folder}')
    os.makedirs(out_dir, exist_ok=True)
    class_names = load_class_names(names_path)
    with open(train_txt, 'r') as f:
        image_paths = [line.strip() for line in f.readlines()]
    for img_path in image_paths:
        abs_img_path = os.path.join(base_dir, img_path) if not os.path.isabs(img_path) else img_path
        img = cv2.imread(abs_img_path)
        if img is None:
            print(f"Could not read {abs_img_path}")
            continue
        img_name = os.path.splitext(os.path.basename(img_path))[0]
        label_path = os.path.join(labels_dir, img_name + '.txt')
        img_annot = draw_yolo_boxes(img, label_path, class_names)
        out_path = os.path.join(out_dir, img_name + '_vis.jpg')
        cv2.imwrite(out_path, img_annot)
        print(f"Saved: {out_path}")

if __name__ == "__main__":
    for folder in ['train', 'val', 'test']:
        view('dataset10', folder)
