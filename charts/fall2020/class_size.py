# Standard library imports
import os
from pathlib import Path

# Third party imports
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.font_manager as font_manager
import numpy as np
import pandas as pd


def make_bin_labels(bins):
    bin_labels = []
    for i in range(len(bins) - 1):
        bin_labels.append(f'{bins[i]}, {bins[i+1]-1}')
    return bin_labels


def autolabel(rects, ax):
    """
    Attach a text label above each bar in *rects*, displaying its height.
    https://matplotlib.org/3.2.1/gallery/lines_bars_and_markers/barchart.html
    """
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'{height:,}',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 0.5),  # points vertical offset
                    textcoords='offset points',
                    ha='center', va='bottom')


def hist(data, title):
    # Calculate histogram
    hist, bin_edges = np.histogram(data, bins=bins)

    # Plot the histogram as a bar chart (since bins are not uniform)
    # https://stackoverflow.com/questions/58183804/matplotlib-histogram-with-equal-bars-width
    fig, ax = plt.subplots()
    rects = ax.bar(range(len(bins) - 1), hist, width=1, edgecolor='k')
    ax.set_xticks(range(len(bins) - 1))
    ax.set_xticklabels(bin_labels)

    ax.set_axisbelow(True)
    ax.yaxis.grid(True, linestyle='dashed', color='gray', alpha=.25)

    # Axis format
    formatter = ticker.StrMethodFormatter('{x:,.0f}')
    ax.yaxis.set_major_formatter(formatter)

    ax.set_ylabel('Number of classes', fontproperties=font)
    ax.set_xlabel('Class size', fontproperties=font)
    ax.set_title(f'{title} (n={len(data):,})', fontproperties=font)

    autolabel(rects, ax)
    autolabel(rects, ax)

    plt.xticks(rotation=70)

    fig.tight_layout()
    plt.savefig(f"{os.getenv('OUTPUT_FOLDER')}/Class Size/{title}.png", format='png', dpi=600)
    print(f'Saved: {title}')


# Load environment variables
basedir = Path(__file__).parent.resolve()
env_path = basedir / '.env'
load_dotenv(dotenv_path=env_path)

# Constants
DIV_CODES = ('SS', 'HUM', 'NS', 'INST', 'CORE')
COURSE_TYPES = ('LECTURE', 'SEMINAR', 'LANGUAGE')
PRIMARY_INSTRUCTOR_FLAG = ('Y', 'NULL')
TERM = '20193'
EXCLUDED_CAP = 999
EXCLUDED_SECTIONS = ('R01', 'R02', 'R06', 'R03', 'R04', 'R05', 'D04', 'D05', 'D01', 'OO3', 'OO2')
EXCLUDED_IDS = ('QMSSG5000', 'ECONW4999', 'CHEMW2496')

# Chart config variables
bins = [
    1,
    6,
    11,
    16,
    26,
    36,
    51,
    101,
    999
]
bin_labels = make_bin_labels(bins)
bin_labels[-1] = f'{bins[-2]}+'

font = font_manager.FontProperties(family='Arial', size=13)

# Filter data
data_path = os.getenv('DATA_PATH')
columns = {
    'Termid': np.str,
    'Course_Identifier': np.str,
    'Academic_Department_Code': np.str,
    'Division_Code': np.str,
    'Academic_Department_Name': np.str,
    'Class_Maximum_Count': np.int,
    'Course_Type_Name': np.str,
    'Section_Code': np.str,
    'Primary_Instructor_Flag': np.str,
    'Student_Enrollment_Count': np.int,
}

df = pd.read_excel(data_path, keep_default_na=False, usecols=list(columns.keys()), dtype=columns)

term_filter = df['Termid'].eq(TERM)
div_filter = df['Division_Code'].isin(DIV_CODES)
instr_filter = df['Primary_Instructor_Flag'].isin(PRIMARY_INSTRUCTOR_FLAG)
section_filter = df['Section_Code'].isin(EXCLUDED_SECTIONS)

course_filter = df['Course_Type_Name'].isin(COURSE_TYPES)
df_filtered = df[course_filter & term_filter & div_filter & instr_filter & ~section_filter]
x = df_filtered['Student_Enrollment_Count']
hist(data=x, title='All classes')

course_filter = df['Course_Type_Name'].eq(COURSE_TYPES[0])
df_filtered = df[course_filter & term_filter & div_filter & instr_filter & ~section_filter]
x = df_filtered['Student_Enrollment_Count']
hist(data=x, title='Lecture classes')

course_filter = df['Course_Type_Name'].eq(COURSE_TYPES[1])
df_filtered = df[course_filter & term_filter & div_filter & instr_filter & ~section_filter]
x = df_filtered['Student_Enrollment_Count']
hist(data=x, title='Seminar classes')

course_filter = df['Course_Type_Name'].eq(COURSE_TYPES[2])
df_filtered = df[course_filter & term_filter & div_filter & instr_filter & ~section_filter]
x = df_filtered['Student_Enrollment_Count']
hist(data=x, title='Language classes')

course_filter = df['Course_Type_Name'].isin(COURSE_TYPES)
div_filter = df['Division_Code'].eq('CORE')
df_filtered = df[course_filter & term_filter & div_filter & instr_filter & ~section_filter]
x = df_filtered['Student_Enrollment_Count']
hist(data=x, title='Core classes')
