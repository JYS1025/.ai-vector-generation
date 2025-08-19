# main_app.py
import sys
import os
import uuid
import shutil
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QLabel, QLineEdit, QPushButton, QStatusBar, QMessageBox, QFileDialog
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QThread, pyqtSignal

# Import refactored logic
from image_generator import generate_image_api, ApiTokenError
from vectorizer import vectorize_image, VectorizationError

class GenerationWorker(QThread):
    """Runs the image generation and vectorization in a separate thread."""
    progress = pyqtSignal(str)
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, prompt):
        super().__init__()
        self.prompt = prompt

    def run(self):
        try:
            # Get the absolute path for the current directory to resolve paths correctly.
            work_dir = os.path.abspath(os.getcwd())
            
            # Create unique absolute filenames for this run
            run_id = str(uuid.uuid4())
            temp_png = os.path.join(work_dir, f"{run_id}.png")
            temp_svg = os.path.join(work_dir, f"{run_id}.svg")

            # Step 1: Generate Image from API
            self.progress.emit("1/3: Generating image from AI (can take up to a minute)...")
            generate_image_api(self.prompt, temp_png)

            # Step 2: Vectorize the generated image
            self.progress.emit("2/3: Vectorizing image...")
            vectorize_image(temp_png, temp_svg)

            # Step 3: Process is complete
            self.progress.emit("3/3: Finalizing...")
            self.finished.emit(temp_svg)

        except (ApiTokenError, VectorizationError, FileNotFoundError) as e:
            self.error.emit(str(e))
        except Exception as e:
            self.error.emit(f"An unexpected error occurred: {e}")
        finally:
            # Final cleanup: ensure the temporary PNG is removed even if errors occur after its creation.
            if os.path.exists(temp_png):
                os.remove(temp_png)

class AIVectorGenStudio(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI VectorGen Studio")
        self.setGeometry(200, 200, 500, 150)

        # --- Set App Icon ---
        # Build an absolute path to the icon file relative to the script's location
        script_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(script_dir, "icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        # --- UI Elements ---
        self.prompt_label = QLabel("Enter your prompt:")
        self.prompt_input = QLineEdit("A vibrant logo for a tech startup called 'SynthWave'")
        self.generate_button = QPushButton("Generate Vector")
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # --- Layout ---
        layout = QVBoxLayout()
        layout.addWidget(self.prompt_label)
        layout.addWidget(self.prompt_input)
        layout.addWidget(self.generate_button)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # --- Connections ---
        self.generate_button.clicked.connect(self.start_generation)
        self.worker = None

    def start_generation(self):
        prompt = self.prompt_input.text()
        if not prompt:
            self.show_error("Prompt cannot be empty.")
            return

        self.generate_button.setEnabled(False)
        self.status_bar.showMessage("Starting generation...")

        self.worker = GenerationWorker(prompt)
        self.worker.progress.connect(self.status_bar.showMessage)
        self.worker.finished.connect(self.generation_finished)
        self.worker.error.connect(self.generation_error)
        self.worker.start()

    def generation_finished(self, temp_svg_path):
        self.status_bar.showMessage("Generation complete! Please save your file.")
        self.generate_button.setEnabled(True)
        self.save_file_dialog(temp_svg_path)

    def generation_error(self, error_message):
        self.show_error(error_message)
        self.status_bar.showMessage("Error occurred.", 5000)
        self.generate_button.setEnabled(True)

    def save_file_dialog(self, temp_svg_path):
        if not os.path.exists(temp_svg_path):
            self.show_error(f"Could not find the generated file: {temp_svg_path}")
            return

        dialog = QFileDialog(self, "Save SVG File", "untitled.svg")
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        dialog.setNameFilters(["SVG Files (*.svg)"])
        dialog.setDefaultSuffix("svg")

        if dialog.exec_() == QFileDialog.Accepted:
            file_path = dialog.selectedFiles()[0]
            try:
                # The content is SVG, but we are saving with the user's chosen extension (.ai or .svg)
                shutil.move(temp_svg_path, file_path)
                self.status_bar.showMessage(f"File saved to {file_path}", 5000)
            except Exception as e:
                self.show_error(f"Could not save file: {e}")
        else:
            # User cancelled the dialog, clean up the temp file
            os.remove(temp_svg_path)
            self.status_bar.showMessage("Save cancelled. Temporary file removed.", 3000)

    def show_error(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText(message)
        msg_box.setWindowTitle("Error")
        msg_box.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AIVectorGenStudio()
    window.show()
    sys.exit(app.exec_())
