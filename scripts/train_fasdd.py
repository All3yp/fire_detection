#!/usr/bin/env python3
"""
FASDD Fire and Smoke Detection Training Script
Train YOLO model on FASDD dataset
"""

from ultralytics import YOLO
from datetime import datetime
import shutil
import os
import time

def train_fasdd_model():
    """Train YOLO model on FASDD dataset"""
    
    # Create timestamp for logging
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Initialize YOLO model
    model = YOLO("yolov9s.pt")  # downloads automatically if not exists
    
    # Training parameters
    results = model.train(
        data="fasdd.yaml",      # path to dataset config
        epochs=15,
        batch=16,               # try 32 if VRAM allows; reduce if OOM
        imgsz=320,
        device=0,               # GPU 0
        workers=2,
        cache=True,
        amp=True,               # mixed precision
        patience=5,
        save_period=5,
        verbose=True,
        project="runs/detect",  # save to project/name
        name=f"fasdd_train_{ts}",
    )
    
    # Save CSV metrics
    src = f"runs/detect/fasdd_train_{ts}/results.csv"
    dst_dir = "training_logs"
    os.makedirs(dst_dir, exist_ok=True)
    
    if os.path.exists(src):
        shutil.copy(src, f"{dst_dir}/fasdd_yolov9s_{ts}.csv")
        print(f"📈 CSV salvo em {dst_dir}/fasdd_yolov9s_{ts}.csv")
    else:
        print(f"⚠️  Arquivo CSV não encontrado em {src}")
    
    return results

if __name__ == "__main__":
    print("🔥 Iniciando treinamento FASDD...")
    results = train_fasdd_model()
    print("✅ Treinamento concluído!")
