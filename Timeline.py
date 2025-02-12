import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np

# Plot timeline

timeline = pd.read_excel("/Users/miramota/OHSU Dropbox/Tania Miramontes/Data_sheets/Timeline_mbpcaaxnls.xlsx",
                         sheet_name = 'Combined')

dpf3 = timeline[timeline['dpf'] == 3]
treat12 = dpf3[dpf3['treatment'] == '1-2']
sns.barplot(data = dpf3,
            x = 'treatment', y = 'aberrant',
            hue = 'cond', 
            palette = ["#1768AC", "#420039"],
            errorbar = ('se', 1))
sns.swarmplot(data = dpf3,
              x = 'treatment', y = 'aberrant',
              hue = 'cond',
              palette= ['black', 'black', 'black'],
              dodge= True, legend= False)
plt.ylim(0,12)
plt.savefig('/Users/miramota/Desktop/timeline-3dpf.pdf', format = 'pdf')

dpf4 = timeline[timeline['dpf'] == 4]
sns.barplot(data = dpf4,
            x = 'treatment', y = 'aberrant',
            hue = 'cond', 
            palette = ["#1768AC", "#420039"],
            errorbar = ('se', 1))
sns.swarmplot(data = dpf4,
              x = 'treatment', y = 'aberrant',
              hue = 'cond',
              palette= ['black', 'black', 'black'],
              dodge= True, legend= False)
plt.savefig('/Users/miramota/Desktop/timeline-4dpf.pdf', format = 'pdf')


fig, (ax1, ax2) = plt.subplots(1, 2)
fig.suptitle('WIN Treatment Timeline')
sns.barplot(data = dpf3,
            x = 'treatment', y = 'aberrant',
            hue = 'cond', 
            palette = ["#1768AC", "#420039"], 
            errorbar = ('se', 1), ax=ax1)
sns.swarmplot(data = dpf3,
              x = 'treatment', y = 'aberrant',
              hue = 'cond',
              palette= ['black', 'black'],
              dodge= True, legend= False, ax=ax1)
ax1.set_ylim(0,14)
sns.barplot(data = dpf4,
            x = 'treatment', y = 'aberrant',
            hue = 'cond', 
            palette = ["#1768AC", "#420039"],
            errorbar = ('se', 1), ax=ax2)
sns.swarmplot(data = dpf4,
              x = 'treatment', y = 'aberrant',
              hue = 'cond',
              palette= ['black', 'black'],
              dodge= True, legend= False, ax=ax2)
ax2.set_ylim(0,14)
plt.savefig('/Users/miramota/Desktop/timeline_graph.pdf', format = 'pdf')


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