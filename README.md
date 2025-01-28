Automatic Number Plate Recognition (ANPR)

Project Overview

This repository contains an Automatic Number Plate Recognition (ANPR) system, designed to detect and extract license plate information from images or video feeds. The system uses computer vision and optical character recognition (OCR) techniques to accurately identify and process license plate numbers.

Features

License Plate Detection: Detects license plates in images or video frames.

OCR Integration: Extracts alphanumeric characters from detected license plates.

High Accuracy: Utilizes advanced deep learning models for accurate recognition.

Flexible Input Formats: Supports multiple formats including images (JPEG, PNG) and video streams.

Scalable: Can be easily integrated with real-time systems such as surveillance cameras.

Tech Stack

Programming Language: Python

Libraries/Frameworks:

OpenCV (for image processing)

TensorFlow/Keras or PyTorch (for model training and inference)

Tesseract OCR (for character recognition)

NumPy & Pandas (for data handling)

Environment: Jupyter Notebook (for experimentation)

Installation

Clone the repository:

git clone https://github.com/shleshitha/ANPR.git
cd anpr-project

Create a virtual environment and activate it:

python -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate   # For Windows

Install the required dependencies:

pip install -r requirements.txt

Download pre-trained models:

Ensure to place the pre-trained detection and OCR models in the models/ directory.

Update the config.json file to include the correct paths.

Usage

Run the System:
For image-based recognition:

python anpr.py --image <path-to-image>

For video-based recognition:

python anpr.py --video <path-to-video>

Outputs:

Detected license plates are saved in the outputs/ directory.

Extracted license plate numbers are displayed in the console and saved as a text file.

File Structure

ANPR-Project/
|-- models/              # Pre-trained models
|-- datasets/            # Sample images and videos
|-- outputs/             # Processed outputs
|-- anpr.py              # Main application script
|-- requirements.txt     # Dependency file
|-- README.md            # Project documentation
|-- config.json          # Configuration file

Contributing

Contributions are welcome! To contribute:

Fork the repository.

Create a feature branch:

git checkout -b feature-name

Commit your changes and push the branch:

git commit -m "Add feature-name"
git push origin feature-name

Create a pull request.

License

This project is licensed under the MIT License.

Acknowledgements

OpenCV for robust image processing.

Tesseract OCR for reliable character recognition.

TensorFlow/Keras and PyTorch for deep learning support.


