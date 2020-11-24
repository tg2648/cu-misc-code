"""
This algorithm tries to match students to faculty based on student's reported availability
and faculty's class schedule.

Rough algorithm description:

    Finding all matches:

    For each class:
        - For each student:
            - For each day of the week in Class_Days:
                - If Class_Time_Num is a subset of student's availability for that week, then True
            - If True for all days of the week:
                - Add student to Potential_Matches list for that class
                - Increment the Potential_Matches_Count value for that class
                - Add class to Potential_Matches list for that student
                - Increment the Potential_Matches_Count value for that class.

    Assigning matches:

    - Create an Is_Assigned column defaulting to False for student data
    - Write all classes with Potential_Matches_Count = 0 to a file classes_with_no_matches.csv
    - Order classes by Potential_Matches_Count
    - If Potential_Matches_Count = 1, assign that student to the class
    - Whenever a student is assigned to a class, set their Is_Assigned flag to True
    - For classes with Potential_Matches_Count > 1:
        - Look at all potential students where Is_Assigned is False
        - Assign a student with the least Potential_Matches_Count
        - Random selection if Potential_Matches_Count are equal

    - Write all students with Is_Assigned = False to a file students_with_no_matches.csv
"""

# Standard library imports
import os
import sys
from pathlib import Path

# Third party imports
from dotenv import load_dotenv
import pandas as pd
import numpy as np

# Local application imports
sys.path.append(str(Path(__file__).parent.parent.resolve()))  # Add parent directory to sys.path to import utils.py
from utils import progress_bar

TIME_CONVERISON = {
    '8am - 9am': 0,
    '9am - 10am': 1,
    '10am - 11am': 2,
    '11am - 12pm': 3,
    '12pm - 1pm': 4,
    '1pm - 2pm': 5,
    '2pm - 3pm': 6,
    '3pm - 4pm': 7,
    '4pm - 5pm': 8,
    '5pm - 6pm': 9,
    '6pm - 7pm': 10,
    '7pm - 8pm': 11,
    '8pm - 9pm': 12,
    '9pm - 10pm': 13,
    '8 - 9': 0,
    '9 - 10': 1,
    '10 - 11': 2,
    '11 - 12': 3,
    '12 - 13': 4,
    '13 - 14': 5,
    '14 - 15': 6,
    '15 - 16': 7,
    '16 - 17': 8,
    '17 - 18': 9,
    '18 - 19': 10,
    '19 - 20': 11,
    '20 - 21': 12,
    '21 - 22': 13,
}

DAY_OF_WEEK_CONVERSION = {
    'Monday': 'M',
    'Tuesday': 'T',
    'Wednesday': 'W',
    'Thursday': 'R',
    'Friday': 'F',
}


class FormData(object):
    """
    Collection of functions to work with Cognito form data
    """

    @staticmethod
    def convert_times_to_num_vals(col):
        """
        Converts begin and end times in a given column to an array of numerical values.
        Example:
            Monday: 8am - 9am, 9am - 10am
            corresponds to an array of [0, 1] in column M
        Returns:
            Array of arrays
        """
        arr = []
        for row in col:
            times = row.split(', ')

            conv = set()
            for time in times:
                if time:
                    conv.add(TIME_CONVERISON.get(time))
            arr.append(conv)

        return arr


class ClassData(object):
    """
    Collection of functions to work with class data
    """

    @staticmethod
    def convert_class_begin_time(row):
        """
        If the time does not end with '00', round down
        """
        time = row['Class_Begin']

        if time[-2:] != '00':
            return f'{time[:-2]}'
        else:
            return time[:-2]

    @staticmethod
    def convert_class_end_time(row):
        """
        If the time does not end with '00', round up
        """
        time = row['Class_End']

        if time[-2:] != '00':
            return f'{int(time[:-2]) + 1}'
        else:
            return time[:-2]

    @staticmethod
    def convert_times_to_num_vals(row):
        """
        Converts converted class begin and end times to an array of numerical values.
        Example:
        Class_Begin_Conv = 10 and Class_End_Conv = 12 correspond to intervals:
            10-11 and 11-12, which have numerical values of [2, 3]
        """
        begin = int(row['Class_Begin_Conv'])
        end = int(row['Class_End_Conv'])

        n = end - begin
        arr = set()

        for i in range(n):
            arr.add(TIME_CONVERISON.get(f'{begin + (i*1)} - {begin + (i*1) + 1}'))

        return arr


