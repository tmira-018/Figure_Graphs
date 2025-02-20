import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np
from scipy import stats

# Import data
nbt_df = pd.read_excel('/Users/miramota/OHSU Dropbox/Tania Miramontes/Data_sheets/combined_nbt_mbpnls_24.xlsx',
                       sheet_name = 'combined')
# Remove WIN05 condition
nbt_df_analysis = nbt_df[nbt_df.condition != 'WIN05μM']
# Remove fish with only one data point
nbt_timeline = nbt_df_analysis[nbt_df_analysis.groupby('fish_ID').fish_ID.transform('count')>1]


def plot_nbt_mbp_aberrant(df, x_interval = 1, y_interval = 5, figsize = (10, 6)):
    """
    Plot the number of aberrant circles over time, tracking the same fish from 3 -5 dpf.
    Seperated by condition. Plots individual fish as small thin lines and the average 
    as thicker lines with standard error bars at 1 standard error."""

    y_min = 0
    y_max = df['aberrant'].max()
    y_max_rounded = np.ceil(y_max / y_interval) * y_interval

    fig, ax = plt.subplots(figsize = figsize)
    sns.lineplot(data = df, x = 'dpf', y = 'aberrant',
                units = 'fish_ID', estimator = None,
                hue = 'condition',
                palette=["#1768AC", "#F72585", "#420039"],
                legend = False,
                alpha = 0.8, linewidth = .25)
                
    sns.lineplot(data = df, x = 'dpf', y = 'aberrant',
                hue = 'condition', err_style = 'bars',
                err_kws={'capsize': 5, 'capthick': 2, 'elinewidth': 2} ,
                palette=["#1768AC", "#F72585", "#420039"],
                errorbar=("se", 1))

# Customize plot
    plt.title('Number of Aberrant Structures')
    plt.xlabel('Cell Age (Days)')
    plt.ylabel('Number of Aberrant Occurences')
    # plt.legend(title='Condition', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(np.arange(3, 6, x_interval))
    plt.yticks(np.arange(y_min, y_max_rounded + y_interval, y_interval))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

# Adjust layout
    plt.tight_layout()
    return plt.gcf()

#Usage
plot_nbt_mbp_aberrant(df = nbt_timeline)
plt.savefig("/Users/miramota/Desktop/Figures/nbt_mbpnlscaax/abberant_timeline.pdf", format='pdf')
plt.show()

# Find average number of aberrant structures in 5 dpf fish
nbt_5avg= nbt_timeline[nbt_timeline['dpf'] == 5]
nbt_5avg.groupby('condition')['aberrant'].mean()
nbt_5avg.groupby('condition')['aberrant'].median()







