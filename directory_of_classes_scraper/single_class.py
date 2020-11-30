"""
Scrape a single class
"""

from doc_scraper import DirectoryClass

url = "http://www.columbia.edu/cu/bulletin/uwb/subj/EESC/V2310-20211-001/"
class_info = DirectoryClass(url=url)

print(class_info.data)
