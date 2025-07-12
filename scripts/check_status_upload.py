import os
import requests
from pathlib import Path
from dotenv import load_dotenv
import json

########## Configs ##########
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")
DAGSHUB_TOKEN = os.getenv("DAGSHUB_TOKEN")
USERNAME = os.getenv("USERNAME")
REPO = os.getenv("REPO_NAME")
##############################

def check_dagshub_repo():
    """Check if repository exists and user authentication"""
    print("🔍 Checking DagsHub repository status...")
    
    # Check user authentication
    user_url = "https://dagshub.com/api/v1/user"
    response = requests.get(user_url, auth=(USERNAME, DAGSHUB_TOKEN))
    
    if response.status_code == 200:
        user_info = response.json()
        print(f"✅ User authenticated: {user_info.get('login', USERNAME)}")
    else:
        print(f"❌ User authentication failed: {response.status_code}")
        print(f"Response: {response.text}")
        return False
    
    # Check if repository exists
    repo_url = f"https://dagshub.com/api/v1/repos/{USERNAME}/{REPO}"
    response = requests.get(repo_url, auth=(USERNAME, DAGSHUB_TOKEN))
    
    if response.status_code == 200:
        repo_info = response.json()
        print(f"✅ Repository exists: {repo_info.get('full_name')}")
        return True
    elif response.status_code == 404:
        print(f"❌ Repository '{USERNAME}/{REPO}' not found")
        return False
    else:
        print(f"❌ Error checking repository: {response.status_code}")
        print(f"Response: {response.text}")
        return False

def list_user_repos():
    """List all repositories for the user"""
    print("📂 Listing your DagsHub repositories...")
    
    repos_url = f"https://dagshub.com/api/v1/users/{USERNAME}/repos"
    response = requests.get(repos_url, auth=(USERNAME, DAGSHUB_TOKEN))
    
    if response.status_code == 200:
        repos = response.json()
        if repos:
            print(f"Found {len(repos)} repositories:")
            for repo in repos:
                print(f"  - {repo['full_name']}")
        else:
            print("No repositories found")
        return repos
    else:
        print(f"❌ Error listing repositories: {response.status_code}")
        return []

def create_dagshub_repo():
    """Create a new repository on DagsHub"""
    print(f"🆕 Creating repository '{REPO}'...")
    
    create_url = "https://dagshub.com/api/v1/user/repos"
    data = {
        "name": REPO,
        "description": "Fire and Smoke Detection Dataset using YOLO",
        "private": False,
        "auto_init": True
    }
    
    response = requests.post(create_url, json=data, auth=(USERNAME, DAGSHUB_TOKEN))
    
    if response.status_code == 201:
        repo_info = response.json()
        print(f"✅ Repository created successfully: {repo_info['full_name']}")
        print(f"🔗 Repository URL: {repo_info['html_url']}")
        return True
    else:
        print(f"❌ Error creating repository: {response.status_code}")
        print(f"Response: {response.text}")
        return False

if __name__ == "__main__":
    print("🚀 DagsHub Repository Status Check...")
    print(f"Username: {USERNAME}")
    print(f"Repository: {REPO}")
    print("-" * 50)
    
    if not DAGSHUB_TOKEN:
        print("❌ DAGSHUB_TOKEN not found in .env file")
        exit(1)
    
    # Check if repo exists
    if check_dagshub_repo():
        print("✅ Repository is accessible. You can proceed with upload.")
    else:
        print("\n📋 Repository not found. Options:")
        print("1. Create a new repository")
        print("2. Check existing repositories")
        print("3. Update .env with correct repository name")
        
        choice = input("\nWhat would you like to do? (1/2/3): ").strip()
        
        if choice == "1":
            if create_dagshub_repo():
                print("\n✅ Repository created! You can now run the upload script.")
            else:
                print("\n❌ Failed to create repository.")
        
        elif choice == "2":
            repos = list_user_repos()
            if repos:
                print("\nYou can update your .env file with one of these repository names.")
        
        elif choice == "3":
            print("\nPlease update your .env file with the correct repository name.")
            print("Current .env values:")
            print(f"USERNAME={USERNAME}")
            print(f"REPO_NAME={REPO}")
        
        else:
            print("Invalid choice. Please run the script again.")
