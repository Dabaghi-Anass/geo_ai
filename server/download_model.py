import os
import requests

MODEL_URL    = "https://drive.usercontent.google.com/download?id=1oZB-6mNWy4Qwj7DjwAh4v4uctFme7LOO&export=download&authuser=0&confirm=t&uuid=8968c8fd-ef25-42c8-ac7e-d06ab155ff31&at=AKSUxGN_DM9mBo-f6VYagPIGHG2Z:1759533344042"
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


if __name__ == "__main__":
    download_model_if_needed()