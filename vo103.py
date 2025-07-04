import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np
from scipy import stats
import scikit_posthocs as sp
import statsmodels.api as sm 
from statsmodels.formula.api import ols 
from statsmodels.stats.multitest import multipletests
from statsmodels.stats.multicomp import pairwise_tukeyhsd

# Plot vo103

# Load the data from the excel file
mutant_df = pd.read_excel("DataSheets/vo103_mbpnlscaax_24.xlsx",
                       sheet_name = 'combined')
 
# Edit the dataframe to include only 5dpf data
mutant_5dpf = mutant_df[mutant_df['dpf']== 5]


# Exclude the WIN05μM condition
mutant_5dpf_01 = mutant_5dpf[mutant_5dpf['condition'] != 'WIN05μM']
mutant_5dpf_01 = mutant_5dpf_01.dropna()
# Separate data by  

# Plotting aberrant data
f, ax = plt.subplots()
sns.swarmplot(data = mutant_5dpf_01, x = 'genotype', y = 'aberrant',
              hue= 'condition',
              dodge = True,
              order=['wt', 'het', 'mut'],
              #hue_order=['wt', 'het', 'mut'],
              palette = ["#1768AC", "#F72585"],
              legend= True)

sns.boxplot(data = mutant_5dpf_01, x = 'genotype',
           y = 'aberrant', hue = 'condition', 
           order=['wt', 'het', 'mut'],
           fill = False, widths = 0.18,
           palette= ['black', 'black'],
           legend=False, linewidth=0.75)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.savefig('Figure_Outputs/vo103_aberrant_genotyped.pdf', format='pdf')
plt.show()

# Plotting nls counts 

f, ax = plt.subplots()
sns.swarmplot(data = mutant_5dpf_01,  x = 'genotype', y = 'nls',
              hue = 'condition',
              dodge = True,
              order = ['wt', 'het', 'mut'],
              palette = ["#1768AC", "#F72585"],
              legend= True)
sns.boxplot(data = mutant_5dpf_01, x = 'genotype', y = 'nls',
            hue= 'condition',
            order = ['wt', 'het', 'mut'],
            fill = False, widths = 0.18,
            palette= ['black', 'black'],
            legend = False, linewidth=0.75)
ax.set_ylim(0,50)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.savefig('Figure_Outputs/vo103_nlscounts.pdf', format = "pdf")
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



#drop nan values in the aberrant column
mutant_5dpf_02 = mutant_5dpf_01.dropna(subset=['aberrant'])
# Do two-way ANOVA
model = ols( 
    'aberrant ~ C(genotype) + C(condition) + C(genotype):C(condition)', 
    data=mutant_5dpf_02).fit() 
result = sm.stats.anova_lm(model, typ=2) 
print(result)


tukey = pairwise_tukeyhsd(mutant_5dpf_02['aberrant'], 
                          mutant_5dpf_02['genotype'] + mutant_5dpf_02['condition'])
print(tukey)

# nls
mutant_5dpf_nls = mutant_5dpf_01.dropna(subset=['nls'])
# Do two-way ANOVA
nls_model = ols( 
    'nls ~ C(genotype) + C(condition) + C(genotype):C(condition)', 
    data=mutant_5dpf_nls).fit() 
result = sm.stats.anova_lm(nls_model, typ=2) 
print(result)

nls_tukey = pairwise_tukeyhsd(mutant_5dpf_nls['nls'], 
                          mutant_5dpf_nls['genotype'] + mutant_5dpf_nls['condition'])
print(nls_tukey)

nls_tukey = sp.posthoc_tukey(mutant_5dpf_nls, val_col= 'nls',
                             group_col= 'condition')
print(nls_tukey)


def cond_gen_types(data, condition, cond_column, genotype, gen_column):
    """
    Seperate data by condition.

    Returns: 
    data_condition (pandas DataFrame),

    Parameters:
    data: pandas DataFrame
    condition: string or integer of the condition
    column: string, name of the colum to be seperated
    """
    data_condition = data[data[cond_column] == condition]
    gen_df = data_condition[data_condition[gen_column] == genotype]

    return gen_df


dmso_wt = cond_gen_types(mutant_5dpf_nls, 'DMSO', 'condition', 'wt', 'genotype')
dmso_het = cond_gen_types(mutant_5dpf_nls, 'DMSO', 'condition', 'het', 'genotype')
dmso_mut = cond_gen_types(mutant_5dpf_nls, 'DMSO', 'condition', 'mut', 'genotype')

wt = cond_gen_types(mutant_5dpf_nls, 'wt', 'genotype')

wt_nls_tukey = sp.posthoc_tukey(mutant_5dpf_nls, val_col = 'nls', group_col = 'genotype')
print(wt_nls_tukey)

#run t-test
dmso_wt_nls = dmso_wt['nls'].to_numpy()
win_wt_nls = win_wt['nls'].to_numpy()
t_stat, p_value = stats.ttest_ind(dmso_wt_nls, win_wt_nls)
print(f"t-statistic: {t_stat}, p-value: {p_value}")

dmso_mut_nls  = dmso_mut['nls'].to_numpy()
win_mut_nls = win_mut['nls'].to_numpy()
t_stat, p_value = stats.ttest_ind(dmso_mut_nls, win_mut_nls)
print(f"t-statistic: {t_stat}, p-value: {p_value}")

win_wt = cond_gen_types(mutant_5dpf_nls, 'WIN1μM', 'condition', 'wt', 'genotype')
win_het = cond_gen_types(mutant_5dpf_nls, 'WIN1μM', 'condition', 'het', 'genotype')
win_mut = cond_gen_types(mutant_5dpf_nls, 'WIN1μM', 'condition', 'mut', 'genotype')

