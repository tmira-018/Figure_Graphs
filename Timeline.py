import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np

# Plot timeline

timeline = pd.read_excel("DataSheets/Timeline_mbpcaaxnls.xlsx",
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
fig, ax = plt.subplots()
sns.boxplot(data = dpf4,
            x = 'treatment', y = 'aberrant',
            hue = 'cond', fill = False,
            widths = 0.25, linewidth= 0.75,
            palette = ['black', 'black'], legend= False
            )
sns.swarmplot(data = dpf4,
              x = 'treatment', y = 'aberrant',
              hue = 'cond',
              palette= ["#276FBF", "#7EBC89"],
              dodge= True, legend= True)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_ylim(-1,14)
plt.savefig('Figure_Outputs/timeline-4dpf.pdf', format = 'pdf')


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