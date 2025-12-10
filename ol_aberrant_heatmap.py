
import os
from matplotlib.colors import ListedColormap
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

path = ('/Graphs/DataSheets/WIN_single_cell.xlsx')
ol_df = pd.read_excel(path)

ol_analysis= ol_df[ol_df['cell_ID'].map(ol_df['cell_ID'].value_counts()) > 1]

#removes cells that were treated with 0.5 um WIN and cell age 4
ol_analysis2 = ol_df[ol_df.cond != 0.5]
ol_analysis2 = ol_analysis2[ol_analysis2.cell_age != 4]
ol_analysis2 = ol_analysis2.dropna(subset=['aberrant'])


ol_3analysis = ol_analysis2[ol_analysis2['cell_ID'].map(ol_analysis2['cell_ID'].value_counts()) == 3]   
ol_3analysis['aberrant_bool'] = (ol_3analysis['aberrant']>=1).astype(int)


#pivot table 
dmso_ol_analysis = ol_3analysis[ol_3analysis['cond'] == 0.0]
win_ol_analysis = ol_3analysis[ol_3analysis['cond'] == 1.0]
dmso_pivot = dmso_ol_analysis.pivot_table(index='cell_ID', 
                                           columns='cell_age', 
                                           values='aberrant')
win_pivot = win_ol_analysis.pivot_table(index='cell_ID',
                                        columns = 'cell_age',
                                        values = 'aberrant')

dmso_cmap_dict = {0: "#daebff", 1: "#8fa0da", 2: '#44558f', 3: '#000a44'}
dmso_cmap = ListedColormap([dmso_cmap_dict[i] for i in range(len(dmso_cmap_dict))])

win_cmap_dict = {0: "#F6E0E9BB", 1: "#F5A4C9", 2: '#F72585', 3: "#900946"}
win_cmap = ListedColormap([win_cmap_dict[i] for i in range(len(win_cmap_dict))])

fig,(ax1, ax2) = plt.subplots(1, 2, figsize = (12,6))
sns.heatmap(dmso_pivot, annot= False, cmap = dmso_cmap, cbar= True, 
            vmin = 0, vmax = 3,
            linewidths= 0.5, ax=ax1)
ax1.set_title('DMSO Treated Cells with aberrant process')
ax1.set_ylabel('Cell ID')
ax1.set_xlabel('Cell Age (days)')

sns.heatmap(win_pivot, annot = False,
            cmap = win_cmap, cbar= True,
            linewidths= 0.5, ax=ax2)
ax2.set_title('WIN Treated Cells with aberrant process')
ax2.set_ylabel('Cell ID')
ax2.set_xlabel('Cell Age (days)')
plt.tight_layout()
plt.savefig('/Graphs/single_ol_aberrant_heatmap.pdf', 
            format = 'pdf')
plt.show()


# Summary data for histogram 
# Grouping by cell age and condition
ol_3days_summary = (
    ol_3analysis
    .groupby(['cell_age', 'cond']).agg(
                  total_cells= ('cell_ID', 'count'),
                  aberrant_cells = ('aberrant_bool', 'sum')).reset_index()
)

# Creating new column to calculate the number of normal cells 
ol_3days_summary['normal'] = ol_3days_summary['total_cells'] - ol_3days_summary['aberrant_cells']


dmso_data = ol_3days_summary[ol_3days_summary['cond'] == 0.0]
dmso_data = dmso_data[dmso_data['cell_age'] != 0]
win_data = ol_3days_summary[ol_3days_summary['cond'] == 1.0]

dmso_data = dmso_data.sort_values('cell_age').reset_index(drop=True)
win_data = win_data.sort_values('cell_age').reset_index(drop=True)



# Plotting histogram of # of aberrant cells per condition
# and the total number of cells in analysis

fig, ax = plt.subplots(figsize = (10,6))
cell_age = np.arange(1,4,1)
n_ages = len(cell_age)
x_dmso = np.arange(n_ages)
x_win = 2.5 + cell_age
width = 0.8

for i, age in enumerate(cell_age):
    ax.bar(x_dmso[i], dmso_data.loc[i, 'normal'], width,
           color = "#08c8ea", label = 'normal dmso')
    ax.bar(x_dmso[i], dmso_data.loc[i, 'aberrant_cells'], width,
           bottom=dmso_data.loc[i, 'normal'],
           color="#1768AC", label='aberrant dmso')

for i, age in enumerate(cell_age):
    ax.bar(x_win[i], win_data.loc[i, 'normal'], width,
           color='#F294BE', label='normal win')
    ax.bar(x_win[i], win_data.loc[i, 'aberrant_cells'], width,
           bottom=win_data.loc[i, 'normal'],
           color="#F72585", label='aberrant win')

# Set x-axis labels
all_positions = np.concatenate([x_dmso, x_win])
all_labels = list(cell_age) + list(cell_age)
ax.set_xticks(all_positions)
ax.set_xticklabels(all_labels)
ax.set_ylim(0, 14)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Add condition labels or title
ax.set_xlabel('Cell Age per Condition')
plt.tight_layout()
plt.savefig('/Graphs/aberrant_ol_histogram.pdf',
            format = 'pdf')
plt.show()

