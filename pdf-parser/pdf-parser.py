"""
Searches PDF files with a regex expression.
Requires Poppler for pdf2image.
Requires tesseract for pytesseract.

Environment variables:
    IMG_FOLDER
    TXT_FOLDER
    PDF_FOLDER
    DEST_FOLDER
    REGEX

TODO: Make more modular
"""

# === IMPORTS/CONFIG ===

# Standard library imports
import os
import sys
import re

# Third party imports
from dotenv import load_dotenv
from pathlib import Path
from PIL import Image
import pytesseract
from pdf2image import convert_from_path

# Local application imports
sys.path.append(str(Path(__file__).parent.parent.resolve())) # Add parent directory to sys.path to import utils.py
from utils import progress_bar

# Base directory of the script file
basedir = Path(__file__).parent.resolve()

# Load environment variables
env_path = basedir / '.env'
load_dotenv(dotenv_path=env_path)

# ======================

###
# Convert PDF to images
###

# Path of the pdf 
pdf_folder = os.getenv('PDF_FOLDER')
pdf_generator = Path(pdf_folder).rglob("*.pdf") # Use globbing to return a list of Path objects to all .pdf files, including from subfolders
pdf_list = [i for i in pdf_generator]

img_folder = os.getenv('IMG_FOLDER')

n = 0
n_max = len(pdf_list)
print("\nConverting PDFs: ")

for pdf_path in pdf_list:

    try:
        pages = convert_from_path(str(pdf_path), 500) # Store all the pages of the PDF in a variable 
    except:
        print(f"\nFailed PDF conversion: {str(pdf_path)}")
    
    image_counter = 1 # Counter to store images of each page of PDF to image 
    # Iterate through all the pages stored above 
    for page in pages:
    
        img_filename = img_folder + Path(pdf_path).stem + "_page_"+str(image_counter)+".jpg" # Build filename for each page of PDF as JPG 
        try:
            page.save(img_filename, 'JPEG') # Save the image of the page in system 
        except:
            print(f"\nFailed image saving: {str(pdf_path)}")
        image_counter = image_counter + 1
    
    progress_bar(n, n_max)
    n = n + 1


###
# Extract text from images
###

txt_folder = os.getenv('TXT_FOLDER')
img_generator = Path(img_folder).rglob("*.jpg") # Use globbing to return a list of Path objects to all .jpg files, including from subfolders
img_list = [i for i in img_generator]

n = 0
n_max = len(list(img_list))
print("\nExtracting text: ")

for img_path in img_list:

    txt_filename = img_path.stem + '.txt'
    txt_path = os.path.join(txt_folder,txt_filename)

    with open(txt_path, "a") as f:
        try:
            img_text = str(pytesseract.image_to_string(Image.open(str(img_path))))
        except:
            print(f"Failed OCR: {str(img_path)}")
        f.write(img_text)

    progress_bar(n, n_max)
    n = n + 1

###
# Search through extracted text
###

regex = re.compile(os.getenv('REGEX'))

txt_generator = Path(txt_folder).rglob("*.txt")
txt_list = [i for i in txt_generator]
txt_matches = [] # list of text files with matching text

n = 0
n_max = len(list(txt_list))
print("\nSearching for regex: ")

for txt_path in txt_list:
    with open(str(txt_path), 'r') as f:
        txt_text = f.read()
        txt_text_match = regex.search(txt_text)

        if txt_text_match is not None:
            txt_matches.append(txt_path.stem)

    progress_bar(n, n_max)
    n = n + 1

###
# Write filenames with matching text to a file
###

dest_folder = os.getenv('DEST_FOLDER')
dest_file = Path(dest_folder) / 'output.txt'

with open(dest_file, 'w') as f:
    for item in txt_matches:
        f.write(f"{item}/n")

print("\nDone!")