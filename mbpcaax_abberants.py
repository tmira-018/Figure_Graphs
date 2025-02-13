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



# palette=["#1768AC", "#F72585", "#420039"]

# plot 4 dpf data 
sns.swarmplot(data = mbp_abb_4dpf, x = 'Condition',
              y = 'abberant_count', hue = 'Condition',
              palette = ["#1768AC", "#F72585", "#420039"],
                )


