import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np
import os
import statsmodels.formula.api as smf
import statsmodels.api as sm
from scipy.stats import linregress
from statsmodels.formula.api import ols, mixedlm

# Import data
nbt_df = pd.read_excel('DataSheets/combined_nbt_mbpnls_24.xlsx',
                       sheet_name = 'combined')
# Remove WIN05 condition
nbt_df_analysis = nbt_df[nbt_df.condition != 0.5]
# Remove fish with only one data point
nbt_timeline = nbt_df_analysis[nbt_df_analysis.groupby('fish_ID').fish_ID.transform('count')>1]

# Seperate the fish by dpf 
nbt_5dpf_analysis = nbt_df_analysis[nbt_df_analysis['dpf'] == 5]

#add column for % ratio of neurons wrapped over total aberrant
nbt_5dpf_analysis.loc[:,'ratio'] = ((nbt_5dpf_analysis['neurons']/ nbt_5dpf_analysis['aberrant'])*100).where(nbt_df_analysis['aberrant'] !=0, 0)
#14 DMSO fish 17 WIN 1 fish

count_WIN1_aberrant = nbt_5dpf_analysis[(nbt_5dpf_analysis['condition'] == 1.0) & 
                                   (nbt_5dpf_analysis['aberrant'] > 0)].shape[0]
#13 out of 17 WIN 1 fish have at least one aberrant structure at 5 dpf
count_dmso_aberrant = nbt_5dpf_analysis[(nbt_5dpf_analysis['condition'] == 0) & 
                                        (nbt_5dpf_analysis['aberrant'] > 0)].shape[0]
# 8 out of 14 DMSO fish have at least one aberrant structure at 5 dpf

# Finding the mean percentage of neurons wrapped over aberrant structures
avg_ratio = nbt_5dpf_analysis.groupby('condition')['ratio'].mean()
#Plotting the ratio of how many neurons are wrapped over total number of aberrant structures


#Find unique fish IDs per condition
def find_unique_fish(df, condition_column, condition):
    cond_df = df[df[condition_column] == condition]
    unique_fish = cond_df['fish_ID'].nunique()
    return unique_fish

dmso_fish = find_unique_fish(nbt_timeline,'condition', 0.0)
win1_fish = find_unique_fish(nbt_timeline, 'condition',1.0)


def plot_nbt_mbp_aberrant(df, x_interval = 1, y_interval = 5, figsize = (8, 6)):
    """
    Plot the number of aberrant circles over time, tracking the same fish from 3 -5 dpf.
    Seperated by condition. Plots individual fish as small thin lines and the average 
    as thicker lines with standard error bars at 1 standard error."""

    y_min = 0
    y_max = df['aberrant'].max()
    y_max_rounded = np.ceil(y_max / y_interval) * y_interval

    fig, ax = plt.subplots(figsize = figsize)
    sns.lineplot(data = df, x = 'dpf', y = 'aberrant',
                units = 'fish_ID', estimator= None,
                hue = 'condition',
                palette=["#1768AC", "#F72585", "#420039"],
                legend = False,
                alpha = 0.9, linewidth = .25)
    
                
    sns.lineplot(data = df, x = 'dpf', y = 'aberrant',
                hue = 'condition', err_style = 'bars',
                err_kws={'capsize': 5, 'capthick': 2, 'elinewidth': 2} ,
                palette=["#1768AC", "#F72585", "#420039"],
                errorbar=("sd"))

# Customize plot
    plt.title('Number of Aberrant Structures')
    plt.xlabel('Fish Age (dpf)')
    plt.ylabel('Number of Aberrant Occurences')
    # plt.legend(title='Condition', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(np.arange(3, 6, x_interval))
    #plt.yticks(np.arange(y_min, y_max_rounded + y_interval, y_interval))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

# Adjust layout
    plt.tight_layout()
    return plt.gcf()

#Usage
plot_nbt_mbp_aberrant(df = nbt_timeline)
plt.savefig("Figure_Outputs/abberant_timeline_stdev.pdf", format='pdf')
plt.show()

