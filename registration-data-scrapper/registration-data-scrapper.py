# === IMPORTS ===

# Standard library imports
from pathlib import Path

# Third party imports
import requests
from bs4 import BeautifulSoup # Requires the lxml parser

# === FUNCTION DEFINITIONS ===

def write_data(file, *args):
    """
    Joins lists provided in *args (should be same length) with a tab and writes to file
    """
    # Combine items in args element-wise with zip
    # Convert resulting tuple to list
    # Join with atab character
    rows = ['\t'.join(list(item)) for item in zip(*args)]

    for row in rows:
        file.write('{}\n'.format(row))

# ============================

# Base directory of the script file
basedir = Path(__file__).parent.resolve()
calendar_data = basedir / 'Academic Calendar Raw Data 2014-2020.txt'

with open(calendar_data, 'a') as txt_file:

    years = ['35', '36', '37']  # 35 is 2017-2018 and so on

    # Loop through each year
    for year in years:
        # ?acfy=<year code> changes in the URL
        my_url = 'http://registrar.columbia.edu/calendar?acfy={}&acterm=All&acschool=11&keys=&field_event_type1_tid%5B%5D=21'\
                 .format(year)

        # Download the URL and convert into soup
        res = requests.get(my_url)
        res.raise_for_status()
        url_soup = BeautifulSoup(res.text, 'lxml')

        # Find dates and event titles based on corresponding classes
        dates = url_soup.find_all('div', 'field-type-datestamp')
        titles = url_soup.find_all('div', 'field-name-event-title')

        # Extract text into a list
        dates_text = [item.get_text() for item in dates]
        titles_text = [item.get_text(strip=True) for item in titles]

        write_data(txt_file, dates_text, titles_text)
