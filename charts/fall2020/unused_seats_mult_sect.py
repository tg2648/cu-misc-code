# Standard library imports
import os
from pathlib import Path
import csv

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
    autolabel(rects, ax)

    rects = ax.bar(range(len(bins) - 1), hist, bottom=hist, width=1, edgecolor='k')
    autolabel(rects, ax)

    # x-axis labels
    ax.set_xticks(range(len(bins) - 1))
    ax.set_xticklabels(bin_labels)

    # y-axis grid
    ax.set_axisbelow(True)
    ax.yaxis.grid(True, linestyle='dashed', color='gray', alpha=.25)

    # Axis format
    formatter = ticker.StrMethodFormatter('{x:,.0f}')
    ax.yaxis.set_major_formatter(formatter)

    ax.set_ylabel('Number of classes', fontproperties=font)
    ax.set_xlabel('Difference between class enrollments and course cap', fontproperties=font)
    ax.set_title(f'{title} (n={len(data):,})', fontproperties=font)

    plt.xticks(rotation=70)

    fig.tight_layout()
    plt.savefig(f"{os.getenv('OUTPUT_FOLDER')}/Unused Seats Multiple Sections/{title}.png", format='png', dpi=600)
    print(f'Saved: {title}')


def stacked_hist(chart_data):
    # https://gist.github.com/jsoma/c61e56819e4ae315ad5d194a630ccb23

    df = pd.DataFrame(chart_data)
    ax = df.plot(stacked=True, kind='bar', figsize=(12, 8), rot='horizontal')

    # # .patches is everything inside of the chart
    # for rect in ax.patches:
    #     # Find where everything is located
    #     height = rect.get_height()
    #     width = rect.get_width()
    #     x = rect.get_x()
    #     y = rect.get_y()

    #     if height > 0:
    #         # The height of the bar is the data value and can be used as the label
    #         label_text = f'{height:.2f}'  # f'{height:.2f}' to format decimal values

    #         # ax.text(x, y, text)
    #         label_x = x + width - 0.2  # adjust 0.2 to center the label
    #         label_y = y + height / 2
    #         ax.text(label_x, label_y, label_text, ha='right', va='center', fontsize=8)

    # x-axis labels
    ax.set_xticks(range(len(bins) - 1))
    ax.set_xticklabels(bin_labels)

    # y-axis grid
    ax.set_axisbelow(True)
    ax.yaxis.grid(True, linestyle='dashed', color='gray', alpha=.25)

    # Axis format
    formatter = ticker.StrMethodFormatter('{x:,.0f}')
    ax.yaxis.set_major_formatter(formatter)

    ax.set_ylabel('Number of classes', fontproperties=font)
    ax.set_xlabel('Difference between class enrollments and course cap', fontproperties=font)
    # ax.set_title(f'{title} (n={len(data):,})', fontproperties=font)

    plt.xticks(rotation=70)

    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)    
    plt.show()

# Load environment variables
basedir = Path(__file__).parent.resolve()
env_path = basedir / '.env'
load_dotenv(dotenv_path=env_path)

# Constants
DIV_CODES = ('SS', 'HUM', 'NS', 'INST')
TERM = '20193'
COURSE_TYPES = 'LANGUAGE'
# COURSE_TYPES = ('LECTURE', 'SEMINAR', 'LANGUAGE')
PRIMARY_INSTRUCTOR_FLAG = ('Y', 'NULL')
EXCLUDED_CAP = 999
EXCLUDED_SECTIONS = ('R01', 'R02', 'R06', 'R03', 'R04', 'R05', 'D04', 'D05', 'D01', 'OO3', 'OO2')
EXCLUDED_IDS = ('QMSSG5000', 'ECONW4999', 'CHEMW2496', 'HISTG6999', 'HISTG6998')

