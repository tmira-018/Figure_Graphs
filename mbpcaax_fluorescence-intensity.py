import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np
from scipy import stats

combined_4dpf_caax = pd.read_excel("DataSheets/combined_4dpf_mbpcaax.xlsx",
                         sheet_name = 'combined')
combined_5dpf_caax = pd.read_excel("DataSheets/combined_5dpf_mbpcaax.xlsx")

#remove 0.25 um DOSE from 4 dpf data
combined_4dpf_caax = combined_4dpf_caax[combined_4dpf_caax['DOSE'] != '0.25 uM']

f, (ax1, ax2) = plt.subplots(1,2, sharey= True)
sns.swarmplot(data = combined_4dpf_caax, x = 'DOSE', y = 'MEAN',
              hue= 'DOSE',
              dodge = False,
              order=['1% DMSO', '0.5 uM', '1 uM'],
              hue_order=['1% DMSO', '0.5 uM', '1 uM'],
              palette = ["#1768AC", "#420039", "#F72585"],
              legend= False, ax= ax1)

sns.boxplot(data = combined_4dpf_caax, x = 'DOSE',
           y = 'MEAN', hue = 'DOSE', 
           order=['1% DMSO', '0.5 uM', '1 uM'],
           fill = False, widths = 0.18,
           palette= ['black', 'black', 'black'],
           legend=False, linewidth=0.75, ax= ax1)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.scatter(['1% DMSO', '0.5 uM', '1 uM'], [8187.889, 8070.632, 8166.594],
            color = 'orange', s = 30,
            edgecolor = 'black', zorder = 10)
ax1.set_ylim(0, 22000)
ax1.set_yticks(np.arange(0,22000,2500))
ax1.set_title('Fluorescence Intensity 4 dpf')

sns.swarmplot(data = combined_5dpf_caax, x = 'DOSE', y = 'MEAN',
              hue= 'DOSE',
              dodge = False,
              order=['1% DMSO', '0.5 uM', '1.0 uM'],
              hue_order=['1% DMSO', '0.5 uM', '1.0 uM'],
              palette = ["#1768AC", "#420039", "#F72585"],
              legend= False, ax = ax2)

sns.boxplot(data = combined_5dpf_caax, x = 'DOSE',
           y = 'MEAN', hue = 'DOSE', 
           order=['1% DMSO', '0.5 uM', '1.0 uM'],
           fill = False, widths = 0.18,
           palette= ['black', 'black', 'black'],
           legend=False, linewidth=0.75, ax= ax2)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.scatter(['1% DMSO', '0.5 uM', '1.0 uM'], [11627.546, 12097.077, 11936.248],
            color = 'orange', s = 30,
            edgecolor = 'black', zorder = 10)
ax2.set_title('Fluorescence Intensity 5 dpf')
plt.savefig('Figure_Outputs/4-5dpf_mbpcaax_fluor-int.pdf', format='pdf')
plt.show()

dose_groups_4dpf = [combined_4dpf_caax[combined_4dpf_caax['DOSE'] == '1% DMSO']['MEAN'],
               combined_4dpf_caax[combined_4dpf_caax['DOSE'] == '0.5 uM']['MEAN'],
               combined_4dpf_caax[combined_4dpf_caax['DOSE'] == '1 uM']['MEAN'],]

H_stat, p_value = stats.kruskal(*dose_groups_4dpf)
print(f"Kruskal-Wallis Test: H = {H_stat}, p = {p_value}")

dose_groups_5dpf = [combined_5dpf_caax[combined_5dpf_caax['DOSE'] == '1% DMSO']['MEAN'],
                combined_5dpf_caax[combined_5dpf_caax['DOSE'] == '0.5 uM']['MEAN'],
                combined_5dpf_caax[combined_5dpf_caax['DOSE'] == '1.0 uM']['MEAN']]
H_stat5, p_value5 = stats.kruskal(*dose_groups_5dpf)
print(f"Kruskal-Wallis Test: H = {H_stat5}, p = {p_value5}")