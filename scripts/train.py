from ultralytics import YOLO
from datetime import datetime
import shutil, os, time

def train_fasdd_model(model_name="yolov8n.pt"):
    """
    Train YOLO model on FASDD dataset
    
    Args:
        model_name (str): YOLO model to use
    """
    
    # Generate timestamp for logging
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Load model (downloads automatically if doesn't exist)
    model = YOLO(model_name)
    dst_dir = f"models/{ts}"

    # Train the model
    # results = model.train(
    #     data="fasdd.yaml",      # Path to dataset YAML file
    #     epochs=5,               # Number of training epochs
    #     batch=32,               # Batch size
    #     imgsz=320,               # Image size (pixels)
    #     device="mps",           # Device to use (0 for GPU, 'cpu' for CPU, 'mps' for Apple Silicon)
    #     workers=16,             # Number of dataloader worker threads
    #     cache="disk",           # Cache images for faster training
    #     amp=True,               # Use Automatic Mixed Precision (faster on supported hardware)
    #     patience=2,             # Early stopping patience (epochs)
    #     save_period=5,          # Save checkpoint every N epochs
    #     verbose=True,           # Print detailed training logs
    # )

    results = model.train(
        data="fasdd.yaml",
        epochs=5,
        batch=16,             
        imgsz=320,
        device="mps",
        workers=8,           
        cache="ram",
        amp=True,
        patience=5,
        verbose=True,
        val=True,
        plots=True,
        save=True,
    )
    print("✅ Training completed successfully!")

    # save trained model
    os.makedirs(dst_dir, exist_ok=True)
    model_path = f"{dst_dir}/{model_name.replace('.pt', '')}_{ts}.pt"
    model.save(model_path)
    print(f"✅ Model saved to {model_path}")

    # Print other useful metrics if available
    if hasattr(results, "box"):
        print(f"mAP50: {results.box.map50:.4f}")
        print(f"mAP50-95: {results.box.map:.4f}")
    if hasattr(results, "results_dict"):
        print("Other metrics:", results.results_dict)

    return results

if __name__ == "__main__":
    # Debug: Check if YAML file exists
    import os
    yaml_path = "fasdd.yaml"
    print(f"🔍 Checking YAML file: {yaml_path}")
    print(f"📁 Current directory: {os.getcwd()}")
    print(f"✅ YAML exists: {os.path.exists(yaml_path)}")
    
    if os.path.exists(yaml_path):
        print(f"📋 Starting training...")
        # Train with default parameters
        results = train_fasdd_model()
    else:
        print(f"❌ YAML file not found at: {os.path.abspath(yaml_path)}")
    
    # Or train with custom parameters (uncomment to use):
    # results = train_fasdd_model(
    #     model_name="yolov9m.pt",
    #     epochs=50,
    #     batch=32,
    #     imgsz=640
    # )