# Find average number of aberrant structures in 5 dpf fish
nbt_5avg= nbt_timeline[nbt_timeline['dpf'] == 5]
nbt_5avg.groupby('condition')['aberrant'].mean()
nbt_5avg.groupby('condition')['aberrant'].std()
nbt_5avg.groupby('condition')['aberrant'].median()

# Remove fish with 0 aberrant structures
nbt_only_ab = nbt_timeline[nbt_timeline['aberrant'] != 0]
nbt_5ab = nbt_5avg[nbt_5avg['aberrant'] != 0]
dmso_5ab = nbt_5ab[nbt_5ab['condition'] == 0.0]
win1_5ab = nbt_5ab[nbt_5ab['condition'] == 1.0]

# Find slopes of dmso and win1 neurons over abberant structures
dslope, dintercept, dr, dpvalue, dse = linregress(dmso_5ab['aberrant'], dmso_5ab['neurons'])
print(dslope, dintercept, dr, dpvalue, dse)

wslope, wintercept, wr, wpvalue, wse = linregress(win1_5ab['aberrant'], win1_5ab['neurons'])
print(wslope, wintercept, wr, wpvalue, wse)

# Perform linear regression with interactions
total_ab_model = mixedlm('aberrant ~ dpf * condition', groups = nbt_timeline['fish_ID'], 
                    data = nbt_timeline).fit()
# Print results
print(total_ab_model.summary()) 

# Perform linear regression with interactions
model = smf.ols('neurons ~ aberrant * condition', data=nbt_5ab).fit()
# Print results
print(model.summary())

stats_data = {
    'variable': ['Intercept', 'aberrant', 'condition', 'aberrant:condition'],
    'coef': [-0.3571, 0.7286, -0.0796, -0.0978],
    'ci_lower': [-3.269, 0.006, -3.228, -0.825],
    'ci_upper': [2.555, 1.451, 3.069, 0.629]
}
stats_df = pd.DataFrame(stats_data)

#ratio model 
ratio_mdl = smf.ols('ratio ~ dpf * condition', data = nbt_only_ab).fit()
print(ratio_mdl.summary())


# Plot neurons over abberant 
nbt_5ab['aberrant'] = pd.to_numeric(nbt_5ab['aberrant'])
nbt_5ab['neurons'] = pd.to_numeric(nbt_5ab['neurons'])

fig, ax = plt.subplots(figsize = (10, 6))
#sns.scatterplot(data = nbt_5ab, x = 'aberrant', y = 'neurons',
#              hue = 'condition', ax = ax, 
#              palette= ["#1768AC", "#F72585"])

sns.lineplot(x=nbt_5dpf_analysis['aberrant'], y = dintercept + dslope*nbt_5dpf_analysis['aberrant'],
            color = "#1768AC")
#sns.lineplot( data= nbt_5ab, x = 'aberrant', y = 'neurons',
          #   hue = 'condition', errorbar= ('ci', 95), ax = ax, 
           #   palette= ["#1768AC", "#F72585"])

#sns.lmplot(data = nbt_5ab, x = 'aberrant', y= 'neurons',
  #         hue = 'condition', palette= ["#1768AC", "#F72585"])

sns.lineplot(x = nbt_5dpf_analysis['aberrant'], y = wintercept + wslope*nbt_5dpf_analysis['aberrant'],
             color = "#F72585")

min_x = nbt_5dpf_analysis['aberrant'].min() * 0.8  # 20% padding on the left
max_x = nbt_5dpf_analysis['aberrant'].max() * 1.05  # 5% padding on the right
ax.set_xlim(min_x, max_x)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_xlabel('Total Number of Aberrant Structures')
ax.set_ylabel('Number of Neurons EGFP +')
plt.tight_layout()
#plt.savefig('Figure_Outputs/dmso_aberrant_linear.pdf', format = 'pdf')
plt.show()

# Plotting the ratio of neuron to aberrant structures over time
nbt_only_ab['ratio'] = nbt_only_ab['neurons'] / nbt_only_ab['aberrant']
fig, ax = plt.subplots(figsize = (10, 6))

sns.lineplot(data = nbt_only_ab, x = 'dpf', y = 'ratio',
                hue = 'condition', palette = ["#1768AC", "#F72585"])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_ylim(0, 1)