if __name__ == '__main__':

    BASEDIR = Path(__file__).parent.resolve()
    env_path = BASEDIR / '.env'
    load_dotenv(dotenv_path=env_path)

    print('Loading data...')
    # === CLASS DATA ===
    df_c = pd.read_excel(os.getenv('CLASS_DATA'), dtype=np.str, keep_default_na=False)
    df_c = df_c.set_index('ID')
    df_c['Class_Days'] = df_c['Class_Days'].map(lambda x: x.strip())

    # Round up End times and round down Begin times to consider whole hours only
    df_c['Class_Begin_Conv'] = df_c.apply(ClassData.convert_class_begin_time, axis=1)
    df_c['Class_End_Conv'] = df_c.apply(ClassData.convert_class_end_time, axis=1)

    # Convert rounded Begin and End times to an array of numerical values
    df_c['Class_Time_Num'] = df_c.apply(ClassData.convert_times_to_num_vals, axis=1)

    # Initialize additional columns
    df_c['Potential_Matches_Count'] = 0
    df_c['Potential_Matches'] = np.empty((len(df_c), 0)).tolist()  # https://stackoverflow.com/questions/31466769/add-column-of-empty-lists-to-dataframe
    df_c['Student_Match'] = ''

    # === COGNITO DATA ===
    df_f = pd.read_excel(os.getenv('FORM_DATA'), dtype=np.str, keep_default_na=False)
    df_f = df_f.drop(['Entry_Status', 'Entry_DateCreated', 'Entry_DateSubmitted', 'Entry_DateUpdated'], axis=1)
    df_f = df_f.set_index('YourUNI')

    # Convert time ranges to arrays of numerical values
    for long, short in DAY_OF_WEEK_CONVERSION.items():
        df_f[short] = FormData.convert_times_to_num_vals(df_f[long])

    # Initialize additional columns
    df_f['Potential_Matches_Count'] = 0
    df_f['Potential_Matches'] = np.empty((len(df_f), 0)).tolist()
    df_f['Is_Assigned'] = False
    df_f['Class_Match'] = ''

    # ===
    # Count and find potential matches
    # ===

    n_max = len(df_c)
    n = 0
    print('Finding potential matches...')

    # Operate on copies to avoid modified dataframes during the loop
    for clas in df_c.copy().itertuples():
        for stud in df_f.copy().itertuples():
            for day_of_week in clas.Class_Days:
                if not clas.Class_Time_Num.issubset(getattr(stud, day_of_week)):
                    break
            else:
                # Loop exhausted all day_of_week and did not break
                # Meaning the student is a potential match
                df_c.loc[clas.Index, 'Potential_Matches_Count'] += 1
                df_c.loc[clas.Index, 'Potential_Matches'].append(stud.Index)
                df_f.loc[stud.Index, 'Potential_Matches_Count'] += 1
                df_f.loc[stud.Index, 'Potential_Matches'].append(clas.Index)

        progress_bar(n, n_max)
        n += 1

    # ===
    # Assign students
    # ===

    matches_count_unique = sorted(df_c['Potential_Matches_Count'].unique())
    matches_count_unique.remove(0)  # Cases of zero matches are simply written to file later

    n_max = len(matches_count_unique)
    n = 0
    print('\nAssigning students...')

    for matches_count in matches_count_unique:
        df_c_matches = df_c[df_c['Potential_Matches_Count'] == matches_count]

        if matches_count == 1:
            for clas in df_c_matches.itertuples():
                stud_index = df_c.loc[clas.Index, 'Potential_Matches'][0]
                df_c.loc[clas.Index, 'Student_Match'] = stud_index
                df_f.loc[stud_index, 'Class_Match'] = clas.Index
                df_f.loc[stud_index, 'Is_Assigned'] = True
        else:
            for clas in df_c_matches.itertuples():
                df_f_potential = df_f.loc[clas.Potential_Matches, ['Potential_Matches_Count', 'Is_Assigned']]
                df_f_potential = df_f_potential[df_f_potential['Is_Assigned'] == False]  # Only students who have not been matched yet

                if df_f_potential.empty:  # All potential students have already been assigned
                    continue

                df_f_potential = df_f_potential.sort_values(by=['Potential_Matches_Count'])
                stud_index = df_f_potential.iloc[0].name

                df_c.loc[clas.Index, 'Student_Match'] = stud_index
                df_f.loc[stud_index, 'Class_Match'] = clas.Index
                df_f.loc[stud_index, 'Is_Assigned'] = True

        progress_bar(n, n_max)
        n += 1

    # ===
    # Output
    # ===

    print('\nWriting results...')

    df_c_zero = df_c[(df_c['Potential_Matches_Count'] == 0) | (df_c['Student_Match'] == '')]
    df_c_zero.to_csv(BASEDIR / 'classes_with_no_matches.csv')

    df_f_zero = df_f[df_f['Is_Assigned'] == False]
    df_f_zero.to_csv(BASEDIR / 'students_with_no_matches.csv')

    df_c_matched = df_c[df_c['Student_Match'] != '']
    df_c_matched.to_csv(BASEDIR / 'matched_classes.csv')

    df_f_matched = df_f[df_f['Is_Assigned'] == True]
    df_f_matched.to_csv(BASEDIR / 'matched_students.csv')

    print('Done.')
