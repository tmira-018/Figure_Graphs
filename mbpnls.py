import os
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np
from scipy import stats


# Import data 
nls_4dpf = pd.read_excel('/Graphs/DataSheets/WIN_mbp-nls_4dpf.xlsx',
                         sheet_name= 'combined_spinal')
#drop 0.5 um 
nls_4dpf_filtered = nls_4dpf.drop(columns=['0.5 um'])

nls_5dpf = pd.read_excel('/Graphs/DataSheets/WIN_mbp-nls_5dpf.xlsx',
                         sheet_name= 'combined_spinal')
nls_5dpf_filtered = nls_5dpf.drop(columns = ['0.5 um'])


def test_normality_wide(data):
    """
    Perform Shapiro-Wilk test and plot histogram on dataframe that is in a 
    wide format. Will loop through all columns in the dataframe.
    
    Parameters:
    data: pandas DataFrame
    column: string, name of column to test
    """
    # Loop through all the  columns
    for column in data.columns:
        data_col = data[column].dropna()

        # Perform Shapiro-Wilk test
        statistic, p_value = stats.shapiro(data_col)
        
        # Create figure with two subplots
        fig, (ax1) = plt.subplots(1, figsize=(12, 5))
    
        # Histogram with density plot
        sns.histplot(data=data_col, kde=True,ax=ax1) 
        ax1.set_title('Distribution of Abberant Count')
    
        plt.tight_layout()
        
        print(f"Shapiro-Wilk test results for {column}:")
        print(f"Statistic: {statistic:.4f}")
        print(f"P-value: {p_value:.4f}")
        print(f"If p-value > 0.05: Data is normally distributed")
        print(f"If p-value < 0.05: Data is not normally distributed\n")
    
    return statistic, p_value, fig

# Usage 4dpf
#test_normality_wide(nls_4dpf)

# Usage 5dpf
#test_normality_wide(nls_5dpf)


# Plot mbpnls for 4 and 5 dpf side by side 
fig, (ax1,ax2) = plt.subplots(1,2, sharey=True, figsize = (6.5,6))
sns.boxplot(data = nls_4dpf_filtered,
            fill = False, widths = 0.3, linewidth= 0.9,
            palette= ['black', 'black'], ax=ax1)
sns.swarmplot(data = nls_4dpf_filtered,
              palette = ["#1768AC", "#F72585"],
              legend = False, ax=ax1)
ax1.scatter(['DMSO', '1.0 um'], [126, 119], color= 'orange',
            edgecolor = 'black', marker = 'o', s = 30, zorder = 10) 
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.set_title('4 dpf')
sns.boxplot(data = nls_5dpf_filtered, 
            fill = False, widths = 0.3, linewidth= 0.9,
            palette = ['black', 'black'], ax=ax2)
sns.swarmplot(data = nls_5dpf_filtered, 
              palette = ["#1768AC", "#F72585"],
              legend = False, ax=ax2)
ax2.scatter(['DMSO', '1.0 um'], [153, 137], color = 'orange',
            edgecolor = 'black', marker = 'o', s = 30, zorder = 10 )
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)  
ax2.legend(loc = 'upper right')
ax2.set_title('5 dpf')
plt.yticks(np.arange(0, 250, 50)) 
fig.suptitle('Number of OL Nuclei')
#plt.savefig('Figure_Outputs/mbpnls-45graph_v2.pdf', format='pdf')
plt.show()

# Perform t test for nls data DMSO and WIN 1.0 um
t_stat_4dpf, p_value_4dpf = stats.ttest_ind(nls_4dpf_filtered['DMSO'].dropna(), 
                                            nls_4dpf_filtered['1.0 um'].dropna()
                                            , equal_var=False)
print(f"4 dpf t-test: t = {t_stat_4dpf}, pvalue = {p_value_4dpf}")

t_stat_5dpf, p_value_5dpf = stats.ttest_ind(nls_5dpf_filtered['DMSO'].dropna(),
                                            nls_5dpf_filtered['1.0 um'].dropna(),
                                                              equal_var = False)
print(f"5 dpf t-test: t = {t_stat_5dpf}, pvalue = {p_value_5dpf}")


# Plot mbpnls just at 5 dpf in a 4x6 figure
# This was used for the manuscript figure
fig, ax = plt.subplots(figsize=(4, 6))
ax  = sns.boxplot(data = nls_5dpf_filtered,
           fill= False,
           palette = ['black', 'black'], widths = 0.4,
           linewidth = 0.9, legend= False)
ax = sns.swarmplot(data = nls_5dpf_filtered,
                 s = 10,
                palette = ["#1768AC", "#F72585"],
              legend = True)
ax.scatter([0, 1], [153, 137], color = 'orange',
            edgecolor = 'black', marker = 'o', s = 75, zorder = 10)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.yticks(np.arange(0, 225, 25))
fig.suptitle('Number of OL Nuclei 5 dpf')
#plt.savefig('Figure_Outputs/mbpnls_5dpf_4x6.pdf', format = 'pdf')
plt.show()