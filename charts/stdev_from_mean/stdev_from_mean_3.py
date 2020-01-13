# Standard library imports
import os
from pathlib import Path

# Third party imports
from dotenv import load_dotenv

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import scipy.stats as stats
import pandas as pd

# Load environment variables
basedir = Path(__file__).parent.resolve()
env_path = basedir / '.env'
load_dotenv(dotenv_path=env_path)

data_path = os.getenv('DATA_PATH')
df = pd.read_csv(data_path, index_col='ID')


div_cat = ['All', 'SS', 'HUM', 'NS']
ten_cat = ['Tenured', 'Non-tenured']
accept_cat = ['Accepted', 'Declined']

# Chart config variables
bins = np.arange(-4, 4.5, 0.5)

colors = {
    'Accepted': 'green',
    'Declined': 'orange'
}

div_names = {
    'All': 'Three Divisions Combined',
    'NS': 'Natural Sciences',
    'SS': 'Social Sciences',
    'HUM': 'Humanities'
}

# Assemble initial histograms
hist_n_max = {}  # Keep track of maximum histogram values

for div in div_cat:
    fig, ax = plt.subplots(nrows=2, ncols=2, constrained_layout=True)
    fig.suptitle(f'{div_names[div]}')
    # fig.suptitle(f'{div_names[div]}\n\nDeviation of Recruitment Offer Salary as Number of\nStandard Deviations from Departmental Mean (x-axis)')

    col = 0
    n_max = 0
    for ten in ten_cat:
        row = 0
        for accept in accept_cat:

            if div == 'All':
                x_data = df[(df['Tenure'] == ten) & (df['Accept_Status'] == accept)]['StDev_Deviation']
            else:
                x_data = df[(df['Div'] == div) & (df['Tenure'] == ten) & (df['Accept_Status'] == accept)]['StDev_Deviation']

            ax[row][col].set_title(f"{ten} {accept} (n={len(x_data)})")
            n, bins, patches = ax[row][col].hist(x_data, bins, edgecolor='black', linewidth=0.5, alpha=0.55, color=colors[accept])

            if np.max(n) > n_max:
                n_max = np.max(n)

            row += 1

        col += 1

    # Format histograms and plot normal distribution
    col = 0
    for ten in ten_cat:
        row = 0
        for accept in accept_cat:

            # Plot normal distribution
            mu = 0
            sigma = 1
            x_norm = np.linspace(mu - 4 * sigma, mu + 4 * sigma, 100)
            y_norm = stats.norm.pdf(x_norm, mu, sigma)
            scaling_factor = n_max / np.max(y_norm)
            ax[row][col].plot(x_norm, y_norm * scaling_factor, zorder=2, linewidth=1)

            # y-axis range
            ax[row][col].set_ylim([0, n_max * 1.05])

            # Axis tick interval
            if n_max > 50:
                y_tick_spacing = 10
            elif n_max > 30:
                y_tick_spacing = 4
            elif n_max > 10:
                y_tick_spacing = 2
            else:
                y_tick_spacing = 1

            ax[row][col].yaxis.set_major_locator(ticker.MultipleLocator(y_tick_spacing))

            ax[row][col].xaxis.set_major_locator(ticker.MultipleLocator(1))
            ax[row][col].xaxis.set_minor_locator(ticker.MultipleLocator(0.5))

            row += 1

        col += 1

    plt.savefig(basedir / f"3/{div}_Recruitment_Sal_Dev_From_Mean.png")
    # plt.show()
