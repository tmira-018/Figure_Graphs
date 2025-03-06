import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np
from scipy import stats
from scipy.stats.contingency import odds_ratio
import os

# Import data
nbt_df = pd.read_excel('DataSheets/combined_nbt_mbpnls_24.xlsx',
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
plt.savefig("Figure_Outputs/abberant_timeline.pdf", format='pdf')
plt.show()

# Find average number of aberrant structures in 5 dpf fish
nbt_5avg= nbt_timeline[nbt_timeline['dpf'] == 5]
nbt_5avg.groupby('condition')['aberrant'].mean()
nbt_5avg.groupby('condition')['aberrant'].median()

# Remove fish with 0 aberrant structures
nbt_5ab = nbt_5avg[nbt_5avg['aberrant'] != 0]
nbt_sum = nbt_5ab.groupby('condition').sum()
contingency_table= nbt_sum[['neurons', 'aberrant']]

# Plot neurons over abberant 

sns.swarmplot(data = nbt_5avg, x = 'aberrant', y = 'neurons',
              hue = 'condition')



res = odds_ratio(contingency_table[['neurons','aberrant']], kind='conditional')
odds_ratio_res = res.statistic
lower_confint, upper_confint = res.confidence_interval(confidence_level=0.95)

print(f"Odds Ratio   : {odds_ratio_res}")
print(f"Lower 95% CI : {lower_confint}")
print(f"Upper 95% CI : {upper_confint}")