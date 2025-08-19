# image_generator.py
import os
import requests  # Added to download images from a URL
from dotenv import load_dotenv
from together import Together

# Load environment variables from the .env file.
load_dotenv()

# Get the API key from environment variables.
API_KEY = os.getenv("TOGETHER_API_KEY")

class ApiTokenError(Exception):
    "Custom exception raised when the API token is missing."
    pass

def generate_image_api(prompt: str, output_path: str):
    '''
    Generates an image using the Together AI API, then downloads and saves it from the returned URL.
    '''
    if not API_KEY:
        raise ApiTokenError("Together AI API key not found. Please set the TOGETHER_API_KEY in your .env file.")

    try:
        client = Together(api_key=API_KEY, timeout=60.0)
        
        # Call the API according to the official documentation.
        response = client.images.generate(
            model="black-forest-labs/FLUX.1-schnell-Free", # Use a free model
            prompt=prompt,
            steps=4
        )

        # As per the documentation, check the url attribute of the first item in the response object's data list.
        if response.data and response.data[0].url:
            image_url = response.data[0].url
            
            # Download the image data from the returned URL.
            image_response = requests.get(image_url, timeout=30)
            image_response.raise_for_status()  # Raise an exception if an HTTP error occurs.
            
            # Save the downloaded image data to a file.
            with open(output_path, "wb") as f:
                f.write(image_response.content)
        else:
            raise Exception("The API response does not include an image URL.")

    except Exception as e:
        # Handle all errors comprehensively.
        raise Exception(f"An error occurred: {e}")
