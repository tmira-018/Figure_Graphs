
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np
from scipy import stats
import numpy as np

astro_cells = pd.read_excel('DataSheets/glast_cellcounts_pharm_combined.xlsx')

astro_4dpf = astro_cells[astro_cells['dpf'] == 4]
astro_5dpf = astro_cells[astro_cells['dpf'] == 5]

fig, (ax1, ax2) = plt.subplots(1,2, sharey=True, figsize = (8, 6))
sns.boxplot(data = astro_4dpf,
            x = "condition", y= "cell_count", hue = "condition",
            widths = 0.8,
            ax= ax1, fill=False, legend=False, 
            palette = ['black', 'black'], linewidth = 0.9)
sns.swarmplot(data= astro_4dpf,
                x= "condition", y= "cell_count", hue = "condition",
                ax= ax1, legend=False, s = 10,
                palette = ["#1768AC", "#F72585"])
sns.boxplot(data= astro_5dpf,
            x= "condition", y= "cell_count", hue = "condition",
            widths = 0.8,
            ax=ax2, fill=False, legend=False, 
            palette = ['black', 'black'], linewidth= 0.9)
sns.swarmplot(data= astro_5dpf,
                x= "condition", y= "cell_count", hue = "condition",
                s = 10,
                ax=ax2, palette = ["#1768AC", "#F72585"])
ax2.scatter(0, mean_5dpf_dmso, color = 'black', marker = 'o',
           s = 50, zorder = 10)
ax2.scatter(1, mean_5dpf_1um, color = 'black', marker = 'o',
            s = 50, zorder = 10)
ax1.set_ylim(0,250)
ax1.spines['right'].set_visible(False)
ax1.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax1.set_title("4dpf")
ax2.set_title("5dpf")
ax1.set_ylabel("aberrant counts")
#plt.savefig("/Users/miramota/Desktop/Graphs/Figure_Outputs/astrocyte_counts.pdf", format= 'pdf')
plt.show()

# make numpy array for stats
astro_4dpf_dmso = astro_4dpf[astro_4dpf['condition'] == 0]['cell_count'].to_numpy()
astro_4dpf_1um = astro_4dpf[astro_4dpf['condition'] == 1]['cell_count'].to_numpy()
mean_4dpf_dmso= np.mean(astro_4dpf_dmso)
mean_4dpf_1um = np.mean(astro_4dpf_1um)

tstat_4dpf, pvalue_4dpf = stats.ttest_ind(astro_4dpf_dmso, astro_4dpf_1um, equal_var= True)
print(f't-statistic: {tstat_4dpf}, p-value: {pvalue_4dpf}')

astro_5dpf_dmso = astro_5dpf[astro_5dpf['condition'] == 0]['cell_count'].to_numpy()
astro_5dpf_1um = astro_5dpf[astro_5dpf['condition'] == 1]['cell_count'].to_numpy()
mean_5dpf_dmso = np.mean(astro_5dpf_dmso)
mean_5dpf_1um = np.mean(astro_5dpf_1um)

tstat_5dpf, pvalue_5dpf = stats.ttest_ind(astro_5dpf_dmso, astro_5dpf_1um, equal_var= True)
print(f't-statistic: {tstat_5dpf}, p-value: {pvalue_5dpf}')

