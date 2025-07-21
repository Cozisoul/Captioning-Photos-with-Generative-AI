import gradio as gr
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch
import requests
from torchvision import transforms

# --- Part 1: Setup for Image Captioning ---
# Load the captioning model and processor
caption_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
caption_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def caption_image(input_image: Image.Image) -> str:
    """Generates a caption for a given PIL Image."""
    inputs = caption_processor(images=input_image, return_tensors="pt")
    outputs = caption_model.generate(**inputs)
    caption = caption_processor.decode(outputs[0], skip_special_tokens=True)
    return caption

# --- Part 2: Setup for Image Classification ---
# Load the classification model
classify_model = torch.hub.load('pytorch/vision:v0.6.0', 'resnet18', pretrained=True).eval()

# Download the labels
response = requests.get("https://git.io/JJkYN")
labels = response.text.split("\n")

def classify_image(input_image: Image.Image) -> dict:
    """Classifies an image and returns a dictionary of confidences."""
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    processed_image = preprocess(input_image).unsqueeze(0)
    with torch.no_grad():
        prediction = torch.nn.functional.softmax(classify_model(processed_image)[0], dim=0)
        confidences = {labels[i]: float(prediction[i]) for i in range(1000)}
    return confidences

# --- Part 3: Create the Interfaces and Combine Them ---

# Define the first interface (Captioning)
iface_caption = gr.Interface(
    fn=caption_image,
    inputs=gr.Image(type="pil", label="Upload Image for Captioning"),
    outputs=gr.Textbox(label="Generated Caption"),
    title="Image Captioning with BLIP",
    description="Upload an image and the AI will generate a descriptive caption."
)

# Define the second interface (Classification)
iface_classify = gr.Interface(
    fn=classify_image,
    inputs=gr.Image(type="pil", label="Upload Image for Classification"),
    outputs=gr.Label(num_top_classes=3, label="Top 3 Predictions"),
    title="Image Classification with ResNet",
    description="Upload an image and the AI will predict its class."
)

# Combine the interfaces in a tabbed layout
demo = gr.TabbedInterface(
    [iface_caption, iface_classify],
    ["Image Captioning", "Image Classification"]
)

# --- Part 4: Launch the App ---
if __name__ == "__main__":
    demo.launch()