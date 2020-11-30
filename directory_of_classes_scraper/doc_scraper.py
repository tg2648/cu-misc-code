"""
Directory of Classes parser
TODO: https://stackoverflow.com/questions/8049520/web-scraping-javascript-page-with-python
"""

# Standard library imports
from urllib.parse import urljoin
import re
import csv
import datetime
import pickle

# Third party imports
import requests
from bs4 import BeautifulSoup


NAME_MAPPING = {
    "Accounting (ACCT)": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Accounting (ACNT)": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Actuarial Science": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "African American and African Diaspora": {'Department Code': 'AFAM', 'Division Code': 'SS', 'School': 'A&S'},
    "African Studies, Institute of": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "African-American Studies, Institute for Research in": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Africana Studies (AFRS)": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Africana Studies (AFSB)": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "American Language Program": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "American Studies": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "American Studies @Barnard": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Anatomy & Cell Biology": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Ancient Studies @Barnard": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Anesthesiology": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Anthropology": {'Department Code': 'ANTH', 'Division Code': 'SS', 'School': 'A&S'},
    "Anthropology @Barnard": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Anthropology @NYU": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Applied Analytics": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Applied Physics and Applied Mathematics": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Architecture @Barnard": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Architecture, Planning and Preservation": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Art History @Barnard": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Art History and Archaeology": {'Department Code': 'AHAR', 'Division Code': 'HUM', 'School': 'A&S'},
    "Arts, Program @Barnard": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Arts, School of the": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Asian American Studies": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Asian and Middle East @Barnard": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Astronomy": {'Department Code': 'ASTR', 'Division Code': 'NS', 'School': 'A&S'},
    "Astronomy and Physics @Barnard": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Athena Center for Leadership Studies @Barnard": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Auditing": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Barnard College": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Biochemistry and Molecular Biophysics": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Bioethics": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Biological Sciences": {'Department Code': 'BIOL', 'Division Code': 'NS', 'School': 'A&S'},
    "Biological Sciences @Barnard": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Biomedical Engineering": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Biomedical Informatics": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Biostatistics": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Business": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Business Economics": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Business School - Core": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Cellular, Molecular, and Biophysical Studies": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Centennial Scholars @Barnard": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Center for Innovative Theory and Empirics": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Chemical Engineering": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Chemistry": {'Department Code': 'CHEM', 'Division Code': 'NS', 'School': 'A&S'},
    "Chemistry @Barnard": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Civil Engineering and Engineering Mechanics": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Classics": {'Department Code': 'CLAS', 'Division Code': 'HUM', 'School': 'A&S'},
    "Classics @Barnard": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Columbia College": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Committee on Global Thought": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Comparative Literature and Society @Barnard": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Comparative Literature and Society, Institute for": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Computer Science": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Computer Science @Barnard": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Computing Systems (Professional Studies)": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Consortium for Critical Interdisciplinary Studies @Barnard": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Construction Administration": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Contemporary Civilization and Literature Humanities": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Core (A&S)": {'Department Code': 'CORE', 'Division Code': 'CORE', 'School': 'A&S'},
    "Dance @Barnard": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Data Science Institute": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Decision, Risk and Operations": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Dental and Oral Surgery": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Dermatology": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Drama and Theatre Arts": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Earth and Environmental Engineering": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Earth and Environmental Sciences": {'Department Code': 'DEES', 'Division Code': 'NS', 'School': 'A&S'},
    "Earth Institute": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "East Asian Languages and Cultures": {'Department Code': 'EALC', 'Division Code': 'HUM', 'School': 'A&S'},
    "East Asian Regional Studies": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Ecology, Evolution, and Environmental Biology": {'Department Code': 'EEEB', 'Division Code': 'NS', 'School': 'A&S'},
    "Economics": {'Department Code': 'ECON', 'Division Code': 'SS', 'School': 'A&S'},
    "Economics @Barnard": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Education @Barnard": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Electrical Engineering": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Emergency Medicine": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Engineering": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "English @Barnard": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "English and Comparative Literature": {'Department Code': 'ENCL', 'Division Code': 'HUM', 'School': 'A&S'},
    "Enterprise Risk Management": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Environmental Health Sciences": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Environmental Sciences @Barnard": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Epidemiology": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Epidemiology: Exec Master Program": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Ethnicity and Race, Center for": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Executive Classes in HPM": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Executive Masters in Public Health": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Film": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Film @Barnard": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Finance": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Finance and Economics": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "First-Year Seminar Program @Barnard": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "First-Year Writing @Barnard": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "French": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "French @Barnard": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "French and Romance Philology": {'Department Code': 'FRRP', 'Division Code': 'HUM', 'School': 'A&S'},
    "General Public Health": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "General Studies": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Genetic Counseling": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Genetics and Development": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "German @Barnard": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Germanic Languages": {'Department Code': 'GERL', 'Division Code': 'HUM', 'School': 'A&S'},
    "Global Health Track": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Global Programs": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Graduate School of Arts and Sciences": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Health Policy & Management": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "History": {'Department Code': 'HIST', 'Division Code': 'SS', 'School': 'A&S'},
    "History @Barnard": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "History @NYU": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Hughes Science Pipeline Project": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Human Capital Management": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Human Nutrition, Institute of": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Human Rights (HRTB)": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Human Rights (ICHR)": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Humanities (College)": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Industrial Engineering and Operations Research": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Information & Knowledge Strat": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Institute for Israel & Jewish Studies": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Institute for Social & Economics Research and Policy": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Institute for Study of Human Rights": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Insurance Management": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Interdepartmental (Engineering)": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "International and Public Affairs": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Italian": {'Department Code': 'ITAL', 'Division Code': 'HUM', 'School': 'A&S'},
    "Italian @Barnard": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Jazz Studies, Center for": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Jewish Theological Seminary": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Journalism": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Juilliard": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Language Resource Center": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Latin American and Iberian Cultures": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Latin-American & Carib RS": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Latino Studies": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Law": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Management": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Management Science": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Marketing": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Mathematics": {'Department Code': 'MATH', 'Division Code': 'NS', 'School': 'A&S'},
    "Mathematics @Barnard": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Mechanical Engineering": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Medicine": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Medieval and Renaissance Studies": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Medieval and Renaissance Studies @Barnard": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Microbiology": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Middle Eastern, South Asian and African Studies": {'Department Code': 'MESA', 'Division Code': 'HUM', 'School': 'A&S'},
    "Modern European Studies": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Music": {'Department Code': 'MUSI', 'Division Code': 'HUM', 'School': 'A&S'},
    "Music @Barnard": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Narrative Medicine": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Negotiation & Conflict Resolution": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Neurobiology and Behavior": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Neurological Surgery (NEUS)": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Neurology": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Neuroscience & Behavior @Barnard": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Neurosurgery (NUSR)": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "New School of Social Research": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Non Profit Management": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Nursing": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Obstetrics and Gynecology": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "OFFC OF THE REGISTRAR": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Ophthalmology": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Oral History": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Orthopedic Surgery": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Otolaryngology / Head and Neck Surgery": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Pathology": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Pediatrics": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Pharmacology": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Philosophy": {'Department Code': 'PHIL', 'Division Code': 'HUM', 'School': 'A&S'},
    "Philosophy @Barnard": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Physical Education": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Physical Education @Barnard": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Physical Therapy": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Physicians & Surgeons: Medicine": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Physics": {'Department Code': 'PHYS', 'Division Code': 'NS', 'School': 'A&S'},
    "Physics and Astronomy @Barnard": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Physiology & Cellular Biophysics": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Political Science": {'Department Code': 'POLS', 'Division Code': 'SS', 'School': 'A&S'},
    "Political Science @Barnard": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Population and Family Health": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Pre-College Program (Barnard)": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Professional Studies": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Professional Studies & Special Pgrms: Department of Global Programs": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Psychiatry": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Psychoanalytic Center": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Psychology": {'Department Code': 'PSYC', 'Division Code': 'NS', 'School': 'A&S'},
    "Psychology @Barnard": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Public Health": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Public Health Information Technology": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Quantitative Methods/Social Sciences": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Radiology": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Rehabilitation Medicine (RMED)": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Reid Hall Paris Programs": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Religion": {'Department Code': 'RELI', 'Division Code': 'HUM', 'School': 'A&S'},
    "Religion @Barnard": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Scholars of Distinction @Barnard": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "School of Professional Studies (DVSP)": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "School of Professional Studies (SCEN)": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "School of Professional Studies (SPEC)": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "School of Professional Studies (SPS)": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Science and Public Policy @Barnard": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Slavic Languages": {'Department Code': 'SLAL', 'Division Code': 'HUM', 'School': 'A&S'},
    "Slavic Languages @Barnard": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Social Work": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Sociology": {'Department Code': 'SOCI', 'Division Code': 'SS', 'School': 'A&S'},
    "Sociology @Barnard": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Sociology @NYU": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Sociomedical Sciences": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Spanish and Latin American Culture": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Sports Management": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Statistics": {'Department Code': 'STAT', 'Division Code': 'NS', 'School': 'A&S'},
    "Statistics (MATS)": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Strategic Communication": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Summer High School Program": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Summer Session (SS)": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Summer Session (SUMM)": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Surgery": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Sustainability Management": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Sustainability Technology": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Systems Biology": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Technology Management": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "TEST DIVISION": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Thanatology": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Theatre @Barnard": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Theatre Arts": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Undergraduate Writing Program": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Union Theological Seminary (UTFE)": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Union Theological Seminary (UTSD)": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Urban Studies": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Urban Studies (URBS)": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Urban Studies @Barnard": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Urology": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Video Network": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Visual Arts": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Wealth Management": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Women's and Gender Studies": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Women's, Gender, Sexuality Studies @Barnard": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
    "Writing": {'Department Code': 'Other', 'Division Code': 'Other', 'School': 'Other'},
}


