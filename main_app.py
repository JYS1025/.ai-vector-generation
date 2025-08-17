# main_app.py
import sys
import os
import uuid
import shutil
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QLabel, QLineEdit, QPushButton, QStatusBar, QMessageBox, QFileDialog
)
from PyQt5.QtCore import QThread, pyqtSignal

# Import refactored logic
from image_generator import generate_image_api, ApiTokenError
from vectorizer import vectorize_image, CommandNotFoundError

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
            # Create unique filenames for this run
            run_id = str(uuid.uuid4())
            temp_png = f"{run_id}.png"
            temp_svg = f"{run_id}.svg"

            # Step 1: Generate Image
            self.progress.emit("Generating image via API...")
            generate_image_api(self.prompt, temp_png)

            # Step 2: Vectorize Image
            self.progress.emit("Vectorizing image...")
            vectorize_image(temp_png, temp_svg)

            # Step 3: Clean up the temp PNG
            if os.path.exists(temp_png):
                os.remove(temp_png)

            self.finished.emit(temp_svg)

        except (ApiTokenError, CommandNotFoundError, FileNotFoundError) as e:
            self.error.emit(str(e))
        except Exception as e:
            self.error.emit(f"An unexpected error occurred: {e}")

class AIVectorGenStudio(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI VectorGen Studio")
        self.setGeometry(200, 200, 500, 150)

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

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getSaveFileName(self, "Save SVG File", "", "SVG Files (*.svg);;All Files (*)", options=options)

        if file_path:
            try:
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
