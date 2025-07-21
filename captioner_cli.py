import argparse
import os
from pathlib import Path
from PIL import Image
from io import BytesIO
import requests
from bs4 import BeautifulSoup
from transformers import BlipProcessor, BlipForConditionalGeneration

# --- 1. Load the Model and Processor (Load once) ---
MODEL_NAME = "Salesforce/blip-image-captioning-base"
processor = BlipProcessor.from_pretrained(MODEL_NAME)
model = BlipForConditionalGeneration.from_pretrained(MODEL_NAME)
print(f"Loaded model: {MODEL_NAME}")

# --- 2. Define Core Functions ---
def generate_caption(image: Image.Image) -> str:
    """Generates a caption for a single PIL Image."""
    try:
        inputs = processor(images=image, return_tensors="pt")
        out = model.generate(**inputs, max_new_tokens=50)
        caption = processor.decode(out[0], skip_special_tokens=True)
        return caption
    except Exception as e:
        return f"Error generating caption: {e}"

def process_local_directory(directory: Path):
    """Finds images in a local directory, captions them, and saves to a file."""
    print(f"\nProcessing local directory: {directory}")
    if not directory.is_dir():
        print(f"Error: Directory '{directory}' not found.")
        return

    image_extensions = ["*.jpg", "*.jpeg", "*.png"]
    image_paths = []
    for ext in image_extensions:
        image_paths.extend(directory.glob(ext))

    if not image_paths:
        print(f"No images found in '{directory}'.")
        return

    with open("local_captions.txt", "w", encoding="utf-8") as f:
        for img_path in image_paths:
            print(f"  - Processing: {img_path.name}")
            image = Image.open(img_path).convert("RGB")
            caption = generate_caption(image)
            f.write(f"{img_path.name}: {caption}\n")
    print("Finished. Captions saved to local_captions.txt")

def process_url(url: str):
    """Scrapes a URL for images, captions them, and saves to a file."""
    print(f"\nProcessing URL: {url}")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        img_elements = soup.find_all('img')

        with open("url_captions.txt", "w", encoding="utf-8") as f:
            for img in img_elements:
                img_url = img.get('src')
                if not img_url: continue

                if img_url.startswith('//'):
                    img_url = 'https:' + img_url
                if not img_url.startswith(('http', 'https')):
                    continue
                
                try:
                    img_response = requests.get(img_url, timeout=5)
                    img_response.raise_for_status()
                    image = Image.open(BytesIO(img_response.content)).convert("RGB")
                    
                    if image.size[0] < 100 or image.size[1] < 100: continue

                    print(f"  - Processing image: {img_url}")
                    caption = generate_caption(image)
                    f.write(f"{img_url}: {caption}\n")
                except Exception as e:
                    print(f"    -> Could not process image {img_url}. Reason: {e}")
        print("Finished. Captions saved to url_captions.txt")
    except Exception as e:
        print(f"Error scraping URL '{url}'. Reason: {e}")

# --- 3. Set up Command-Line Argument Parsing ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Image Captioner CLI Tool")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--local_dir", type=str, help="Path to the local directory of images to process.")
    group.add_argument("--url", type=str, help="URL of a webpage to scrape for images.")
    
    args = parser.parse_args()

    if args.local_dir:
        process_local_directory(Path(args.local_dir))
    elif args.url:
        process_url(args.url)