def get_soup_from_url(url):
    res = requests.get(url)
    res.raise_for_status()
    return BeautifulSoup(res.text, 'lxml')


class DirectoryClass(object):
    """
    Wrapper for class information in the directory of classes.
    Class information is organized in a table:

    ------------|------------------
    Call Number	| 12520
    ------------|------------------
    Day & Time  | TR 6:10pm-7:25pm
    Location    | ONLINE ONLY
    ----------- | -----------------

    Goes row-by-row and extracts data.
    The text of the first column is mapped to a function that will extract the data.

    Attributes:
        url (str): URL to class page in the DoC
        data (dict): Information about the class obtained from the DoC
    """

    def __init__(self, url) -> None:
        self.url = url
        self.data = {}

        handlers = {
            'Day & Time Location': self._get_dtl,
            'Instructor': self._get_instructor,
            'Instructors': self._get_mult_instructors,
            'Web Site': self._get_website,
            'Enrollment': self._get_enrl,

            'Call Number': self._get_generic,
            'Points': self._get_generic,
            'Grading Mode': self._get_generic,
            'Approvals Required': self._get_generic,
            'Type': self._get_generic,
            'Method of Instruction': self._get_generic,
            'Course Description': self._get_generic,
            'Department': self._get_generic,
            'Subject': self._get_generic,
            'Number': self._get_generic,
            'Section': self._get_generic,
            'Division': self._get_generic,
            'Open To': self._get_generic,
            'Campus': self._get_generic,
            'Note': self._get_generic,
            'Section key': self._get_generic,
        }

        soup = get_soup_from_url(url=url)
        rows = soup.find_all('tr')

        # Class name is not in the two-column format like the rest
        self._get_class_name(rows[1])

        for row in rows[2:-1]:
            key = row.contents[0].get_text(" ", strip=True)
            func = handlers.get(key, None)
            if func:
                func(row)

        # Extract term from section key
        if self.data.get('Section key', None):
            self.data['Term'] = self.data.get('Section key')[:5]
        else:
            self.data['Term'] = 'n/a'

        self.data['URL'] = self.url

        dept_name = self.data.get('Department', '')
        self.data['Department Code'] = NAME_MAPPING.get(dept_name, {}).get('Department Code', '')
        self.data['Division Code'] = NAME_MAPPING.get(dept_name, {}).get('Division Code', '')

        self.fieldnames = set(self.data.keys())

    def _get_generic(self, row):
        key = row.contents[0].string.strip()
        try:
            val = row.contents[2].string.strip()
            self.data[key] = val
        except Exception:
            self.data[key] = ''

    def _get_class_name(self, row):
        try:
            td = row.contents[1]
            b = td.contents[0]
        except Exception:
            print(f'ERROR: Course/class name formatting issue in {self.url}')
        else:
            try:
                course_name = b.contents[5].string.strip()
            except Exception:
                print(f'ERROR: Failed to get course name from {self.url}')
                course_name = ''
            finally:
                self.data['Course Name'] = course_name

            try:
                class_name = b.contents[8].string.strip()
            except Exception:
                print(f'ERROR: Failed to get class name from {self.url}')
                class_name = ''
            finally:
                self.data['Class Name'] = class_name

    def _get_dtl(self, row):
        """
        Gets day, time, and location.
        Looks like <td>TR 6:10pm-7:25pm<br/>ONLINE ONLY</td>
        The <br> tag is in position 1 in <td>'s contents
        """
        second_col = row.contents[2]

        try:
            day_time = second_col.contents[0]
            location = second_col.contents[2]
        except Exception:
            print(f'ERROR: Day & Time Location formatting issue in {self.url}')
        else:

            try:
                days, time = day_time.split(' ')  # Separate days and time in TR 6:10pm-7:25pm
                time_begin, time_end = time.split('-')  # Separate begin and end in 6:10pm-7:25pm
            except Exception:
                print(f'ERROR: Failed to get day/time from {self.url}')
                days = time = time_begin = time_end = ''
            finally:
                self.data['Days'] = days
                self.data['Time Begin'] = time_begin
                self.data['Time End'] = time_end

            try:
                regex_result = re.search(r'(.*?) (?<= )(.*)', location)
                room = regex_result.group(1)  # Anything before the first space
                building = regex_result.group(2)  # Anything after the first space
            except Exception:
                print(f'ERROR: Failed to get location from {self.url}')
                room = building = ''
            finally:
                self.data['Room'] = room
                self.data['Building'] = building

    def _get_mult_instructors(self, row):
        """
        Gets all instructor names for classes with multiple instructors.
        """
        instructors = []
        try:
            strings = row.contents[2].strings
            for str in strings:
                instructor = str.strip()
                if instructor:
                    instructors.append(instructor)
        except Exception:
            print(f'ERROR: Failed to get multiple instructors from {self.url}')
            instructors = ['']
        finally:
            for i, instructor in enumerate(instructors):
                self.data[f'Instructor_{i + 1}'] = instructor

    def _get_instructor(self, row):
        """
        Gets instructor's name. Some classes include instructor's website and/or email.
        In that case, the name will be in position zero.
        """
        try:
            second_col = row.contents[2]

            if len(second_col.contents) > 1:
                instructor = second_col.contents[0].strip()
            else:
                instructor = second_col.string.strip()
        except Exception:
            print(f'ERROR: Failed to get instructor from {self.url}')
            instructor = ''
        finally:
            self.data['Instructor_1'] = instructor

    def _get_website(self, row):
        try:
            second_col = row.contents[2]
            link = second_col.contents[0]['href']
        except Exception:
            print(f'ERROR: Failed to get website from {self.url}')
            link = ''
        finally:
            self.data['Website'] = link

    def _get_enrl(self, row):
        """
        Extract enrollment numbers from string formatted as:
            24 students (25 max) as of 11:03AM Thursday, November 12, 2020
        """
        raw_val = row.contents[2].string.strip()

        enrl_max = re.search(r'([0-9]*)(?= student)', raw_val)
        enrl = re.search(r'(?<=\()([0-9]*)(?= max)', raw_val)

        if enrl_max:
            self.data['Enrollment Max'] = enrl_max.group(0)
        else:
            self.data['Enrollment Max'] = ''

        if enrl:
            self.data['Enrollment'] = enrl.group(0)
        else:
            self.data['Enrollment'] = ''