# Chart config variables
bins = [
    -350,
    -300,
    -250,
    -200,
    -150,
    -99,
    -49,
    -39,
    -29,
    -19,
    -9,
    0,
    11,
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
cap_filter = df['Class_Maximum_Count'].ne(EXCLUDED_CAP)
enrl_filter = df['Student_Enrollment_Count'].ne(0)
section_filter = df['Section_Code'].isin(EXCLUDED_SECTIONS)
courseid_filter = df['Course_Identifier'].isin(EXCLUDED_IDS)
# course_filter = df['Course_Type_Name'].isin(COURSE_TYPES)
course_filter = df['Course_Type_Name'].eq(COURSE_TYPES)

# Filter common to all charts
dff = df[term_filter & course_filter & div_filter & instr_filter & cap_filter
         & enrl_filter & ~section_filter & ~courseid_filter]

# Add counts of each course ID (without copying it would be trying to modify a 'view')
dff = dff.copy()
dff['Counts'] = dff['Course_Identifier'].map(dff['Course_Identifier'].value_counts())
dff.to_csv(f"{os.getenv('OUTPUT_FOLDER')}/test.csv")

# Aggregate classes with multiple sections
dff = dff.groupby('Course_Identifier').agg({'Class_Maximum_Count': 'sum',
                                            'Student_Enrollment_Count': 'sum',
                                            'Counts': 'count'})
dff.to_csv(f"{os.getenv('OUTPUT_FOLDER')}/test_agg.csv")

counts = dff['Counts'].unique()
counts.sort()

chart_data = {}

with open(f"{os.getenv('OUTPUT_FOLDER')}/{TERM}_{COURSE_TYPES}_Mult_Sections_Histogram.csv", 'w', newline='') as csvfile:
    fieldnames = ['bin', 'sections', 'classes']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for section_count in counts[1:]:
        dff_chart = dff[dff['Counts'] == section_count]
        x = list(dff_chart['Student_Enrollment_Count'] - dff_chart['Class_Maximum_Count'])

        # Calculate histogram
        histogram, bin_edges = np.histogram(x, bins=bins)
        chart_data[section_count] = histogram

        for label, class_count in zip(bin_labels, histogram):
            writer.writerow({'bin': label, 'sections': section_count, 'classes': class_count})

        # print(f'Sections: {count}')
        # print(f'bin_edges: {list(bin_edges)}')
        # print(f'histogram: {list(histogram)}')

# print(chart_data)
stacked_hist(chart_data)




# count_column = dff.groupby('Course_Identifier').size()
# Find courses with multiple sections
# dff = dff.groupby('Course_Identifier').filter(lambda x: len(x) > 1)

# dff['Count'] = count_column
# dff = dff.groupby('Course_Identifier').size().reset_index(name='Count')


# dff_grouped = dff.groupby('Course_Identifier')





# course_filter = df['Course_Type_Name'].isin(COURSE_TYPES)
# df_filtered = df[course_filter & div_filter & instr_filter & cap_filter & enrl_filter &
#                  ~section_filter & ~courseid_filter]
# x = df_filtered['Student_Enrollment_Count'] - df_filtered['Class_Maximum_Count']
# hist(data=x, title='All classes')

# course_filter = df['Course_Type_Name'].eq(COURSE_TYPES[0])
# df_filtered = df[course_filter & div_filter & instr_filter & cap_filter & enrl_filter &
#                  ~section_filter & ~courseid_filter]
# x = df_filtered['Student_Enrollment_Count'] - df_filtered['Class_Maximum_Count']
# hist(data=x, title='Lecture classes')

# course_filter = df['Course_Type_Name'].eq(COURSE_TYPES[1])
# df_filtered = df[course_filter & div_filter & instr_filter & cap_filter & enrl_filter &
#                  ~section_filter & ~courseid_filter]
# x = df_filtered['Student_Enrollment_Count'] - df_filtered['Class_Maximum_Count']
# hist(data=x, title='Seminar classes')

# course_filter = df['Course_Type_Name'].eq(COURSE_TYPES[2])
# df_filtered = df[course_filter & div_filter & instr_filter & cap_filter & enrl_filter &
#                  ~section_filter & ~courseid_filter]
# x = df_filtered['Student_Enrollment_Count'] - df_filtered['Class_Maximum_Count']
# hist(data=x, title='Language classes')