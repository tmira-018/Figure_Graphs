import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
import scipy.stats as stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import scikit_posthocs as sp

# Plot timeline

timeline = pd.read_excel("DataSheets/Timeline_mbpcaaxnls.xlsx",
                         sheet_name = 'Combined')

dpf3 = timeline[timeline['dpf'] == 3]
dpf4 = timeline[timeline['dpf'] == 4]

fig,(ax1,ax2) = plt.subplots(1,2, figsize = (10, 6))
fig.suptitle('WIN Treatment Timeline')
sns.boxplot(data = timeline,
            x = 'treatment', y = 'aberrant',
            hue = 'cond', fill = False, 
            widths = 0.25, linewidth= 0.75,
            palette = ['black', 'black'], legend= False, ax= ax1)
sns.stripplot(data = timeline,
              x = 'treatment', y = 'aberrant',
              hue = 'cond',
              palette= ["#276FBF", "#7EBC89"],
              dodge= True, legend= False, ax = ax1)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.set_ylim(-1,14)
ax1.set_title('3 dpf')
#plt.savefig('/Users/miramota/Desktop/timeline-3dpf.pdf', format = 'pdf')

fig,ax= plt.subplots(figsize = (10, 6))
sns.boxplot(data = dpf4,
            x = 'treatment', y = 'aberrant',
            hue = 'cond', fill = False,
            widths = 0.25, linewidth= 0.75,
            palette = ['black', 'black'], legend= False
            )
sns.swarmplot(data = dpf4,
              x = 'treatment', y = 'aberrant',
              hue = 'cond',
              palette= ["#1768AC", "#F72585"],
              dodge= True, legend= True)
ax.set_title('4 dpf')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_ylim(-1,14)
plt.savefig('Figure_Outputs/timeline-4dpf-dayformat.pdf', format = 'pdf')



mbp_4dpf = pd.read_excel("/Users/miramota/OHSU Dropbox/Tania Miramontes/Data_sheets/WINmbpcaax_4dpf_sumproj_codyscode.xlsx",
                       sheet_name = 'combined_4dpf')
filtered_mbp_4dpf = mbp_4dpf[~mbp_4dpf['Cond'].isin([' 0.25 uM'])]
sns.barplot(data= filtered_mbp_4dpf, x = 'Cond', y = 'Mean',
            hue = 'Cond', hue_order= ['DMSO', '0.5 uM', '1 uM'],
            palette = ["#97EAD2","#FECEE9", "#A63A50"],
            errorbar = ('se', 1),
            capsize = .2 )
sns.swarmplot(data = filtered_mbp_4dpf, x = 'Cond', y = 'Mean',
              hue= 'Cond', hue_order= ['DMSO', '0.5 uM', '1 uM'],
              dodge = False,
              palette= ["#1768AC", "#F72585", "#420039"],
              legend= False)

DMSO_mean = mbp_4dpf[mbp_4dpf['Cond'] == 'DMSO']['Mean'].mean()
mean_05 = mbp_4dpf[mbp_4dpf['Cond'] == '0.5 uM']['Mean'].mean()
mean_1 = mbp_4dpf[mbp_4dpf['Cond'] == '1 uM']['Mean'].mean()
plt.show()


# dpf stat test

aberrant_12 = dpf4[dpf4['treatment'] == '1-2']
aberrant_23 = dpf4[dpf4['treatment'] == '2-3']
aberrant_34 = dpf4[dpf4['treatment'] == '3-4']

# numpy array condition = 0 and condition = 1
aberrant_12_0 = np.array(aberrant_12[aberrant_12['cond'] == 0]['aberrant'])
aberrant_12_1 = np.array(aberrant_12[aberrant_12['cond'] == 1]['aberrant'])
aberrant_23_0 = np.array(aberrant_23[aberrant_23['cond'] == 0]['aberrant'])
aberrant_23_1 = np.array(aberrant_23[aberrant_23['cond'] == 1]['aberrant'])
aberrant_34_0 = np.array(aberrant_34[aberrant_34['cond'] == 0]['aberrant'])
aberrant_34_1 = np.array(aberrant_34[aberrant_34['cond'] == 1]['aberrant'])

timeline_test = stats.kruskal(aberrant_12_0, aberrant_12_1, aberrant_23_0, aberrant_23_1, aberrant_34_0, aberrant_34_1)
print(timeline_test)

posthoc_results = sp.posthoc_dunn(aberrant_23, val_col="aberrant", group_col="cond", p_adjust="sidak")
print(posthoc_results)



timeline_model = ols('aberrant ~ C(treatment) * C(cond)', data=dpf4).fit()
timeline_anova_table = sm.stats.anova_lm(timeline_model, typ=2)  # Type II ANOVA
print(timeline_anova_table)

# Check effect sizes (Partial Eta Squared)
def calculate_partial_eta_squared(anova_table):
    anova_table['partial_eta_sq'] = anova_table['sum_sq'] / (anova_table['sum_sq'] + anova_table['sum_sq'].sum())
    return anova_table

anova_with_effect = calculate_partial_eta_squared(timeline_anova)
print("\nANOVA with Effect Sizes:")
print(anova_with_effect)


timeline_tukey = pairwise_tukeyhsd(timeline['aberrant'], 
                          timeline['treatment'] + timeline['cond'])
print(timeline_tukey)

summary = timeline.groupby(['treatment', 'cond', 
                      'dpf'])['aberrant'].agg(['mean', 'var']).reset_index()

summary['overdispersion'] = summary['var'] / summary['mean']

timeline_model = smf.glm('aberrant ~ C(treatment) * C(cond)', 
                         data = dpf3).fit()
print(timeline_model.summary())

timeline_model4 = smf.glm('aberrant ~ C(treatment) * C(cond)', 
                         data = dpf4).fit()
print(timeline_model4.summary())