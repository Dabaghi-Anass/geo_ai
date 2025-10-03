from functools import lru_cache
import os
import torch
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
from PIL import Image
import torchvision.transforms as transforms
from syntax_correcter import correct_syntax
MODEL_PATH="best_model"

@lru_cache()
def load_model(model_path):
    model = VisionEncoderDecoderModel.from_pretrained(model_path)
    processor = ViTImageProcessor.from_pretrained(model_path)
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    tokenizer.pad_token = "[PAD]"
    tokenizer.add_tokens(["[PAD]"])
    model.config.pad_token_id = tokenizer.convert_tokens_to_ids("[PAD]")

    return model, processor, tokenizer

model, processor, tokenizer = load_model(MODEL_PATH)
print("Model loaded successfully.")
# Image pre-processing transform
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=processor.image_mean, std=processor.image_std)
])

# Load and process test image
def load_image(image_path):
    image = Image.open(image_path).convert("RGB")
    pixel_values = transform(image).unsqueeze(0)
    return pixel_values

def generate_caption(image_path):
    pixel_values = load_image(image_path)

    attention_mask = torch.ones(pixel_values.shape[:2], dtype=torch.long)  # (batch_size, num_pixels)

    with torch.no_grad():
        output_ids = model.generate(
            pixel_values,
            max_length=64,
            do_sample=True,
            top_k=50,
            top_p=0.95,
            attention_mask=attention_mask  # from previous fix
        )
    caption = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return caption

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/generate-caption")
async def generate_caption_endpoint(file: UploadFile = File(...)):
    image = await file.read()
    with open("temp.jpg", "wb") as f:
        f.write(image)
    caption = generate_caption("temp.jpg")
    os.remove("temp.jpg")
    return {"generated": caption, "corrected": correct_syntax(caption)}

@app.post("/correct-syntax")
async def correct_syntax_endpoint(text: str):
    new_text = correct_syntax(text)
    return {"corrected": new_text}

@app.get("/health")
async def health():
    return {"status": "ok", "message":"server is healthy"}

app.mount("/", StaticFiles(directory="public", html=True), name="static")