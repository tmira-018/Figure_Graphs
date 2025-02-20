import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np
from scipy import stats
from scikit_posthocs import posthoc_dunn

# Import data 
nls_4dpf = pd.read_excel('/Users/miramota/OHSU Dropbox/Tania Miramontes/Data_sheets/WIN_mbp-nls_4dpf.xlsx',
                         sheet_name= 'combined_spinal')
nls_5dpf = pd.read_excel('/Users/miramota/OHSU Dropbox/Tania Miramontes/Data_sheets/WIN_mbp-nls_5dpf.xlsx',
                         sheet_name= 'combined_spinal')

def test_normality_wide(data, column):
    """
    Perform Shapiro-Wilk test and plot histogram on dataframe that is 
    wide format.
    
    Parameters:
    data: pandas DataFrame
    column: string, name of column to test
    """
    data_analysis = data[column].dropna()

    # Perform Shapiro-Wilk test
    statistic, p_value = stats.shapiro(data_analysis)
    
    # Create figure with two subplots
    fig, (ax1) = plt.subplots(1, figsize=(12, 5))
    
    # Histogram with density plot
    sns.histplot(data=data_analysis, kde=True,ax=ax1) 
    ax1.set_title('Distribution of Abberant Count')
    
    plt.tight_layout()
    
    print(f"Shapiro-Wilk test results:")
    print(f"Statistic: {statistic:.4f}")
    print(f"P-value: {p_value:.4f}")
    print(f"\nIf p-value > 0.05: Data is normally distributed")
    print(f"If p-value < 0.05: Data is not normally distributed")
    
    return statistic, p_value, fig

# Usage 4dpf
stat, p_val, fig = test_normality_wide(nls_4dpf, 'DMSO')
plt.show()
stat, p_val, fig = test_normality_wide(nls_4dpf, '0.5 um')
plt.show()
stat, p_val, fig = test_normality_wide(nls_4dpf, '1.0 um')
plt.show()

# Usage 5dpf
stat, p_val, fig = test_normality_wide(nls_5dpf, 'DMSO')
plt.show()
stat, p_val, fig = test_normality_wide(nls_5dpf, '0.5 um')
plt.show()
stat, p_val, fig = test_normality_wide(nls_5dpf, '1.0 um')
plt.show()

# make 5dpf dataframe long version
nls5dpf_long = nls_5dpf.melt(var_name="Drug", value_name="Response")
nls5dpf_long = nls5dpf_long.dropna()

# Perform Kruskal-Wallis test
H_stat, p_value = stats.kruskal(nls_4dpf['DMSO'].dropna(), 
                                nls_4dpf['0.5 um'], 
                                nls_4dpf['1.0 um'])
print(f"Kruskal-Wallis Test: H = {H_stat}, p = {p_value}")

H_stat5, p_val5 = stats.kruskal(nls_5dpf['DMSO'].dropna(),
                                nls_5dpf['0.5 um'],
                                nls_5dpf['1.0 um'].dropna())
print(f"Kruskal-Wallis Test: H = {H_stat5}, p = {p_val5}")

# Perform Dunn's test post hoc
nls_posthoc_5results = sp.posthoc_dunn(nls5dpf_long, val_col="Response", group_col="Drug", p_adjust="bonferroni")
print(nls_posthoc_5results)


# Plot mbpnls
fig, (ax1,ax2) = plt.subplots(1,2, sharey=True)
sns.boxplot(data = nls_4dpf,
            fill = False, widths = 0.25, linewidth= 0.75,
            palette= ['black', 'black', 'black'], ax=ax1)
sns.swarmplot(data = nls_4dpf,
              palette = ["#1768AC", "#F72585", "#420039"],
              legend = False, ax=ax1)
sns.boxplot(data = nls_5dpf, 
            fill = False, widths = 0.25, linewidth= 0.75,
            palette = ['black', 'black', 'black'], ax=ax2)
sns.swarmplot(data = nls_5dpf, 
              palette = ["#1768AC", "#F72585", "#420039"],
              legend = False, ax=ax2)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False) 
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False) 
plt.yticks(np.arange(0, 250, 50))  
ax2.legend(loc = 'upper right')
plt.savefig("/Users/miramota/Desktop/Figures/mbp_nls/mbpnls-45graph.pdf", format='pdf')
plt.show()
