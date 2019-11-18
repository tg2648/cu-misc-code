"""
Searches Word files with a regex expression
Windows only

Environment variables:
    WORD_FOLDER: path to a folder where the search will start 
    DEST_FOLDER: path to a folder where the output will be saved to
    REGEX: regex expression used in search
"""

# === IMPORTS/CONFIG ===

# Standard library imports
import os
import json
import sys
import re
import csv
from pathlib import Path

# Third party imports
from dotenv import load_dotenv
import win32com.client

# Local application imports
sys.path.append(str(Path(__file__).parent.parent.resolve())) # Add parent directory to sys.path to import utils.py
from utils import progress_bar

# Base directory of the script file
basedir = Path(__file__).parent.resolve()

# Load environment variables
env_path = basedir / '.env'
load_dotenv(dotenv_path=env_path)

# ======================

word = win32com.client.Dispatch("Word.Application")
word.visible = False

word_folder = os.getenv('WORD_FOLDER')
regex = re.compile(os.getenv('REGEX'))

word_generator_1 = Path(word_folder).rglob("*.doc") # Use globbing to return a list of Path objects to all .doc files, including from subfolders
word_list = [i for i in word_generator_1]
word_generator_2 = Path(word_folder).rglob("*.docx")
for item in word_generator_2:
    word_list.append(item)
word_matches = []

print(word_list)

n = 0
n_max = len(word_list)
print("\nParsing Word: ")

for word_path in word_list:

    doc = word.Documents.Open(str(word_path))
    doc_text = doc.Range().Text

    doc_text_match = regex.findall(doc_text) # List of tuples

    if doc_text_match:
        to_insert = [word_path.stem]
        doc_text_match = [list(filter(None, i)) for i in doc_text_match] # Clean up tuple to remove empty strings and convert to list
        # Concatenate lists:
        for group in doc_text_match:
            to_insert.append(group)
        word_matches.append(to_insert)

    doc.Close(False) # Close without saving
    progress_bar(n, n_max)
    n = n + 1


dest_folder = os.getenv('DEST_FOLDER')
dest_file = Path(dest_folder) / 'output_word.csv'

with open(dest_file, 'w+', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(word_matches)

print("\nDone!")