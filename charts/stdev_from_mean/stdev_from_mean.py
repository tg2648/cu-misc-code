# Standard library imports
import os
from pathlib import Path

# Third party imports
from dotenv import load_dotenv

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import scipy.stats as stats
import math
import pandas as pd

# Load environment variables
basedir = Path(__file__).parent.resolve()
env_path = basedir / '.env'
load_dotenv(dotenv_path=env_path)

data_path = os.getenv('DATA_PATH')
df = pd.read_csv(data_path, index_col='ID')

# Normal distribution data
mu = 0
variance = 1
sigma = math.sqrt(variance)
x = np.linspace(mu - 4 * sigma, mu + 4 * sigma, 100)
y = stats.norm.pdf(x, mu, sigma)
x_fill = np.linspace(mu - 1 * sigma, mu + 1 * sigma, 100)
y_fill = stats.norm.pdf(x_fill, mu, sigma)

div_cat = ['SS', 'HUM', 'NS']
ten_cat = ['Tenured', 'Non-tenured']
accept_cat = ['Accepted', 'Declined']

x_data = {}

for div in div_cat:
    for ten in ten_cat:
        for accept in accept_cat:
            index = '_'.join([div, ten, accept])
            x_data[index] = df[(df['Div'] == div) & (df['Tenure'] == ten) & (df['Accept_Status'] == accept)]['StDev_Deviation']

        # Plot normal distribution
        fig, ax = plt.subplots()
        ax.plot(x, y, zorder=2)

        # Plot the data
        x_data_a = df[(df['Div'] == div) & (df['Tenure'] == ten) & (df['Accept_Status'] == 'Accepted')]['StDev_Deviation']
        x_data_d = df[(df['Div'] == div) & (df['Tenure'] == ten) & (df['Accept_Status'] == 'Declined')]['StDev_Deviation']

        for x_i in x_data_a:
            y_i = stats.norm.pdf(x_i, mu, sigma)
            ax.plot([x_i, x_i], [0, y_i], color='green', zorder=1, linewidth=1)

        for x_i in x_data_d:
            y_i = stats.norm.pdf(x_i, mu, sigma)
            ax.plot([x_i, x_i], [0, y_i], color='orange', zorder=1, linewidth=1)

        ## Plot formatting
        ax.set_title(f"{div} {ten}")
        # x-axis
        ax.set_xlim([-4, 4])
        ax.set_xlabel('# of Standard Deviations From the Mean')
        # y-axis
        ax.set_ylim([0, 0.4])
        ax.get_yaxis().set_ticks([])

        # Remove all but bottom border
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)

        # Custom Legend
        custom_lines = [Line2D([0], [0], color='green'),
                        Line2D([0], [0], color='orange')]
        ax.legend(custom_lines, ['Accepted', 'Declined'])

        plt.savefig(basedir / f"{div}_{ten}.png")

        # Also save a version with the fill
        ax.fill_between(x_fill, y_fill, 0, alpha=0.9, color='lavender')
        plt.savefig(basedir / f"{div}_{ten}_fill.png")

# x_h_t_a = df[(df['Div'] == 'SS') & (df['Tenure'] == 'Tenured') & (df['Accept_Status'] == 'Accepted')]['StDev_Deviation']
# x_h_t_d = df[(df['Div'] == 'SS') & (df['Tenure'] == 'Tenured') & (df['Accept_Status'] == 'Declined')]['StDev_Deviation']
# x_h_nt_a = df[(df['Div'] == 'SS') & (df['Tenure'] == 'Non-tenured') & (df['Accept_Status'] == 'Accepted')]['StDev_Deviation']
# x_h_nt_d = df[(df['Div'] == 'SS') & (df['Tenure'] == 'Non-tenured') & (df['Accept_Status'] == 'Declined')]['StDev_Deviation']


# for i in range(4):


# for x_i in x_h_t_a:
#     y_i = stats.norm.pdf(x_i, mu, sigma)
#     ax.plot([x_i, x_i], [0, y_i], color='orange', zorder=1, linewidth=1)

# for x_i in x_h_t_d:
#     y_i = stats.norm.pdf(x_i, mu, sigma)
#     ax.plot([x_i, x_i], [0, y_i], color='green', zorder=1, linewidth=1)

# for x_i in x_h_nt_a:
#     y_i = stats.norm.pdf(x_i, mu, sigma)
#     ax.plot([x_i, x_i], [0, y_i], color='orange', zorder=1, linewidth=1)

# for x_i in x_h_nt_d:
#     y_i = stats.norm.pdf(x_i, mu, sigma)
#     ax.plot([x_i, x_i], [0, y_i], color='green', zorder=1, linewidth=1)

# plt.show()
