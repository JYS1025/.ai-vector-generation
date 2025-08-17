# vectorizer.py
import subprocess
import os

class CommandNotFoundError(Exception):
    "Custom exception for missing command-line tools."
    pass

def check_command_exists(command: str) -> bool:
    """Checks if a command exists on the system PATH."""
    try:
        subprocess.run([command, "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, text=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        try:
            # Fallback for tools that use -version or other syntax
            subprocess.run([command, "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, text=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

def vectorize_image(input_path: str, output_svg_path: str):
    """
    Converts a raster image to a posterized SVG.
    Raises exceptions for errors.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found at '{input_path}'")

    if not check_command_exists("magick"):
        raise CommandNotFoundError("ImageMagick is not installed or not in the system's PATH.")
        
    if not check_command_exists("potrace"):
        raise CommandNotFoundError("Potrace is not installed or not in the system's PATH.")

    base_name = os.path.splitext(input_path)[0]
    temp_bmp = f"{base_name}_posterized.bmp"

    # Step 1: Posterize using ImageMagick
    magick_command = ["magick", input_path, "-posterize", "8", temp_bmp]
    try:
        subprocess.run(magick_command, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        # Clean up before raising
        if os.path.exists(temp_bmp):
            os.remove(temp_bmp)
        raise Exception(f"Error during ImageMagick processing: {e.stderr}")

    # Step 2: Vectorize using Potrace
    potrace_command = ["potrace", temp_bmp, "--svg", "-o", output_svg_path]
    try:
        subprocess.run(potrace_command, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        raise Exception(f"Error during Potrace processing: {e.stderr}")
    finally:
        # Step 3: Clean up temporary file
        if os.path.exists(temp_bmp):
            os.remove(temp_bmp)
