import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
import scipy.stats as stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import scikit_posthocs as sp
import statsmodels.api as sm
import statsmodels.formula.api as smf

# Plot timeline

timeline = pd.read_excel("/Graphs/DataSheets/Timeline_mbpcaaxnls.xlsx",
                         sheet_name = 'Combined')

dpf3 = timeline[timeline['dpf'] == 3]
dpf4 = timeline[timeline['dpf'] == 4]

fig, ax= plt.subplots(figsize = (10, 6))
fig.suptitle('WIN Treatment Timeline')
sns.boxplot(data = timeline,
            x = 'treatment', y = 'aberrant',
            hue = 'cond', fill = False, 
            widths = 0.25, linewidth= 0.75,
            palette = ['black', 'black'], legend= False)
sns.stripplot(data = timeline,
              x = 'treatment', y = 'aberrant',
              hue = 'cond',
              palette= ["#276FBF", "#7EBC89"],
              dodge= True, legend= False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_ylim(-1,14)
ax.set_title('3 dpf')
#plt.savefig('/Graphs/Figure_Outputs/timeline-3dpf.pdf', format = 'pdf')

fig,ax= plt.subplots(figsize = (10, 6))
sns.boxplot(data = dpf4,
            x = 'treatment', y = 'aberrant',
            hue = 'cond', fill = False,
            widths = 0.25, linewidth= 0.75,
            palette = ['black', 'black'], legend= False
            )
sns.swarmplot(data = dpf4,
              x = 'treatment', y = 'aberrant',
              hue = 'cond', size = 8,
              palette= ["#1768AC", "#F72585"],
              dodge= True, legend= True)
ax.set_title('4 dpf')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_ylim(-1,14)
#plt.savefig('/Graphs/Figure_Outputs/timeline-4dpf-dayformat.pdf', format = 'pdf')


# Statistical analysis 2 way ANOVA

timeline_model = ols('aberrant ~ C(treatment) * C(cond)', data=dpf4).fit()
timeline_anova_table = sm.stats.anova_lm(timeline_model, typ=2)  # Type II ANOVA
print(timeline_anova_table)
