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


def aberrants_vo103(dataframe, analysis_col, 
                    y_lim = None, saving_path = None):
    """
    creates plot across genotypes
    dataframe = pandas dataframe
    analysis_col = column name of data to be plotted (y axis)
    saving_path = path where to save figure"""
# Plotting aberrant data
    f, ax = plt.subplots()
    sns.swarmplot(data = dataframe, x = 'genotype', y = analysis_col,
                hue= 'condition',
                dodge = True,
                order=['wt', 'het', 'mut'],
                #hue_order=['wt', 'het', 'mut'],
                palette = ["#1768AC", "#F72585"],
                legend= True)

    sns.boxplot(data = dataframe, x = 'genotype',
            y = analysis_col, hue = 'condition', 
            order=['wt', 'het', 'mut'],
            fill = False, widths = 0.18,
            palette= ['black', 'black'],
            legend=False, linewidth=0.75)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_ylim(y_lim)
    if saving_path is not None:
        plt.savefig(saving_path, format = "pdf")
    else:
        plt.show()
    plt.tight_layout()
    return plt.gcf()


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

# nls
mutant_5dpf_nls = mutant_5dpf_01.dropna(subset=['nls'])


def cond_gen_types(data, condition, cond_column, genotype, gen_column):
    """
    Seperate data by condition.

    Returns: 
    data_condition (pandas DataFrame),

    Parameters:
    data: pandas DataFrame
    condition: string or integer of the condition
    cond_column: string, name of the colum to be seperated
    genotype: string of the genotype to be filtered
    gen_column: string, name of the column with genotype information
    """
    data_condition = data[data[cond_column] == condition]
    gen_df = data_condition[data_condition[gen_column] == genotype]

    return gen_df

# Plot aberrant counts and nls counts
aberrants_vo103(mutant_5dpf_01, 'aberrant', saving_path= 'Figure_Outputs/vo103tests.pdf')
aberrants_vo103(mutant_5dpf_01, 'nls', 
                y_lim = (0,60), 
                saving_path= 'Figure_Outputs/vo103_nlstests.pdf')

# filtering data by condition and genotype
#DMSO
dmso_wt = cond_gen_types(mutant_5dpf_nls, 'DMSO', 'condition', 'wt', 'genotype')
dmso_het = cond_gen_types(mutant_5dpf_nls, 'DMSO', 'condition', 'het', 'genotype')
dmso_mut = cond_gen_types(mutant_5dpf_nls, 'DMSO', 'condition', 'mut', 'genotype')
# WIN 1uM
win_wt = cond_gen_types(mutant_5dpf_nls, 'WIN1μM', 'condition', 'wt', 'genotype')
win_het = cond_gen_types(mutant_5dpf_nls, 'WIN1μM', 'condition', 'het', 'genotype')
win_mut = cond_gen_types(mutant_5dpf_nls, 'WIN1μM', 'condition', 'mut', 'genotype')

# run t-test on aberrant counts 
dmso_wt_abb = dmso_wt['aberrant'].to_numpy()
win_wt_abb = win_wt['aberrant'].to_numpy()
t_stat, p_value = stats.ttest_ind(dmso_wt_abb, win_wt_abb)
print(f"t-statistic: {t_stat}, p-value: {p_value}")

dmso_het_abb = dmso_het['aberrant'].to_numpy()
win_het_abb = win_het['aberrant'].to_numpy()
t_stat_het, p_value_het = stats.ttest_ind(dmso_het_abb, win_het_abb)
print(f't-stat(het): {t_stat_het}, p_value(het): {p_value_het}')

dmso_mut_abb  = dmso_mut['aberrant'].to_numpy()
win_mut_abb = win_mut['aberrant'].to_numpy()
t_stat, p_value = stats.ttest_ind(dmso_mut_abb, win_mut_abb)
print(f"t-statistic: {t_stat}, p-value: {p_value}")


aberrant_model = ols('aberrant ~ C(genotype) * C(condition)', data=mutant_5dpf_01).fit()
anova_table = sm.stats.anova_lm(aberrant_model, typ=2)  # Type II ANOVA
print(anova_table)


aberrant_tukey = pairwise_tukeyhsd(endog=mutant_5dpf_01['aberrant'],
                          groups=mutant_5dpf_01['genotype'].astype(str) + "_" + 
                          mutant_5dpf_01['condition'].astype(str),
                          alpha=0.05)
print(aberrant_tukey)

#run t-test on nls counts 
dmso_wt_nls = dmso_wt['nls'].to_numpy()
win_wt_nls = win_wt['nls'].to_numpy()
t_stat, p_value = stats.ttest_ind(dmso_wt_nls, win_wt_nls)
print(f"t-statistic: {t_stat}, p-value: {p_value}")

dmso_het_nls = dmso_het['nls'].to_numpy()
win_het_nls = win_het['nls' ].to_numpy()
t_stat_het, p_value_het = stats.ttest_ind(dmso_het_nls, win_het_nls)
print(f't-stat(het): {t_stat_het}, p_value(het): {p_value_het}')

dmso_mut_nls  = dmso_mut['nls'].to_numpy()
win_mut_nls = win_mut['nls'].to_numpy()
t_stat, p_value = stats.ttest_ind(dmso_mut_nls, win_mut_nls)
print(f"t-statistic: {t_stat}, p-value: {p_value}")

nls_model = ols('nls ~ C(genotype) * C(condition)', data=mutant_5dpf_01).fit()
nls_anova_table = sm.stats.anova_lm(nls_model, typ=2)  # Type II ANOVA
print(nls_anova_table)
