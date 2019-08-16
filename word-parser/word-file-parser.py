"""
Searches Word files with a regex expression
Windows only

Environment variables:
    FOLDER: path to a folder where the search will start 
    REGEX: regex expression used in search
"""

# === IMPORTS/CONFIG ===

# Standard library imports
import os
import json
import sys
import re

# Third party imports
from dotenv import load_dotenv
from pathlib import Path
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

doc = word.Documents.Open(os.getenv('FOLDER'))
doc_text = doc.Range().Text

regex = re.compile(os.getenv('REGEX'))
doc_text_match = regex.search(doc_text)

if doc_text_match is None:
    print("No match found")
else:
    print("Match found")

doc.Close(False) # Close without saving