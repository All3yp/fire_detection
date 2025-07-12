import os
import subprocess
from pathlib import Path
from dotenv import load_dotenv
import requests

########## Configs ##########
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")
DAGSHUB_TOKEN = os.getenv("DAGSHUB_TOKEN")
USERNAME = os.getenv("USERNAME")
REPO = os.getenv("REPO")
REPO_PATH = f"{USERNAME}/{REPO}"
##############################

if not DAGSHUB_TOKEN:
    raise ValueError("❌ DAGSHUB_TOKEN not found in .env")

def testar_conexao_dagshub(token):
    print("🔐 Testing DagsHub authentication...")
    url = f"https://dagshub.com/api/v1/repos/{USERNAME}/{REPO}"
    response = requests.get(url, auth=(USERNAME, token))
    if response.status_code == 200:
        print("✅ DagsHub connection OK")
        return True
    print(f"❌ Authentication failed ({response.status_code}): {response.text}")
    return False

def install_dagshub_client():
    print("🔧 Checking DagsHub client...")
    try:
        subprocess.run(["dagshub", "--help"], capture_output=True, text=True, check=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("📦 Installing DagsHub client...")
        subprocess.run(["uv", "pip", "install", "dagshub", "--upgrade"], check=True)

def login_dagshub():
    print("🔐 Performing automatic login to DagsHub via token...")
    try:
        subprocess.run(["dagshub", "login", "--token", DAGSHUB_TOKEN], check=True)
        print("✅ Login successful")
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Warning during login: {e.stderr}")

def upload_datasets():
    print("📤 Uploading datasets to DagsHub bucket...")

    datasets_to_upload = [
        "datasets/"
    ]
    
    for dataset_path in datasets_to_upload:
        path_obj = Path(dataset_path)
        if not path_obj.exists():
            print(f"⚠️  Dataset not found: {dataset_path}, skipping...")
            continue

        print(f"📁 Uploading: {dataset_path}")
        try:
            subprocess.run([
                "dagshub", "upload",
                REPO_PATH,
                dataset_path,
                f"data/{path_obj.name}/",
                "--bucket", "--update", "-v"
            ], check=True)
            print(f"✅ Upload completed: {dataset_path}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Upload error for {dataset_path}: {e.stderr}")

if __name__ == "__main__":
    print("🚀 Starting upload to DagsHub bucket...")

    if not testar_conexao_dagshub(DAGSHUB_TOKEN):
        raise SystemExit("⛔ Invalid token or repository inaccessible.")

    try:
        install_dagshub_client()
        login_dagshub()
        upload_datasets()
        print("✅ Upload completed successfully!")
    except Exception as e:
        print(f"❌ Error during process: {e}")
        raise
