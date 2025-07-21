# AI Vision Toolkit: Image Captioning & Classification

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Gradio](https://img.shields.io/badge/Gradio-4.x-orange.svg)](https://www.gradio.app/)
[![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Transformers-yellow.svg)](https://huggingface.co/docs/transformers/index)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.x-ee4c2c.svg)](https://pytorch.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

This repository contains a multi-functional AI toolkit that can generate descriptive captions and classify the content of images. This project was developed as part of the **"Building Generative AI-Powered Applications with Python"** course by IBM on Coursera.

## Project Purpose & Features

The primary goal of this project is to create a practical, user-friendly toolkit for advanced vision-language AI models. The project includes three main components:

1.  **Interactive Web App (`app.py`):** A Gradio web interface with two tabs for real-time interaction.
    *   **Image Captioning Tab:** Upload an image and the Salesforce BLIP model will generate a descriptive text caption.
    *   **Image Classification Tab:** Upload an image and a pre-trained ResNet model will identify the object, providing the top 3 predictions.
2.  **Automated URL Scraper (`automate_url_captioner.py`):** A command-line tool that scrapes a given webpage, extracts all images, and generates captions for them, saving the results to a text file.
3.  **Local Batch Processor (`caption_local_files.py`):** A powerful script that processes an entire folder of local images at once, generating a caption for each and saving the output.

## Demo Screenshots

Here is the interactive web application in action.

**Image Captioning Tab:**
*The model accurately identifies "a man in a blue shirt" from the input image.*![Image Captioning Demo](./captioning-screenshot.png)

**Image Classification Tab:**
*The model correctly classifies the image as containing a 'web site' with high confidence.*
![Image Classification Demo](./classification-screenshot.png)

## Tech Stack

*   **Python**
*   **Gradio:** For building the interactive web UI.
*   **Hugging Face `transformers`:** For loading and interfacing with pre-trained models.
*   **PyTorch:** As the backend deep learning framework.
*   **BeautifulSoup4:** For HTML parsing and web scraping.
*   **Models:**
    *   `Salesforce/blip-image-captioning-base` & `blip2-opt-2.7b` for captioning.
    *   `pytorch/vision/resnet18` for classification.

## Setup and Running the Toolkit

To run this application on your local machine, please follow these initial setup steps.

**1. Clone the Repository**
```bash
git clone https://github.com/cozisoul/Captioning-Photos-with-Generative-AI.git
cd Captioning-Photos-with-Generative-AI
```

**2. Create and Activate a Virtual Environment**
It is highly recommended to use a virtual environment to manage project dependencies.

```bash
# Create the environment
python -m venv .venv

# Activate the environment
# On Windows (Git Bash):
source .venv/Scripts/activate
# On Windows (Command Prompt or PowerShell):
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

**3. Install Dependencies**
This project's dependencies are listed in `requirements.txt`. Install them with pip:
```bash
pip install -r requirements.txt
```

---

### Running the Tools

Once the initial setup is complete, you can run any of the three tools.

**A. Running the Interactive Web App**
```bash
python app.py
```
Open your web browser and navigate to the local URL provided in the terminal, usually `http://127.0.0.1:7860`.

**B. Running the Automated URL Captioner**
```bash
python automate_url_captioner.py
```
The script will scrape the default URL (Wikipedia's IBM page) and create a file named `captions.txt` with the results.

**C. Running the Local Batch Captioner**
1.  Create a folder named `images` in the main project directory.
2.  Place your `.jpg`, `.jpeg`, or `.png` files inside the `images` folder.
3.  Run the script:
```bash
python caption_local_files.py
```
The script will create a file named `local_captions.txt` with the filenames and their captions.

---

## Project Journey: Challenges & Key Learnings

This project was a fantastic learning experience that went beyond simply writing AI code. The journey involved significant learning in environment setup, dependency management, and debugging—skills that are critical for any real-world software project.

### Challenges Faced

*   **Environment Management:** Initially encountered `ModuleNotFoundError` because packages were installed in the global Python environment instead of the project's virtual environment (`.venv`). This emphasized the critical importance of activating the `.venv` *before* installing any packages.

*   **Operating System Constraints:** The installation of `torch` and its dependencies failed due to the "Windows Long Path" error. Because I did not have administrator privileges to change the system setting, the solution was to restructure the project into a much shorter file path (`C:\Users\ThapeloMasebe\code\ai-caption-app`), which immediately resolved the `OSError`.

*   **Dependency Specifics:** Discovered that installing `torch` does not automatically install `torchvision`, and that the correct package for BeautifulSoup is `beautifulsoup4`. This reinforced the need for careful dependency management.

### Key Learnings

*   **Model Integration:** Gained hands-on experience using the Hugging Face `transformers` library to download and run powerful, pre-trained vision models like BLIP, BLIP-2, and ResNet.

*   **Building Interactive UIs:** Learned to use the Gradio library to rapidly build and launch a clean, user-friendly web interface. I successfully implemented a `TabbedInterface` to house multiple AI functionalities within a single application.

*   **DevOps Best Practices:** This project was a practical lesson in essential developer operations:
    *   **Version Control:** Using `git` and GitHub to track changes and build a project portfolio.
    *   **Environment Isolation:** The absolute necessity of using virtual environments (`.venv`).
    *   **Dependency Management:** Creating and using a `requirements.txt` file to ensure the project is easily reproducible.

*   **Systematic Problem-Solving:** The series of errors provided a crash course in debugging—reading tracebacks carefully, identifying the root cause, and applying a targeted solution.

## Future Improvements

This project serves as a strong foundation. Potential future enhancements include:

*   **Command-Line Arguments:** Allow users to pass a URL or local directory path as an argument to the scripts instead of editing the code.
*   **Deployment:** Containerize the application with a `Dockerfile` and deploy it to a cloud service like Hugging Face Spaces or AWS.
*   **Combine Scripts:** Merge the two command-line tools into a single script with arguments to choose the mode (e.g., `python captioner.py --url <URL>` or `python captioner.py --local <folder>`).

## License

This project is licensed under the MIT License. You can view the license [here](LICENSE).

## Acknowledgments

*   This project was completed as part of the **Building Generative AI-Powered Applications with Python** course offered by **IBM** on the **Coursera** platform.