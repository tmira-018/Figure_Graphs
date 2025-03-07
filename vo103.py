import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np
from scipy import stats
import scikit_posthocs as sp

# Plot vo103

# Load the data from the excel file
mutant_df = pd.read_excel("DataSheets/vo103_mbpnlscaax_24.xlsx",
                       sheet_name = 'combined')
 
# Edit the dataframe to include only 5dpf data
mutant_5dpf = mutant_df[mutant_df['dpf']== 5]

# Exclude the WIN05μM condition
mutant_5dpf_01 = mutant_5dpf[mutant_5dpf['condition'] != 'WIN05μM']

f, ax = plt.subplots()
'''sns.barplot(data= mutant_5dpf_2, x = 'condition', y = 'aberrant',
            hue = 'genotype', hue_order= ['wt', 'het', 'mut'],
            palette = ["#97EAD2","#FECEE9", "#A63A50"],
            errorbar = ('se', 1),
            capsize = .2 )'''

sns.swarmplot(data = mutant_5dpf_2, x = 'condition', y = 'aberrant',
              hue= 'genotype',
              dodge = True,
              hue_order=['wt', 'het', 'mut'],
              palette = ["#095256","#6DD6DA", "#6588D4"],
              legend= False)

sns.boxplot(data = mutant_5dpf_2, x = 'condition', y = 'aberrant',
            hue = 'genotype', hue_order = ['wt', 'het', 'mut'],
            fill = False, widths= 0.25,
            palette = ['black', 'black', 'black'],
            legend = False, linewidth= 0.75)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.savefig('Figure_Outputs/vo103_aberrant.pdf', format='pdf')
plt.show()

def test_normality(data, condition, column='aberrant'):
    """
    Perform Shapiro-Wilk test and create Q-Q plot for normality check
    
    Parameters:
    data: pandas DataFrame
    condition: string or integer of the condition variable
    column: string, name of column to test
    """
    data_condition = data[data['condition'] == condition]
    data_condition.dropna(subset= [column])

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

test_normality(mutant_5dpf_01, 'DMSO')
test_normality(mutant_5dpf_01, 'WIN1μM')

#Seperate conditions
def cond_types(dataframe, condition, column):
    data_condition = dataframe[dataframe[column] == condition]
    return data_condition

# Seperateing data by condition
DMSO_5dpf = cond_types(mutant_5dpf_01, 'DMSO', 'condition')
dmso_5_array = DMSO_5dpf['aberrant'].to_numpy()
win1_5dpf = cond_types(mutant_5dpf_01, 'WIN1μM', 'condition')
win1_wt = cond_types(win1_5dpf, 'wt', 'genotype')
win1_het = cond_types(win1_5dpf, 'het', 'genotype')
win1_mut = cond_types(win1_5dpf, 'mut', 'genotype')
win1_wt_array = win1_wt['aberrant'].to_numpy()
win1_het_array = win1_het['aberrant'].to_numpy()
win1_mut_array = win1_mut['aberrant'].to_numpy()

H5 = stats.kruskal(win1_wt_array, win1_het_array, win1_mut_array)
print(H5)

# Post-hoc test 5 dpf
posthoc_results = sp.posthoc_dunn(win1_5dpf, val_col="aberrant", group_col="genotype", p_adjust="bonferroni")
print(posthoc_results)
