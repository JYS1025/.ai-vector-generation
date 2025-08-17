# image_generator.py
import requests
import os
import time
from dotenv import load_dotenv

# .env 파일에서 환경 변수를 로드합니다.
load_dotenv()

API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")

class ApiTokenError(Exception):
    "Custom exception for missing API token."
    pass

def generate_image_api(prompt: str, output_path: str):
    """
    Generates an image using the Hugging Face API and saves it.
    Raises exceptions for errors.
    """
    if not API_TOKEN:
        raise ApiTokenError("Hugging Face API token not found. Please set the HUGGINGFACE_API_TOKEN environment variable.")

    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    payload = {"inputs": prompt}

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 503: # Model is loading
        estimated_time = response.json().get("estimated_time", 20.0)
        # Wait and retry
        time.sleep(estimated_time)
        response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        error_message = f"API Error (Status {response.status_code}): {response.text}"
        raise Exception(error_message)

    with open(output_path, "wb") as f:
        f.write(response.content)
