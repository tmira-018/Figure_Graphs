import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np

# Plot vo103

mutant_df = pd.read_excel("/Users/miramota/OHSU Dropbox/Tania Miramontes/Data_sheets/vo103_mbpnlscaax_24.xlsx",
                       sheet_name = 'combined')
 
mutant_5dpf = mutant_df[mutant_df['dpf']== 5]

mutant_5dpf_2 = mutant_5dpf[mutant_5dpf['condition'] != 'WIN05μM']

sns.barplot(data= mutant_5dpf_2, x = 'condition', y = 'aberrant',
            hue = 'genotype', hue_order= ['wt', 'het', 'mut'],
            palette = ["#97EAD2","#FECEE9", "#A63A50"],
            errorbar = ('se', 1),
            capsize = .2 )
sns.swarmplot(data = mutant_5dpf_2, x = 'condition', y = 'aberrant',
              hue= 'genotype',
              dodge = True,
              hue_order=['wt', 'het', 'mut'],
              palette= ['black', 'black', 'black'],
              legend= False)
plt.savefig('/Users/miramota/Desktop/vo103_aberrant.pdf', format='pdf')
plt.show()