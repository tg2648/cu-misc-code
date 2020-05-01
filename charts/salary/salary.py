# Standard library imports
import os
import json
import logging
from pathlib import Path

# Third party imports
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.colors as mcolors  # https://matplotlib.org/gallery/color/named_colors.html
from scipy import stats
from scipy.stats import t
import pandas as pd
import numpy as np

# Load environment variables
basedir = Path(__file__).parent.resolve()
env_path = basedir / '.env'
load_dotenv(dotenv_path=env_path)

logging.basicConfig(level=logging.INFO)

data_path = os.getenv('DATA_PATH')
output_path = Path(os.getenv('OUTPUT_PATH'))

with open(os.getenv('DEPT_NAMES_PATH')) as f:
    dept_names = json.load(f)

df = pd.read_excel(data_path, sheet_name='Pivot for Python', skiprows=4)
depts = df['DEPT'].unique()

div_counts = {'HUM': 0, 'NS': 0, 'SS': 0}  # Want to number charts in each division separately
div_names = {'HUM': 'Humanities', 'NS': 'Natural Sciences', 'SS': 'Social Sciences'}

for dept in depts:

    x = np.array(df[(df['DEPT'] == dept)]['Year Since Degree'])
    y = np.array(df[(df['DEPT'] == dept)]['Sum of Primary Dept-Full Base'])

    slope, intercept, r_value, p_value, seg = stats.linregress(x=x, y=y)

    n = len(x)
    mx = np.mean(x)
    sx = np.sum(x)
    sx2 = np.sum(x**2)
    smx2 = np.sum(((x - mx)**2))
    STEYX = seg * np.sqrt(smx2)  # Equivalent to the STEYX Excel function: https://stackoverflow.com/questions/2038667/scipy-linregress-function-erroneous-standard-error-return

    # T critical value from the two-tailed inverse of the Student's t-distribution
    # p-value is 0.005 but divided by two because two-tailed
    t_val = t.isf(0.0025, n - 2)

    sd = STEYX * np.sqrt((1 / n) + (n * (x - mx)**2 / (n * sx2 - sx**2)))  # estimated sd of intercept+slope(x) - column Y in the spreadsheet
    lower_interval = intercept + slope * x - t_val * sd  # Column AB

    # The lower bound needs to be sorted for the line to follow from one marker to the next correctly
    ix = np.lexsort([x])  # array of integer indices that describes the sort order
    x_sorted = [x[i] for i in ix]
    li_sorted = [lower_interval[i] for i in ix]

    # Plotting

    fig, ax = plt.subplots()
    fig.set_size_inches(7.5, 4)

    # Axis limits
    ax.set_xlim([0, max(x) * 1.1])
    ax.set_ylim([0, max(y) * 1.1])

    # Axis currency format
    formatter = ticker.StrMethodFormatter('${x:,.0f}')
    ax.yaxis.set_major_formatter(formatter)

    women_logical = (df['DEPT'] == dept) & (df['Gender'] == 'F') & (df['URM'] == 'N')
    women_urm_logical = (df['DEPT'] == dept) & (df['Gender'] == 'F') & (df['URM'] == 'Y')
    men_logical = (df['DEPT'] == dept) & (df['Gender'] == 'M') & (df['URM'] == 'N')
    men_urm_logical = (df['DEPT'] == dept) & (df['Gender'] == 'M') & (df['URM'] == 'Y')

    ax.plot(
        df[men_logical]['Year Since Degree'],
        df[men_logical]['Sum of Primary Dept-Full Base'],
        label='Men',
        linestyle='',
        marker='D',
        markeredgecolor=mcolors.CSS4_COLORS['wheat'],
        markeredgewidth=1.0,
        markersize=6.0,
        color=mcolors.CSS4_COLORS['sandybrown']
    )

    ax.plot(
        df[men_urm_logical]['Year Since Degree'],
        df[men_urm_logical]['Sum of Primary Dept-Full Base'],
        label='Men URM',
        linestyle='',
        marker='D',
        markeredgecolor=mcolors.CSS4_COLORS['black'],
        markeredgewidth=1.0,
        markersize=7.0,
        color=mcolors.CSS4_COLORS['goldenrod']
    )

    ax.plot(
        df[women_logical]['Year Since Degree'],
        df[women_logical]['Sum of Primary Dept-Full Base'],
        label='Women',
        linestyle='',
        marker='D',
        markeredgecolor=mcolors.CSS4_COLORS['aliceblue'],
        markeredgewidth=1.0,
        markersize=7.0,
        color=mcolors.CSS4_COLORS['lightskyblue']
    )

    ax.plot(
        df[women_urm_logical]['Year Since Degree'],
        df[women_urm_logical]['Sum of Primary Dept-Full Base'],
        label='Women URM',
        linestyle='',
        marker='D',
        markeredgecolor=mcolors.CSS4_COLORS['black'],
        markeredgewidth=1.0,
        markersize=7.0,
        color=mcolors.CSS4_COLORS['dodgerblue']
    )

    ax.plot(x, intercept + slope * x, label='Linear regression', color='k', linewidth=0.8)
    ax.plot(x_sorted, li_sorted, '--', label='Lower bound', color='k', linewidth=0.8)

    # Show the major grid lines with dark grey lines
    plt.grid(b=True, which='major', axis='y', color=mcolors.CSS4_COLORS['lightgray'], linestyle='-')

    # Titles
    div = df[(df['DEPT'] == dept)]['DIV'].iloc[0]  # Increment division chart counter
    div_counts[div] = div_counts[div] + 1

    ax.set_title(f"Chart {div_counts[div]} {div_names[div]}: {dept_names.get(dept, 'n/a')} Tenured Faculty")
    ax.set_xlabel('Years Since Highest Degree Received')
    ax.set_ylabel('Full Base Salary in Primary Department')

    # Legend and canvas adjustments to fit legend
    # plt.legend(loc='lower left')
    plt.legend(bbox_to_anchor=(1, 1), loc='upper left')

    # plt.legend(bbox_to_anchor=(1.52, 1), loc='upper right', borderaxespad=0)
    # plt.subplots_adjust(left=0.16)
    # plt.subplots_adjust(right=0.70)

    plt.tight_layout()
    plt.savefig(output_path / f'{dept}.png', dpi=600)
    logging.info(f'Saved: {dept}.png')
    plt.close()

logging.info('DONE')
