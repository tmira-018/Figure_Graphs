
import os
import argparse
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

#Find unique fish IDs per condition
def find_unique_fish(df, condition_column, condition, unique_column):
    cond_df = df[df[condition_column] == condition]
    unique_fish = cond_df[unique_column].nunique()
    return unique_fish

ol_dmso_fish = find_unique_fish(ol_analysis2, 'cond', 0.0, 'fish_ID')
ol_dmso_cells = find_unique_fish(ol_analysis2, 'cond', 0.0, 'cell_ID')

ol_win_fish = find_unique_fish(ol_analysis2, 'cond', 1.0, 'fish_ID')
ol_win_cells = find_unique_fish(ol_analysis2, 'cond', 1.0, 'cell_ID')


# Add boolean column for presence of aberrant cells 
for index, row in ol_analysis2.iterrows():
    if row['aberrant'] >= 1:
        ol_analysis2.loc['aberrant_bool'] = 1
    else:
        ol_analysis2.loc['aberrant_bool'] = 0


# Extracting data where the aberrant boolean value is 1 
ol_time = ol_analysis2[ol_analysis2['aberrant_bool']==1]

fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(data = ol_time, 
                x = 'cell_age',
                hue = 'cond', palette=["#1768AC", "#F72585"],
                multiple = 'stack',
                bins = 7)

for bar in ax.patches:
    height = bar.get_height()
    y = bar.get_y()
    if height >0:
        ax.text(
            bar.get_x() + bar.get_width() /2,
            y + height / 2,
            str(int(height)),
            ha = 'center',
            va = 'center',
            color = 'black',
            weight = 'bold',
            size = 12
    )
x_min, x_max = ax.get_xlim()
plt.xticks(np.arange(1, int(x_max)+1, 1))
ax.set_ylim(0,14)
ax.set_xlabel('Cell Age')
ax.set_ylabel('Number of Cells with mbp egfp+ ring')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_title('Number of individual oligodendrocytes with \n'
                'mbp egfp+ ring across cell age ')
plt.savefig('/Users/miramota/Desktop/Graphs/Figure_Outputs/ol_ab_time.pdf', format = 'pdf')
plt.show()
