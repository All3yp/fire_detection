import os
import subprocess
from pathlib import Path
from dotenv import load_dotenv
import requests
import sys

########## Configs ##########
load_dotenv(Path(__file__).resolve().parent.parent / ".env")
DAGSHUB_TOKEN = os.getenv("DAGSHUB_TOKEN")
USERNAME      = os.getenv("USERNAME")
REPO          = os.getenv("REPO_NAME")
BRANCH        = os.getenv("DAGSHUB_BRANCH", "main")
REPO_PATH     = f"{USERNAME}/{REPO}"
##############################

if not all([DAGSHUB_TOKEN, USERNAME, REPO]):
    raise ValueError("❌ .env must contain DAGSHUB_TOKEN, USERNAME, REPO_NAME")

def testar_conexao_dagshub(token):
    print("🔐 Testing DagsHub authentication...")
    
    # First test user authentication
    user_url = "https://dagshub.com/api/v1/user"
    response = requests.get(user_url, auth=(USERNAME, token))
    if response.status_code != 200:
        print(f"❌ User authentication failed ({response.status_code}): {response.text}")
        return False
    
    # Then test repository access
    url = f"https://dagshub.com/api/v1/repos/{USERNAME}/{REPO}"
    response = requests.get(url, auth=(USERNAME, token))
    if response.status_code == 200:
        print("✅ DagsHub connection OK")
        return True
    else:
        print(f"❌ Repository access failed ({response.status_code}): {response.text}")
        print(f"Trying to access: {url}")
        return False

def install_dagshub_client():
    print("🔧 Checking DagsHub client...")
    try:
        subprocess.run(["dagshub", "--help"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("📦 Installing/Upgrading DagsHub client...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-U", "dagshub"], check=True)
        print("✅ DagsHub client installed/updated successfully")

def login_dagshub():
    print("🔐 Performing automatic login to DagsHub via token...")
    try:
        subprocess.run(["dagshub", "login", "--token", DAGSHUB_TOKEN], check=True)
        print("✅ Login successful")
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Warning during login: {e.stderr}")

def upload_datasets():
    # decide which datasets
    datasets_to_upload = sys.argv[1:] or ["datasets/"]
    print("📋 Upload list:", datasets_to_upload)

    for dataset_path in datasets_to_upload:
        path_obj = Path(dataset_path)
        if not path_obj.exists():
            print(f"⚠️  Not found, skipping: {dataset_path}")
            continue

        print(f"📁 Uploading: {dataset_path}")
        try:
            subprocess.run([
                "dagshub", "upload",
                REPO_PATH,
                dataset_path,
                f"data/{path_obj.name}/",
                "--bucket", "--update", "-v",
                "--branch", BRANCH
            ], check=True)
            print(f"✅ Completed: {dataset_path}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Upload error: {e.stderr or e}")

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
