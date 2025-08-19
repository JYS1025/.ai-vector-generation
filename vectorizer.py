# vectorizer.py
import vtracer
import os
import io
from PIL import Image

class VectorizationError(Exception):
    "Custom exception for vectorization errors."
    pass

def vectorize_image(input_path: str, output_svg_path: str):
    """
    Converts a raster image to an SVG. It normalizes the image with Pillow
    before passing its data to vtracer to handle potential format issues.
    """
    try:
        # 1. Read the raw image file into memory.
        with open(input_path, 'rb') as f:
            image_bytes = f.read()

        if not image_bytes:
            raise VectorizationError("Input image file is empty.")

        # 2. Normalize the image using Pillow to resolve format/encoding issues.
        # Open the image from the raw bytes.
        img_buffer_in = io.BytesIO(image_bytes)
        img = Image.open(img_buffer_in)

        # Save the image back to a new in-memory buffer in a standard PNG format.
        img_buffer_out = io.BytesIO()
        img.save(img_buffer_out, format="PNG")
        normalized_image_bytes = img_buffer_out.getvalue()

        # 3. Convert the normalized image bytes to an SVG string using vtracer.
        svg_string = vtracer.convert_raw_image_to_svg(normalized_image_bytes, img_format='png')

        # 4. Write the resulting SVG string to the output file.
        with open(output_svg_path, 'w') as f:
            f.write(svg_string)

    except FileNotFoundError:
        # Re-raise the specific error if the input file is not found.
        raise FileNotFoundError(f"Input file not found at '{input_path}'")
    except Exception as e:
        # Wrap other exceptions in our custom error type.
        raise VectorizationError(f"Error during vtracer processing: {e}")