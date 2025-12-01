
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import scipy.stats as stats


# Load data, this is the dataframe with fish age accounted for only
path = ()
fishage_df = pd.read_excel(path)

# Load data, this is the original dataframe with cell age 
path2 = ()
cellage_df = pd.read_excel(path2)


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



repeats = fishage_df2['cell_ID'].value_counts()
one_times = repeats[repeats == 1].index
ol_var_analysis= fishage_df2[fishage_df2['cell_ID'].map(fishage_df2['cell_ID'].value_counts()) > 1]


def var_test(dataframe, condition, variable):
    print(f'Variable: {variable} Condition: {condition}')
    cell_ages = sorted(dataframe['cell_age'].unique())
    fish_ages = sorted(dataframe['fish_age'].unique())

    for i, j in zip(cell_ages, fish_ages):
        print(i,j)

        cell_subset = dataframe[(dataframe['cell_age'] == i) &
                            (dataframe['cond'] == condition)]
        
        fish_subset = dataframe[(dataframe['fish_age'] == j) &
                                (dataframe['cond'] == condition)]
        
        cell_arr = cell_subset[variable].to_numpy()
        fish_arr = fish_subset[variable].to_numpy()

        if len(cell_arr) == 0 or len(fish_arr) == 0:
            print(f"no data for cell age {i} or fish age {j}")
        else:
            stat, p = stats.levene(cell_arr, fish_arr)
            print('Levene test = %.3f, p=%.3f' % (stat, p))
        if p > 0.05:
            print('Probably equal variances')
        else:
            print('Probably unequal variances')


def var_test_combined(dataframe, variable):
    print(f' Variable: {variable}')
    cell_ages = sorted(dataframe['cell_age'].unique())
    fish_ages = sorted(dataframe['fish_age'].unique())

    for i, j in zip(cell_ages, fish_ages):
        print(i,j)

        cell_subset = dataframe[dataframe['cell_age'] == i]

        fish_subset = dataframe[dataframe['fish_age'] == j]

        cell_arr = cell_subset[variable].to_numpy()
        fish_arr = fish_subset[variable].to_numpy()

        if len(cell_arr) == 0 or len(fish_arr) == 0:
            print(f"no data for cell age {i} or fish age {j}")
        else:
            stat, p = stats.levene(cell_arr, fish_arr)
            print('Levene test = %.3f, p=%.3f' % (stat, p))
        if p > 0.05:
            print('Probably equal variances')
        else:
            print('Probably unequal variances')


var_test(ol_var_analysis, 'DMSO', 'no_sheaths')
var_test(ol_var_analysis, 'WIN1', 'no_sheaths')

var_test(ol_var_analysis, 'DMSO', 'avg_sheath_len')
var_test(ol_var_analysis, 'WIN1', 'avg_sheath_len')

var_test(ol_var_analysis, 'DMSO', 'total_output')
var_test(ol_var_analysis, 'WIN1', 'total_output')


var_test_combined(ol_var_analysis, 'no_sheaths')
var_test_combined(ol_var_analysis, 'avg_sheath_len')
var_test_combined(ol_var_analysis, 'total_output')

