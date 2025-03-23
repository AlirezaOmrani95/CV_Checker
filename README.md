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
   ```bash
   git clone https://github.com/AlirezaOmrani95/CV_Checker.git
   cd CV_Checker

3. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt


## Usage
### Running the Script
Once everything is set up, you can run the script to compare a CV against a job description.

### Command-line Arguments
--cv: Path to the CV file (can be a URL or local file). Accepts PDF, DOC/DOCX, XLS/XLSX, PPT/PPTX, and HWP/HWPX formats.

--learn_mode: Choose between zero-shot or one-shot learning modes.

--model_type: Select the model to use. For example, `google/gemma-3-27b-it:free` or any other model listed in the free_model_names.txt file.

### Example Command
   ```bash
   python CV_checker.py --cv cv.pdf --learn_mode one-shot --model_type google/gemma-3-27b-it:free

