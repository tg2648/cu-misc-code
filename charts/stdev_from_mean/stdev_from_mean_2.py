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

for div in div_cat:
    fig, ax = plt.subplots(nrows=2, ncols=2, constrained_layout=True)
    fig.suptitle(f'{div_names[div]}\n\nDeviation of Recruitment Offer Salary as Number of\nStandard Deviations from Departmental Mean (x-axis)')
    col = 0

    for ten in ten_cat:
        row = 0
        for accept in accept_cat:

            if div == 'All':
                x_data = df[(df['Tenure'] == ten) & (df['Accept_Status'] == accept)]['StDev_Deviation']
            else:
                x_data = df[(df['Div'] == div) & (df['Tenure'] == ten) & (df['Accept_Status'] == accept)]['StDev_Deviation']

            n, bins, patches = ax[row][col].hist(x_data, bins, edgecolor='black', linewidth=0.5, alpha=0.55, color=colors[accept])
            ax[row][col].set_title(f"{ten} {accept} (n={len(x_data)})")

            # # Plot normal distribution
            mu = 0
            sigma = 1
            x_norm = np.linspace(mu - 4 * sigma, mu + 4 * sigma, 100)
            y_norm = stats.norm.pdf(x_norm, mu, sigma)
            scaling_factor = np.max(n) / np.max(y_norm)
            ax[row][col].plot(x_norm, y_norm * scaling_factor, zorder=2, linewidth=1)

            # y-axis
            # ax.set_ylim([0, 0.4])
            # ax.get_yaxis().set_ticks([])
            if np.max(n) > 30:
                y_tick_spacing = 4
            elif np.max(n) > 10:
                y_tick_spacing = 2
            else:
                y_tick_spacing = 1

            ax[row][col].yaxis.set_major_locator(ticker.MultipleLocator(y_tick_spacing))

            # # x-axis
            # ax[row][col].set_xlim([-4, 4])
            # ax[row][col].set_xlabel('# of Standard Deviations From Departmental Mean')
            row += 1
        col += 1

    # fig.tight_layout()
    plt.savefig(basedir / f"2/{div}_Recruitment_Sal_Dev_From_Mean.png")
    # plt.show()

# x_data_a = df[(df['Div'] == div) & (df['Tenure'] == ten) & (df['Accept_Status'] == 'Accepted')]['StDev_Deviation']
# x_data_d = df[(df['Div'] == div) & (df['Tenure'] == ten) & (df['Accept_Status'] == 'Declined')]['StDev_Deviation']
# ax1.hist(x_data_a, bins, edgecolor='black', linewidth=0.5, alpha=0.5, color='green')
# ax2.hist(x_data_d, bins, edgecolor='black', linewidth=0.5, alpha=0.5, color='orange')
# ax3.hist(x_data_a, bins, edgecolor='black', linewidth=0.5, alpha=0.5, color='green')
# ax4.hist(x_data_d, bins, edgecolor='black', linewidth=0.5, alpha=0.5, color='orange')
# # bins = np.arange(-4, 5.5, 1)
# # ax.hist(x_data, bins, edgecolor='black', linewidth=0.5, alpha=0.5, color=['green','orange'])


# for x_i in x_data_a:
#     y_i = stats.norm.pdf(x_i, mu, sigma)
#     ax.plot([x_i, x_i], [0, y_i], color='green', zorder=1, linewidth=1)

# for x_i in x_data_d:
#     y_i = stats.norm.pdf(x_i, mu, sigma)
#     ax.plot([x_i, x_i], [0, y_i], color='orange', zorder=1, linewidth=1)

# ## Plot formatting
# ax1.set_title(f"{div} {ten} (n={len(x_data_a)} 1)")
# ax2.set_title(f"{div} {ten} (n={len(x_data_d)} 2)")
# ax3.set_title(f"{div} {ten} (n={len(x_data_d)} 3)")
# ax4.set_title(f"{div} {ten} (n={len(x_data_d)} 4)")
# x_tick_spacing = 1
# ax.xaxis.set_major_locator(ticker.MultipleLocator(x_tick_spacing))


# # Remove all but bottom border
# ax.spines['top'].set_visible(False)
# ax.spines['right'].set_visible(False)
# # ax.spines['left'].set_visible(False)

# # Custom Legend
# custom_lines = [Line2D([0], [0], color='green'),
#                 Line2D([0], [0], color='orange')]
# ax.legend(custom_lines, ['Accepted', 'Declined'])


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
