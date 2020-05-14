"""
Given a list of faculty by year, create a "pivot" where the rows are a union of faculty from all years,
the columns are years. The values are the faculty's FTE for that year or `null`
if person was not present in that year.
"""

# Standard Library
import csv
import os
from pathlib import Path

# Third-party
import pandas as pd
import numpy as np
from dotenv import load_dotenv

# Load environment variables
basedir = Path(__file__).parent.resolve()
env_path = basedir / '.env'
load_dotenv(dotenv_path=env_path)

# Column name constants
ACADEMIC_YEAR_NAME = 'Academic_Year'
DIVISION_CODE_NAME = 'Division_Code'
DEPARTMENT_CODE_NAME = 'Department_Code'
TENURE_STATUS_NAME = 'Tenure_Status'
RANK_NAME = 'Rank'
NAME_NAME = 'Name'
FTE_NAME = 'FTE'
JOINT_NAME = 'Joint_Interdisc'
UNI_NAME = 'UNI'

# Filter constants
YEARS = ['2016/17', '2017/18', '2018/19', '2019/20']
TENURE_STAT = ['Tenured', 'Non-Ten/Ten-Track']

# Column data types
dtypes = {
    ACADEMIC_YEAR_NAME: np.str,
    DIVISION_CODE_NAME: np.str,
    DEPARTMENT_CODE_NAME: np.str,
    TENURE_STATUS_NAME: np.str,
    RANK_NAME: np.str,
    NAME_NAME: np.str,
    FTE_NAME: np.float64,
    JOINT_NAME: np.str,
    UNI_NAME: np.str,
}

df = pd.read_excel(os.getenv('DATA'), sheet_name='Combined FTE', usecols=dtypes.keys(), dtype=dtypes)

# Filter booleans
df_year_filter = df[ACADEMIC_YEAR_NAME].isin(YEARS)
df_ladder_filter = df[TENURE_STATUS_NAME].isin(TENURE_STAT)

# Filter data
df = df[df_year_filter & df_ladder_filter]
df[JOINT_NAME].fillna('', inplace=True)
df.reset_index(drop=True, inplace=True)

depts = df[DEPARTMENT_CODE_NAME].unique()

csv_rows = []
for dept in depts:

    df_dept_filter = df[DEPARTMENT_CODE_NAME].eq(dept)
    df_dept = df[df_dept_filter]  # Only a particular department
    dept_uni_set = df_dept[UNI_NAME].unique()  # Everyone who has ever been with the department

    for uni in dept_uni_set:
        # Extract personal information based on the year of the first occurrence of the person
        df_person_filter = df_dept[UNI_NAME] == uni
        person = df_dept[df_person_filter].iloc[0]
        csv_row = [
            person[DIVISION_CODE_NAME],
            dept,
            uni,
            person[NAME_NAME],
            person[TENURE_STATUS_NAME],
            person[RANK_NAME],
            person[JOINT_NAME]
        ]

        # Check if a person has been in the department in every year
        for year in YEARS:
            df_year_filter = df_dept[ACADEMIC_YEAR_NAME].eq(year)

            if uni in df_dept[df_year_filter][UNI_NAME].values:
                fte = df_dept[df_year_filter & df_person_filter][FTE_NAME].iloc[0]
                csv_row.append(fte)
            else:
                csv_row.append('null')

        csv_rows.append(csv_row)

csv_header = [
    DIVISION_CODE_NAME,
    DEPARTMENT_CODE_NAME,
    UNI_NAME,
    NAME_NAME,
    TENURE_STATUS_NAME,
    RANK_NAME,
    JOINT_NAME
]
csv_header.extend(YEARS)

with open('timeline.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(csv_header)
    writer.writerows(csv_rows)
