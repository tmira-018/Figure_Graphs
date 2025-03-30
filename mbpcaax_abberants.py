import os 
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import statsmodels.api as sm
import scikit_posthocs as sp

#import and edit data
#imports excel sheet with all the abberant counts
mbp4dpf_abb = pd.read_excel('DataSheets/abberant_counts.xlsx', 
                          sheet_name = '4dpf_combined')

#removes rows with non numeric values in the abberant_count column
mbp4dpf_abb = mbp4dpf_abb[pd.to_numeric(mbp4dpf_abb['abberant_count'], errors = 'coerce').notnull()]

mbp5dpf_abb = pd.read_excel('DataSheets/abberant_counts.xlsx',
                         sheet_name = '5dpf_combined')
mbp5dpf_long = mbp5dpf_abb.melt(var_name="Drug", value_name="Response")

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
    print(f"If p-value > 0.05: Data is normally distributed")
    print(f"If p-value < 0.05: Data is not normally distributed\n")
    
    return statistic, p_value, fig

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

# Example usage:
stat, p_val, fig = test_normality(mbp4dpf_abb, 'DMSO')
plt.show()
stat, p_val, fig = test_normality(mbp4dpf_abb, 0.5)
plt.show()
stat, p_val, fig = test_normality(mbp4dpf_abb, 1)
plt.show()

# Test for normality at 5 dpf
test_normality_wide(mbp5dpf_abb)

#Seperate conditions and find means and location
def cond_types(data, condition, column):
    """
    Seperate data by condition.

    Returns: 
    data_condition (pandas DataFrame),

    Parameters:
    data: pandas DataFrame
    condition: string or integer of the condition
    column: string, name of the colum to be seperated
    """
    data_condition = data[data[column] == condition]

    return data_condition

# Seperating data by condition and convert to numpy array
dmso_4dpf = cond_types(mbp4dpf_abb, 'DMSO', 'Condition')
dmso_4_array = cond_types(mbp4dpf_abb, 'DMSO', 'Condition')['abberant_count'].to_numpy()

win05_4dpf = cond_types(mbp4dpf_abb, 0.5, 'Condition')
win05_4_array = cond_types(mbp4dpf_abb, 0.5, 'Condition')['abberant_count'].to_numpy()

win1_4dpf = cond_types(mbp4dpf_abb, 1, 'Condition')
win1_4_array = cond_types(mbp4dpf_abb, 1, 'Condition')['abberant_count'].to_numpy()


# Medians
dmso_mean = DMSO_4dpf['abberant_count'].median()

win05_mean = win05_4dpf['abberant_count'].median()

win1_mean = win1_4dpf['abberant_count'].median()


dmso_5dpf = mbp5dpf_abb['DMSO'].to_numpy()
dmso_5dpf = dmso_5dpf[~np.isnan(dmso_5dpf)]
dmso_mean5 = dmso_5dpf.mean()
dmso_rep5 = 15

win05_5dpf = mbp5dpf_abb[0.5].to_numpy()
win05_5dpf = win05_5dpf[~np.isnan(win05_5dpf)]
win05_mean5 = win05_5dpf.mean()
win05_rep5 = 23

win1_5dpf = mbp5dpf_abb[1].to_numpy()
win1_5dpf = win1_5dpf[~np.isnan(win1_5dpf)]
win1_mean5 = win1_5dpf.mean()
win1_rep5 = 32

# Do Kruskal-Wallis test 4 dpf                                           
H4 = stats.kruskal(dmso_4_array, win05_4_array, win1_4_array)
print(H4)

H5 = stats.kruskal(dmso_5dpf, win05_5dpf, win1_5dpf)
print(H5)

# Post-hoc test 5 dpf
posthoc_results = sp.posthoc_dunn(mbp5dpf_long, val_col="Response", group_col="Drug", p_adjust="bonferroni")
print(posthoc_results)


#plot 4 and 5 dpf together 

fig, (ax1, ax2) = plt.subplots(1,2, sharey=True)
# Plot 4 dpf data 
sns.swarmplot(data = mbp4dpf_abb, x = 'Condition',
              y = 'abberant_count', hue = 'Condition',
              palette = ["#1768AC", "#420039", "#F72585"],
              ax= ax1)

sns.boxplot(data = mbp4dpf_abb, x = 'Condition',
           y = 'abberant_count', hue = 'Condition',
           fill = False, widths = 0.5,
           palette= ['black', 'black', 'black'],
           legend=False, linewidth=0.75, ax = ax1)
ax1.set_ylim(0,70)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.set_title('4 dpf')

# Plot 5 dpf data

sns.swarmplot(data= mbp5dpf_abb,
              palette = ["#1768AC", "#420039", "#F72585"], ax = ax2)

ax2.scatter(x = [0], y = [dmso_rep5], 
            color = 'red', s = 75, marker = 'o', zorder = 2)
ax2.scatter(x = [1], y = [win05_rep5],
            color = 'red', s = 75, marker= 'o', zorder = 2)
ax2.scatter(x = [2], y = [win1_rep5],
            color = 'black', s = 75, marker = 'o', zorder = 2)

sns.boxplot(data = mbp5dpf_abb, widths = 0.5, fill = False,  
            palette= ['black', 'black', 'black'], linewidth=0.75, ax = ax2)
ax2.set_ylim(0,70)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.set_title('5 dpf')
plt.savefig("Figure_Outputs/abberrant_count4-5dpf.pdf", format='pdf')
plt.show()
