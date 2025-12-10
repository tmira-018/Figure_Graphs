import os
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np
from scipy import stats
from scikit_posthocs import posthoc_dunn

# Import EM data 
em_df = pd.read_excel("/Graphs/Data_sheets/EM_axoncounts.xlsx", 
                    sheet_name = "combined")

ventral_dmso = em_df[em_df['cond'] == 0]['ventral'].dropna()
dorsal_dmso = em_df[em_df['cond']== 0]['dorsal'].dropna()

ventral_win = em_df[em_df['cond'] ==1]['ventral'].dropna()
dorsal_win = em_df[em_df['cond'] == 1]['dorsal'].dropna()

def em_axon(dataframe, saving_path = None):
    fig, (ax1, ax2) = plt.subplots(1,2, sharey=True, figsize = (8, 6))
    sns.boxplot(data = dataframe,
                x = "cond", y= "dorsal", hue = "cond",
                widths = 0.8,
                ax= ax1, fill=False, legend=False, 
                palette = ['black', 'black'], linewidth = 0.9)
    sns.swarmplot(data= dataframe,
                    x= "cond", y= "dorsal", hue = "cond",
                    ax= ax1, legend=False, s = 10,
                    palette = ["#1768AC", "#F72585"])
    sns.boxplot(data= dataframe,
                x= "cond", y= "ventral", hue = "cond",
                widths = 0.8,
                ax=ax2, fill=False, legend=False, 
                palette = ['black', 'black'], linewidth= 0.9)
    sns.swarmplot(data= dataframe,
                    x= "cond", y= "ventral", hue = "cond", s = 10,
                    ax=ax2, palette = ["#1768AC", "#F72585"])
    ax1.set_ylim(0,38)
    ax1.spines['right'].set_visible(False)
    ax1.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    ax1.set_title("Dorsal Spinal Cord")
    ax2.set_title("Ventral Spinal Cord")
    ax1.set_ylabel("Axon Count")
    if saving_path is not None:
        plt.savefig(saving_path, format = 'pdf')
    else:
        plt.show()
    return plt.gcf()

em_axon(em_df, saving_path='Figure_Outputs/em_test.pdf')

ventral_t_stat, ventral_p_value = stats.ttest_ind(ventral_dmso, ventral_win)
print(f"Independent two-sample t-test: t_stat = {ventral_t_stat}, p_value = {ventral_p_value}")

dorsal_t_stat, dorsal_p_value = stats.ttest_ind(dorsal_dmso, dorsal_win)
print(f"ind t-test dorsal: t_stat = {dorsal_t_stat}, p_value = {dorsal_p_value}")