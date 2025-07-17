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
    
    # Store original directory
    original_dir = os.getcwd()
    
    # Change to dataset directory so relative paths in annotations work
    os.chdir('/mnt/FASDD_CV')
    print(f"📁 Changed to dataset directory: {os.getcwd()}")
    
    try:
        # Load model (downloads automatically if doesn't exist)
        model = YOLO(os.path.join(original_dir, model_name))
        dst_dir = os.path.join(original_dir, f"models/{ts}")

        results = model.train(
            data="/home/sharkobau/code/fire_detection/fasdd.yaml",     # Full path to YAML file
            epochs=50,             # Aumentar epochs para melhor convergência do modelo menor
            batch=16,              # Manter batch menor ou ajustar conforme testes
            imgsz=320,             # Manter este tamanho para o embarcado
            device="cpu",          # Ajustado para CPU (Linux environment)
            workers=8,             # Mantenha ou ajuste conforme CPUs disponíveis
            cache="disk",          # Pode ser mais seguro para 32GB RAM e dataset grande
            amp=True,              # Manter para treino mais rápido
            patience=10,           # Aumentar paciência para um treino mais completo
            verbose=True,
            val=True,
            plots=True,
            save=True,
            project=os.path.join(original_dir, 'runs/detect'),
            name='train',
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
        
    finally:
        # Always return to original directory
        os.chdir(original_dir)

if __name__ == "__main__":
    # Debug: Check if YAML file exists
    import os
    yaml_path = "/home/sharkobau/code/fire_detection/fasdd.yaml"
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
