
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

glast_df = pd.read_excel('/Graphs/DataSheets/glast_aberrants.xlsx',
                         sheet_name = 'combined_5dpf')

glast_df['ratio'] = glast_df['wrapped'] / glast_df['total']

fig, ax = plt.subplots(figsize = (5,6))
sns.boxplot(data = glast_df, x = 'cond', y = 'total',
            hue = 'cond', fill = False, widths = 0.3,
            palette = ['black', 'black'],
            linewidth = 0.9, legend = False, ax = ax)
sns.swarmplot(data = glast_df, x = 'cond', y = 'total',
              hue = 'cond', dodge = False,
              palette = ["#1768AC", "#F72585"], s = 10,
              legend = True, ax= ax)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_ylim(-1, 14)
#plt.savefig('Figure_Outputs/glast_total_aberrants.pdf', format='pdf')
plt.show()


fig, ax = plt.subplots(figsize = (5,6))
sns.boxplot(data = glast_df, x = 'cond', y = 'ratio',
            hue = 'cond', fill = False, widths = 0.3,
            palette= ['black', 'black'], linewidth= 0.9,
            legend = False, ax= ax)
sns.swarmplot(data = glast_df, x = 'cond', y = 'ratio',
              hue = 'cond', dodge = False,
              palette = ["#1768AC", "#F72585"], s = 10,
              legend = True, ax= ax)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
#plt.savefig('Figure_Outputs/glast_ratio.pdf', format='pdf')
plt.show()