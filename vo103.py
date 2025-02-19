import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np

# Plot vo103

# Load the data from the excel file
mutant_df = pd.read_excel("/Users/miramota/OHSU Dropbox/Tania Miramontes/Data_sheets/vo103_mbpnlscaax_24.xlsx",
                       sheet_name = 'combined')
 
# Edit the dataframe to include only 5dpf data
mutant_5dpf = mutant_df[mutant_df['dpf']== 5]

# Exclude the WIN05μM condition
mutant_5dpf_2 = mutant_5dpf[mutant_5dpf['condition'] != 'WIN05μM']

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
plt.savefig('/Users/miramota/Desktop/Figures/vo103/vo103_aberrant.pdf', format='pdf')
plt.show()
