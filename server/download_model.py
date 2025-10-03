import os
import requests
import rarfile

MODEL_URL    = "https://drive.google.com/uc?export=view&id=1oZB-6mNWy4Qwj7DjwAh4v4uctFme7LOO"
MODEL_PATH   = "best_model.rar"
EXTRACT_DIR  = "best_model"

def download_model_if_needed():
    if not os.path.exists(MODEL_PATH):
        print("Model not found. Downloading...")
        response = requests.get(MODEL_URL, stream=True)
        with open(MODEL_PATH, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        print("Model downloaded.")
    else:
        print("Model already exists.")

def extract_model():
    if not os.path.isdir(EXTRACT_DIR):
        print(f"Extracting {MODEL_PATH} → {EXTRACT_DIR}/")
        with rarfile.RarFile(MODEL_PATH) as rf:
            rf.extractall(EXTRACT_DIR)
        print("Extraction complete.")
    else:
        print("Archive already extracted.")

if __name__ == "__main__":
    download_model_if_needed()
    extract_model()