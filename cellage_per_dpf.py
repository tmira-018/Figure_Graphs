

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import pairwise_tukeyhsd

# Load data, this is the dataframe with fish age accounted for only
path = ('/Users/miramota/Desktop/Graphs/DataSheets/ol_single_cell_oldanalysis.xlsx')
fishage_df = pd.read_excel(path)

# Load data, this is the original dataframe with cell age 
path2 = ('/Users/miramota/Desktop/Graphs/DataSheets/WIN_single_cell.xlsx')
cellage_df = pd.read_excel(path2)
cellage_df = cellage_df[cellage_df.cond != 0.5]

# Count how many times each cell_ID appears in the dataframe
cell_repeats = cellage_df['cell_ID'].value_counts()
cell_repeats_fa = fishage_df['cell_ID'].value_counts()


comparison = (
    pd.concat([cell_repeats, cell_repeats_fa], axis=1, 
              keys=['cellage1', 'cellage2'])
    .fillna(0)
    .astype(int)
)

# get only the IDs where counts don't match
mismatch_ids = comparison[comparison['cellage1'] != comparison['cellage2']].index.tolist()

print(mismatch_ids)


# Merge the dataframes to include both cell age and fish age into
# one dataframe making sure that fish_ID, cell_ID, no_sheaths,
# total_output and avg_sheath_len are matching in both dataframes before merging 
# because data on the two different df are not the same
match_col = ['fish_ID', 'cell_ID', 'no_sheaths', 
             'total_output', 'avg_sheath_len']

fishage_df2 = fishage_df.merge(
    cellage_df[match_col + ["cell_age"]],
    on= match_col,
    how="inner"
)


def cellage_variance_per_dpf(df, dpf, analysis_type, savepath = None):
    df2 = df[(df['fish_age'] == dpf) &
                      (df['cond'] == 'DMSO')]
    df2.dropna(subset=[analysis_type], inplace = True)
    fig, ax = plt.subplots(figsize = (6, 6))
    ax = sns.boxplot(x = 'cell_age',
                     y = analysis_type,
                     hue = 'cell_age',
                     palette = ['black', 'black', 'black'],
                     widths = 0.4, linewidth = 0.9,
                     data = df2, fill= False, legend = False)
    ax = sns.swarmplot(x = 'cell_age', 
                       y = analysis_type,
                       data= df2, hue = 'cell_age',
                       hue_order = sorted(df2['cell_age'].unique()),
                       palette = ['#b7adcf', '#429ea6', '#ff6b35'], size = 8)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.ylim(0, df2[analysis_type].max() + 10)
    if savepath is not None:
        plt.savefig(f'{savepath}.pdf', format = 'pdf')
    else:
        plt.show()

    if len(df2['cell_age'].unique()) == 2:
        group1 = df2[df2['cell_age'] == df2['cell_age'].unique()[0]][analysis_type]
        group2 = df2[df2['cell_age'] == df2['cell_age'].unique()[1]][analysis_type]
        t_stat, p_val = stats.ttest_ind(group1, group2, equal_var = False)
        print(f'Independent t-test run: T stat = {t_stat: 3f}, p-value = {p_val: 3f}')

    elif len(df2['cell_age'].unique()) > 2:
        print( 'More than 2 cell ages, running one way ANOVA')
        model = ols(f'{analysis_type} ~ C(cell_age)', data = df2).fit()
        anova_table = sm.stats.anova_lm(model, typ = 2)
        print(anova_table)
    else:
        print('error cannot figure out number of groups')
        return None
    return df2
    

# Testing at 4 dpf across OL measurements
cellage_variance_per_dpf(fishage_df2, 4, 'no_sheaths')
cellage_variance_per_dpf(fishage_df2, 4, 'total_output')
cellage_variance_per_dpf(fishage_df2, 4, 'avg_sheath_len')


# Testing at 5 dpf across OL measurements
nosheaths_5dpf = cellage_variance_per_dpf(fishage_df2, 5, 'no_sheaths')
output_5dpf = cellage_variance_per_dpf(fishage_df2, 5, 'total_output')
avgsheath_5dpf = cellage_variance_per_dpf(fishage_df2, 5, 'avg_sheath_len')

# Post hoc tests
output_posthoc = pairwise_tukeyhsd(output_5dpf['total_output'], 
                                   groups = output_5dpf['cell_age'])
print(output_posthoc)

avgsheath_posthoc = pairwise_tukeyhsd(avgsheath_5dpf['avg_sheath_len'].dropna(), 
                                      groups = avgsheath_5dpf['cell_age'])
print(avgsheath_posthoc)


# Showing distribution between cell ages at 5 dpf between DMSO and WIN
def cellage_distribution(df, dpf, savepath = None):
    dmso_df = df[(df['fish_age'] == dpf) &
                 (df['cond'] == 'DMSO')]
    win_df = df[(df['fish_age'] == dpf) &
                (df['cond'] == 'WIN1')]

    fig, (ax1, ax2) = plt.subplots(1,2, figsize = (8, 6))
    
    ax1.pie(dmso_df['cell_age'].value_counts(),
            labels = dmso_df['cell_age'].value_counts().index,
            autopct = lambda p: f'{int(round(p * sum(dmso_df['cell_age'].value_counts()) / 100.0))}',
            colors = ['#ee964b', '#429ea6', '#b7adcf'])
    ax2.pie(win_df['cell_age'].value_counts(),
            labels = win_df['cell_age'].value_counts().index,
            autopct = lambda p: f'{int(round(p * sum(win_df['cell_age'].value_counts()) / 100.0))}',
            colors = ['#ee964b', '#b7adcf', '#429ea6'])
    ax1.set_title('Distribution of cell ages DMSO')
    ax2.set_title('Distribution of cell ages WIN 55')
    if savepath is not None:
        plt.savefig(f'{savepath}.pdf', format = 'pdf')
    else:
        plt.show()

cellage_distribution(fishage_df2, 5, 'Figure_outputs/cellage_distribution_5dpf')
