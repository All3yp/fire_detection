from ultralytics import YOLO
import os
from pathlib import Path

def test_trained_model(model_path, test_images=None):
    """
    Test the trained YOLO model on sample images
    """
    if not os.path.exists(model_path):
        print(f"❌ Model not found: {model_path}")
        return
    
    print(f"🔍 Loading model: {model_path}")
    model = YOLO(model_path)
    
    # Default test images if none provided
    if test_images is None:
        test_images = [
            '/mnt/FASDD_CV/images/fire_CV010684.jpg',           # Fire image
            '/mnt/FASDD_CV/images/smoke_CV009187.jpg',          # Smoke image  
            '/mnt/FASDD_CV/images/bothFireAndSmoke_CV009840.jpg', # Both
            '/mnt/FASDD_CV/images/neitherFireNorSmoke_CV012364.jpg' # Neither
        ]
    
    for img_path in test_images:
        if not os.path.exists(img_path):
            print(f"⚠️  Image not found: {img_path}")
            continue
            
        print(f"\n🖼️  Testing: {os.path.basename(img_path)}")
        
        # Run inference
        results = model(img_path, verbose=False)
        
        if len(results) > 0:
            boxes = results[0].boxes
            if boxes is not None and len(boxes) > 0:
                print(f"✅ Detected {len(boxes)} objects:")
                for i, box in enumerate(boxes):
                    class_id = int(box.cls)
                    confidence = float(box.conf)
                    class_name = model.names[class_id]
                    print(f"   {i+1}. {class_name}: {confidence:.3f}")
            else:
                print("🔍 No objects detected")
        else:
            print("❌ No results returned")

def main():
    print("🔥 FASDD Model Testing Script")
    print("=" * 40)
    
    # Test the latest trained model
    model_paths = [
        '/home/sharkobau/code/fire_detection/runs/detect/train_extended/weights/best.pt',
        '/home/sharkobau/code/fire_detection/runs/detect/train15/weights/best.pt'
    ]
    
    for model_path in model_paths:
        if os.path.exists(model_path):
            print(f"\n📊 Testing model: {model_path}")
            test_trained_model(model_path)
            break
    else:
        print("❌ No trained models found!")

if __name__ == "__main__":
    main()
