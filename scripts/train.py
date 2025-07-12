from ultralytics import YOLO
from datetime import datetime
import shutil, os, time

def train_fasdd_model(
    data_config="fasdd.yaml",
    model_name="yolov9s.pt",
    epochs=15,
    batch=16,
    imgsz=320,
    device=0,
    workers=2,
    cache=True,
    amp=True,
    patience=5,
    save_period=5,
    verbose=True
):
    """
    Train YOLO model on FASDD dataset
    
    Args:
        data_config (str): Path to dataset YAML configuration
        model_name (str): YOLO model to use
        epochs (int): Number of training epochs
        batch (int): Batch size (try 32 if VRAM allows; reduce if OOM)
        imgsz (int): Image size for training
        device (int): GPU device ID (0 for first GPU)
        workers (int): Number of worker threads
        cache (bool): Cache images for faster training
        amp (bool): Use mixed precision training
        patience (int): Early stopping patience
        save_period (int): Save checkpoint every N epochs
        verbose (bool): Verbose output
    """
    
    # Generate timestamp for logging
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Load model (downloads automatically if doesn't exist)
    model = YOLO(model_name)
    
    # Train the model
    results = model.train(
        data=data_config,
        epochs=epochs,
        batch=batch,
        imgsz=imgsz,
        device=device,
        workers=workers,
        cache=cache,
        amp=amp,
        patience=patience,
        save_period=save_period,
        verbose=verbose,
    )
    
    # Save CSV metrics
    src = "runs/detect/train/results.csv"
    dst_dir = "training_logs"
    os.makedirs(dst_dir, exist_ok=True)
    
    model_base = model_name.replace('.pt', '')
    dst_file = f"{dst_dir}/{model_base}_{ts}.csv"
    
    if os.path.exists(src):
        shutil.copy(src, dst_file)
        print(f"📈 CSV salvo em {dst_file}")
    else:
        print("⚠️  Arquivo de resultados não encontrado")
    
    return results

if __name__ == "__main__":
    # Train with default parameters
    results = train_fasdd_model()
    
    # Or train with custom parameters (uncomment to use):
    # results = train_fasdd_model(
    #     model_name="yolov9m.pt",
    #     epochs=50,
    #     batch=32,
    #     imgsz=640
    # )
