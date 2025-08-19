# AI VectorGen Studio

AI VectorGen Studio is a desktop application that generates high-quality, editable vector graphics (SVG) from text descriptions (prompts). It lowers the initial barrier to creation by transforming ideas into vector assets that can be immediately integrated into a design workflow.

## Features

- **Text-to-Vector Conversion**: Describe the image you want with text and generate a vector graphic.
- **Simple GUI**: An intuitive interface makes it easy to generate and save vector files.
- **Robust Conversion**: Uses the `Pillow` library to normalize images, ensuring stable vectorization across different formats.
- **macOS Application Support**: Can be bundled into a native macOS Application (`.app`) with a custom Dock icon using `py2app`.

## Technology Stack

- **Language**: Python 3.9+
- **GUI Framework**: PyQt5
- **Image Generation**: Together AI API (`together`)
- **Vector Conversion**: `vtracer`
- **Image Processing**: `Pillow`
- **macOS App Bundling**: `py2app`

---

## How to Use

You can run this project in two ways.

### Option 1: Run as a Python Script (Simple)

This method runs the application directly from the terminal.

**1. Prerequisites**

- **Get a Together AI API Key**: You need an API key from [Together.ai](https://www.together.ai/) to enable image generation.
- **Clone the Repository**: Download the project files to your local machine.

**2. Setup**

1.  **Set API Key**: Create a file named `.env` in the project root and place your API key in it as follows:
    ```
    TOGETHER_API_KEY="your_together_api_key_here"
    ```
2.  **(Optional) Set Window Icon**: Place your desired icon file named `icon.png` in the project root. If found, it will be used as the window icon.

3.  **Install Dependencies**: Open a terminal in the project directory and run:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the App**: Launch the application using the following command:
    ```bash
    python main_app.py
    ```

### Option 2: Build a Native macOS Application (`.app`)

This method packages the project into a standalone macOS application with a proper Dock icon.

**1. Prerequisites**

- Complete all steps (1 & 2) from **Option 1** above.
- **Prepare Dock Icon**: You must have an icon file named `icon.png` in the project root. This will be used as the application and Dock icon.

**2. Build the Application**

1.  **Install Dependencies**: Ensure all libraries, including `py2app`, are installed by running `pip install -r requirements.txt`.
2.  **Run Build Command**: In the terminal, run the following command to start the build process.
    ```bash
    python setup.py py2app -A
    ```
    *(The `-A` or `--alias` flag uses "alias mode," which is a workaround for potential dependency analysis errors during the build process.)*

3.  **Launch the App**: Once the build is complete, you will find **`AIVectorGenStudio.app`** inside the `dist` folder. You can run this file like any other macOS application, and it will appear in the Dock with your custom icon.

---

## On AI Model Fine-Tuning

This application uses a public, pre-trained model provided by Together AI. If you wish to train the AI on your own set of images (.ai, .png, etc.) to generate results in a more personalized style, you would need to perform **fine-tuning**.

- **Feasibility**: While you cannot fine-tune a model directly within this app, the **Together AI platform itself offers fine-tuning as a service**.
- **Process**: This is an advanced workflow that typically involves preparing a dataset of `image-text` pairs, uploading it to the Together AI platform, and initiating a training job via their web interface.
- **Conclusion**: Fine-tuning is a powerful but complex process that requires significant effort in data preparation. If you are interested, we recommend consulting the official Together AI documentation. Once your custom model is trained, you can use it in this app by simply changing the model name in the `image_generator.py` file to your new custom model ID.