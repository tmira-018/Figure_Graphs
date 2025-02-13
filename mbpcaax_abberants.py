import os 
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import statsmodels.api as sm

#import and edit data
#imports excel sheet with all the abberant counts
mbp4dpf_abb = pd.read_excel('/Users/miramota/OHSU Dropbox/Tania Miramontes/Data_sheets/abberant_counts.xlsx', 
                          sheet_name = '4dpf_combined')

#removes rows with non numeric values in the abberant_count column
mbp_abb_4dpf = mbp4dpf_abb[pd.to_numeric(mbp4dpf_abb['abberant_count'], errors = 'coerce').notnull()]

mbp5dpf_abb = pd.read_excel('/Users/miramota/OHSU Dropbox/Tania Miramontes/Data_sheets/abberant_counts.xlsx',
                         sheet_name = '5dpf_combined')

#Check normality of data

def test_normality(data, condition, column='abberant_count'):
    """
    Perform Shapiro-Wilk test and create Q-Q plot for normality check
    
    Parameters:
    data: pandas DataFrame
    condition: string or integer of the condition variable
    column: string, name of column to test
    """
    data_condition = data[data['Condition'] == condition]

    # Perform Shapiro-Wilk test
    statistic, p_value = stats.shapiro(data_condition[column])
    
    # Create figure with two subplots
    fig, (ax1) = plt.subplots(1, figsize=(12, 5))
    
    # Histogram with density plot
    sns.histplot(data=data_condition, x=column, kde=True, ax=ax1)
    ax1.set_title('Distribution of Abberant Count')
    
    plt.tight_layout()
    
    print(f"Shapiro-Wilk test results:")
    print(f"Statistic: {statistic:.4f}")
    print(f"P-value: {p_value:.4f}")
    print(f"\nIf p-value > 0.05: Data is normally distributed")
    print(f"If p-value < 0.05: Data is not normally distributed")
    
    return statistic, p_value, fig

# Example usage:
stat, p_val, fig = test_normality(mbp_abb_4dpf, 'DMSO')
plt.show()
stat, p_val, fig = test_normality(mbp_abb_4dpf, 0.5)
plt.show()
stat, p_val, fig = test_normality(mbp_abb_4dpf, 1)
plt.show()

#Seperate conditions
def cond_types(data, condition, column):
    data_condition = data[data[column] == condition]
    return data_condition

# Seperateing data by condition
DMSO_4dpf = cond_types(mbp_abb_4dpf, 'DMSO', 'Condition')
win05_4dpf = cond_types(mbp_abb_4dpf, 0.5, 'Condition')
win1_4dpf = cond_types(mbp_abb_4dpf, 1, 'Condition')

dmso_5dpf = mbp5dpf_abb['DMSO'].dropna()
win05_5dpf = mbp5dpf_abb[0.5].dropna()
win1_5dpf = mbp5dpf_abb[1].dropna()

#means 
dmso_mean = DMSO_4dpf['abberant_count'].mean()
win05_mean = win05_4dpf['abberant_count'].mean()
win1_mean = win1_4dpf['abberant_count'].mean()

dmso_mean5 = dmso_5dpf['abberant_count'].mean()
win05_mean5 = win05_5dpf['abberant_count'].mean()
win1_mean5 = win1_5dpf['abberant_count'].mean()

#plot 4 and 5 dpf together 

fig, (ax1, ax2) = plt.subplots(1,2, sharey=True)
# plot 4 dpf data 
sns.swarmplot(data = mbp_abb_4dpf, x = 'Condition',
              y = 'abberant_count', hue = 'Condition',
              palette = ["#1768AC", "#F72585", "#420039"],
              ax= ax1)
sns.boxplot(data = mbp_abb_4dpf, x = 'Condition',
           y = 'abberant_count', hue = 'Condition',
           fill = False, widths = 0.25,
           palette= ['black', 'black', 'black'],
           legend=False, linewidth=0.75, ax = ax1)
ax1.set_ylim(0,70)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.set_title('4 dpf')

#plot 5 dpf data

sns.swarmplot(data= mbp5dpf_abb,
              palette = ["#1768AC", "#F72585", "#420039"], ax = ax2)
sns.boxplot(data = mbp5dpf_abb, fill = False, widths = 0.25, 
            palette= ['black', 'black', 'black'], linewidth=0.75, ax = ax2)
ax2.set_ylim(0,70)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.set_title('5 dpf')

