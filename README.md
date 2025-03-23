# CV Checker

## Overview

This script extracts information from your CV and a specific job and checks how similar your CV is to the job using LLM models.

## Features

- **Zero-shot learning mode**: Uses pre-trained models without the need for additional fine-tuning.
- **One-shot learning mode**: Requires one example for better model performance and to personalize results.
- **Model selection**: Allows users to choose from a list of available free LLM models.
- **Supports multiple file formats**: CVs can be in PDF, DOC/DOCX, XLS/XLSX, PPT/PPTX, and HWP/HWPX formats.

## Installation
1. **Clone the repository**:
   `git clone https://github.com/AlirezaOmrani95/CV_Checker.git
   cd CV_Checker`

2. **Install the dependencies**:
   `pip install -r requirements.txt`

## Usage
### Running the Script
Once everything is set up, you can run the script to compare a CV against a job description.

### Command-line Arguments
--cv: Path to the CV file (can be a URL or local file). Accepts PDF, DOC/DOCX, XLS/XLSX, PPT/PPTX, and HWP/HWPX formats.

--learn_mode: Choose between zero-shot or one-shot learning modes.

--model_type: Select the model to use. For example, `google/gemma-3-27b-it:free` or any other model listed in the free_model_names.txt file.

### Example Command
`python CV_checker.py --cv cv.pdf --learn_mode one-shot --model_type google/gemma-3-27b-it:free`

This command will analyze the CV against the job description using the specified model and learning mode.

## Files in this Repository

- **CV_checker.py**: Main script to compare CVs with job descriptions using LLM models.

- **requirements.txt**: List of required Python packages.

- **examples.json**: Example for one-shot learning.

- **free_model_names.txt**: A list of available free models.

- **README.md**: Documentation for the repository.

## Notes
- To use the script you need an API key, which you can create for free by registering on [openrouter](www.openrouter.ai).
- Make sure your CV file is accessible and in one of the accepted formats.
- The learn_mode option determines whether the model will use zero-shot or one-shot learning. One-shot generally provides better results but requires an example. So, you can change the examples in **examples.json file** based on your field.

## Contact
If you have any questions or suggestions, feel free to open an issue on GitHub or contact me at Omrani.alireza95@gmail.com.