if __name__ == "__main__":

    BASE = 'http://www.columbia.edu'
    DIRECTORY = '/cu/bulletin/uwb/sel/departments.html'
    DEPARTMENT_ROW_START = 3  # Where list of depts starts
    SKIP_NON_AS = 1  # Whether to skip non-A&S depts

    # Keep track of CSV column headers
    fieldnames = set()

    # Go through all departments
    soup = get_soup_from_url(urljoin(base=BASE, url=DIRECTORY))
    rows = soup.find_all('tr')

    class_data = []
    # Ignore the footer row
    for row in rows[DEPARTMENT_ROW_START:-1]:
        dept_name = row.contents[0].string

        if SKIP_NON_AS:
            if NAME_MAPPING.get(dept_name, {}).get('School', 'Other') != 'A&S':
                print(f'SKIPPING: {dept_name}')
                continue

        term_links = row.find_all('a')

        # Follow all term links if exist
        term = ''
        for link in term_links:
            term = link.string

            # Follow all links whose text starts with Section and extract data
            term_soup = get_soup_from_url(urljoin(base=BASE, url=link['href']))
            class_links = term_soup.find_all('a', href=True, text=re.compile('^Section'))

            for link in class_links:
                class_info = DirectoryClass(url=urljoin(base=BASE, url=link['href']))
                class_data.append(class_info.data)
                fieldnames.update(class_info.fieldnames)

            print(f'{dept_name} - {term} done.')

    if class_data:
        # Pickle backup
        with open(f'directory_of_classes_scraper/backup.bak', 'wb') as f:
            pickle.dump(class_data, f)

        # Write to CSV
        timestamp = datetime.date.today()
        with open(f'directory_of_classes_scraper/{timestamp}.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for data in class_data:
                writer.writerow(data)
    else:
        print("No data to write.")
