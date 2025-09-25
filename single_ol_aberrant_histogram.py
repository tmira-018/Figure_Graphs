
import os
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

path = ('/Users/miramota/Desktop/Graphs/DataSheets/WIN_single_cell.xlsx')
ol_df = pd.read_excel(path)

ol_analysis= ol_df[ol_df['cell_ID'].map(ol_df['cell_ID'].value_counts()) > 1]
#removes cells that were treated with 0.5 um WIN
ol_analysis2 = ol_analysis[ol_analysis.cond != 0.5]

#removes cells that were treated with 0.5 um WIN
#ol_analysis2 = ol_df[ol_df.cond != 0.5]

# get cell names where the cell_age is 3 
cells_age3 = ol_analysis2.loc[ol_analysis2['cell_age'] == 3, 'cell_ID'].unique()
# remove omicron cell
cells_age3_arr = cells_age3[cells_age3 != 'omicron']

# filter the df to only include cells that appear 3 times
ol_3days = ol_analysis2[ol_analysis2['cell_ID'].isin(cells_age3)]

# remove the cells with cell_age == 4
ol_3days = ol_3days[ol_3days['cell_age'] != 4]
ol_3days['aberrant_bool'] = (ol_3days['aberrant'] >=1).astype(int)

summary_3days_df = (
    ol_3days
    .groupby(['cell_age', 'cond']).agg(
              total_cells= ('cell_ID', 'count'),
              aberrant_cells= ('aberrant_bool', 'sum')).reset_index()
)

summary_3days_df['normal'] = summary_3days_df['total_cells'] - summary_3days_df['aberrant_cells']

x = np.arange(1,4,1)
width = 0.3

dmso_data = summary_3days_df[summary_3days_df['cond'] == 0.0]
dmso_data = dmso_data[dmso_data['cell_age'] != 0]
win_data = summary_3days_df[summary_3days_df['cond'] == 1.0]

dmso_data = dmso_data.sort_values('cell_age').reset_index(drop=True)
win_data = win_data.sort_values('cell_age').reset_index(drop=True)



# Plotting histogram of # of aberrant cells per condition
# and the total number of cells in analysis
fig, ax = plt.subplots(figsize = (10,6))
p1 = ax.bar(x - width/2, dmso_data['normal'], width,
        label = 'normal dmso', color = '#08c8ea')
p2 = ax.bar(x - width/2, dmso_data['aberrant_cells'], width,
        bottom = dmso_data['normal'], 
        label = 'aberrant dmso',
        color = "#1768AC")

p3 = ax.bar(x + width/2, win_data['normal'], width,
        label = 'normal win', color = '#F294BE')
p4 = ax.bar(x + width/2, win_data['aberrant_cells'], width,
        bottom = win_data['normal'],
        label = 'aberrant win', 
        color = "#F72585")


def add_labels(bars, values, bottom_values = None):
    for i, (bar,value) in enumerate(zip(bars, values)):
        if value >0: 
            if bottom_values is not None:
                y_pos = bottom_values[i] + value/2
            else:
                y_pos = value / 2
            ax.text(bar.get_x() + bar.get_width()/2, y_pos, 
                    str(int(value)),
                    ha = 'center', va = 'center',
                    fontweight = 'bold',
                    fontsize = 9,
                    color = 'white')
add_labels(p1, dmso_data['normal'])
add_labels(p2, dmso_data['aberrant_cells'], dmso_data['normal'])
add_labels(p3, win_data['normal'])
add_labels(p4, win_data['aberrant_cells'], win_data['normal'])
      

ax.set_xlabel('Cell Age')
ax.set_ylabel('Number of Cells')
ax.set_title('OL count distribution through days')
ax.set_xticks(x)
ax.set_ylim(0,17)
ax.legend()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
#plt.savefig('/Users/miramota/Desktop/Graphs/Figure_Outputs/aberrant_histogram_3days.pdf', format = 'pdf')
plt.show()


fig, ax = plt.subplots(figsize = (10,6))
sns.lineplot(data = ol_3days, 
             x = 'cell_age', y = 'aberrant',
             hue = 'cond',
             legend= True,
             err_style= 'band',
             errorbar= ('ci', 95),
             palette = ['#1768AC', '#F72585'],
             )
ax.set_yticks(np.arange(0,4, 1))
ax.set_xticks(x)
ax.set_ylim(0,3)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
#plt.savefig('/Users/miramota/Desktop/Graphs/Figure_Outputs/aberrant_lineplot.pdf', format = 'pdf')
plt.show()