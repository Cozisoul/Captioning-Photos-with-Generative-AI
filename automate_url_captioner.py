import requests
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
from transformers import AutoProcessor, BlipForConditionalGeneration

# --- 1. Load the Pretrained Model and Processor ---
# It's good practice to use the specific model you intend to use.
# AutoProcessor can work, but being explicit is often better.
processor = AutoProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# --- 2. Scrape the Webpage ---
# URL of the page to scrape
url = "https://en.wikipedia.org/wiki/IBM"
print(f"Scraping images from: {url}")

# Download the page
response = requests.get(url)
# Parse the page with BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find all img elements
img_elements = soup.find_all('img')
print(f"Found {len(img_elements)} image tags.")

# --- 3. Process Images and Generate Captions ---
# Open a file to write the captions
with open("captions.txt", "w", encoding="utf-8") as caption_file:
    # Iterate over each img element
    for img_element in img_elements:
        img_url = img_element.get('src')
        
        # Skip if the src attribute is missing
        if not img_url:
            continue

        # Correct the URL if it's a relative URL (starts with //)
        if img_url.startswith('//'):
            img_url = 'https:' + img_url
        
        # Skip non-http URLs and SVGs
        if not img_url.startswith(('http://', 'https://')) or '.svg' in img_url:
            continue
            
        try:
            print(f"Processing image: {img_url}")
            # Download the image
            img_response = requests.get(img_url, timeout=5) # Added a timeout
            img_response.raise_for_status() # Raise an exception for bad status codes
            
            # Convert the image data to a PIL Image
            raw_image = Image.open(BytesIO(img_response.content)).convert('RGB')
            
            # Skip very small images (likely icons or spacers)
            if raw_image.size[0] < 100 or raw_image.size[1] < 100:
                print("  -> Skipping small image.")
                continue
            
            # Process the image
            inputs = processor(images=raw_image, return_tensors="pt")
            
            # Generate a caption for the image
            out = model.generate(**inputs, max_new_tokens=50)
            
            # Decode the generated tokens to text
            caption = processor.decode(out[0], skip_special_tokens=True)
            
            # Write the caption to the file, prepended by the image URL
            caption_file.write(f"{img_url}: {caption}\n")
            print(f"  -> Caption: {caption}")

        except Exception as e:
            print(f"  -> Error processing image {img_url}: {e}")
            continue

print("\nFinished. Captions saved to captions.txt")