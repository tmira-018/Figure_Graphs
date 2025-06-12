
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np
from scipy import stats
import numpy as np

astro_cells = pd.read_excel('DataSheets/glast_cellcounts_pharm_combined.xlsx')

astro_4dpf = astro_cells[astro_cells['dpf'] == 4]
astro_5dpf = astro_cells[astro_cells['dpf'] == 5]

fig,(ax1,ax2) = plt.subplots(1,2, figsize = (10, 6))
fig.suptitle('Number of Astrocytes')
sns.boxplot(data = astro_4dpf,
            x = 'condition', y = 'cell_count',
            hue = 'condition', fill = False, 
            widths = 0.25, linewidth= 0.75,
            palette = ['black', 'black'], legend= False, ax= ax1)
sns.stripplot(data = astro_4dpf,
              x = 'condition', y = 'cell_count',
              hue = 'condition',
              palette= ["#276FBF", "#F72585"],
              legend= False, ax = ax1)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.set_ylim(0, 250)
ax1.set_title('4 dpf')
sns.boxplot(data= astro_5dpf,
            x = 'condition', y= 'cell_count',
             hue = 'condition', fill= False, 
             widths = 0.25, linewidth = 0.75,
             palette = ['black', 'black'], legend = False, 
              ax = ax2)
sns.stripplot(data = astro_5dpf, 
              x = 'condition', y = 'cell_count',
               hue = 'condition', 
               palette= ["#276FBF", "#F72585"], 
               legend = False, ax = ax2)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.set_ylim(0, 250)
ax2.set_title('5 dpf')
plt.savefig('Figure_Outputs/astrocyte_counts.pdf', format = 'pdf')

# make numpy array for stats
astro_4dpf_dmso = astro_4dpf[astro_4dpf['condition'] == 0]['cell_count'].to_numpy()
astro_4dpf_1um = astro_4dpf[astro_4dpf['condition'] == 1]['cell_count'].to_numpy()

tstat_4dpf, pvalue_4dpf = stats.ttest_ind(astro_4dpf_dmso, astro_4dpf_1um)
print(f't-statistic: {tstat_4dpf}, p-value: {pvalue_4dpf}')

astro_5dpf_dmso = astro_5dpf[astro_5dpf['condition'] == 0]['cell_count'].to_numpy()
astro_5dpf_1um = astro_5dpf[astro_5dpf['condition'] == 1]['cell_count'].to_numpy()

tstat_5dpf, pvalue_5dpf = stats.ttest_ind(astro_5dpf_dmso, astro_5dpf_1um)
print(f't-statistic: {tstat_5dpf}, p-value: {pvalue_5dpf}')