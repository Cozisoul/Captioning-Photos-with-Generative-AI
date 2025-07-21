import os
from pathlib import Path
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration, Blip2Processor, Blip2ForConditionalGeneration
import torch

# --- Configuration ---
# Set the directory where your images are stored.
# Create a folder named 'images' in your project and put your pictures there.
IMAGE_DIR = Path("images")

# Choose which model to use by uncommenting ONE of the sections below.

# --- Option 1: Standard BLIP Model (Smaller, Faster, Recommended for most users) ---
MODEL_NAME = "Salesforce/blip-image-captioning-base"
processor = BlipProcessor.from_pretrained(MODEL_NAME)
model = BlipForConditionalGeneration.from_pretrained(MODEL_NAME)
print(f"Loaded smaller model: {MODEL_NAME}")

# --- Option 2: Advanced BLIP-2 Model (Larger, more powerful, requires >10GB space & RAM) ---
# NOTE: Uncomment the 3 lines below to use the larger model. Be patient, the download is large!
# MODEL_NAME = "Salesforce/blip2-opt-2.7b"
# processor = Blip2Processor.from_pretrained(MODEL_NAME)
# model = Blip2ForConditionalGeneration.from_pretrained(MODEL_NAME, torch_dtype=torch.float16)
# print(f"Loaded LARGE model: {MODEL_NAME}")


def caption_image_file(image_path: Path) -> str:
    """Generates a caption for a single image file."""
    try:
        raw_image = Image.open(image_path).convert('RGB')
        
        # Process the image
        inputs = processor(raw_image, return_tensors="pt")
        
        # Generate a caption
        out = model.generate(**inputs, max_new_tokens=50)
        
        # Decode and return the caption
        caption = processor.decode(out[0], skip_special_tokens=True)
        return caption
    except Exception as e:
        return f"Error processing file: {e}"

def main():
    """
    Main function to find images, generate captions, and save them to a file.
    """
    if not IMAGE_DIR.is_dir():
        print(f"Error: The directory '{IMAGE_DIR}' was not found.")
        print("Please create it and add some images (.jpg, .jpeg, .png).")
        return

    image_extensions = ["*.jpg", "*.jpeg", "*.png"]
    image_paths = []
    for ext in image_extensions:
        image_paths.extend(IMAGE_DIR.glob(ext))

    if not image_paths:
        print(f"No images found in the '{IMAGE_DIR}' directory.")
        return

    print(f"Found {len(image_paths)} images. Starting caption generation...")

    with open("local_captions.txt", "w", encoding="utf-8") as caption_file:
        for img_path in image_paths:
            print(f"Processing: {img_path.name}")
            caption = caption_image_file(img_path)
            caption_file.write(f"{img_path.name}: {caption}\n")
            print(f"  -> Caption: {caption}")

    print(f"\nFinished. All captions saved to local_captions.txt")

if __name__ == "__main__":
    main()