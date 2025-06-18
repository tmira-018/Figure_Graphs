import os
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np
from scipy import stats
from scikit_posthocs import posthoc_dunn


em_df = pd.read_excel("/Users/miramota/OHSU Dropbox/Tania Miramontes/Data_sheets/EM_axoncounts.xlsx", 
                    sheet_name = "combined")

ventral_dmso = em_df[em_df['cond'] == 0]['ventral'].dropna()
dorsal_dmso = em_df[em_df['cond']== 0]['dorsal'].dropna()

ventral_win = em_df[em_df['cond'] ==1]['ventral'].dropna()
dorsal_win = em_df[em_df['cond'] == 1]['dorsal'].dropna()

fig, (ax1, ax2) = plt.subplots(1,2, sharey=True)
sns.boxplot(data = em_df,
            x = "cond", y= "dorsal", hue = "cond",
            ax= ax1, fill=False, legend=False, 
            palette = ['black', 'black'], linewidth = 0.75)
sns.scatterplot(data= em_df,
                x= "cond", y= "dorsal", hue = "cond",
                ax= ax1, legend=False,
                palette = ["#1768AC", "#F72585"])
sns.boxplot(data= em_df,
            x= "cond", y= "ventral", hue = "cond",
            ax=ax2, fill=False, legend=False, 
            palette = ['black', 'black'], linewidth= 0.75)
sns.scatterplot(data= em_df,
                x= "cond", y= "ventral", hue = "cond",
                ax=ax2, palette = ["#1768AC", "#F72585"])
ax1.set_ylim(0,38)
ax1.spines['right'].set_visible(False)
ax1.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax1.set_title("Dorsal Spinal Cord")
ax2.set_title("Ventral Spinal Cord")
ax1.set_ylabel("Axon Count")
plt.savefig("/Users/miramota/Desktop/Graphs/Figure_Outputs/axon_counts.pdf", format= 'pdf')

dmso_t_stat, dmso_p_value = stats.ttest_ind(ventral_dmso, ventral_win)
print("Independent two-sample t-test:", dmso_t_stat, dmso_p_value)

win_t_stat, win_p_value = stats.ttest_ind(dorsal_dmso, dorsal_win)
print("ind t-test dorsal:", win_t_stat, win_p_value)