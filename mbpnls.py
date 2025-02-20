import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np

# Import data 
nls_4dpf = pd.read_excel('/Users/miramota/OHSU Dropbox/Tania Miramontes/Data_sheets/WIN_mbp-nls_4dpf.xlsx',
                         sheet_name= 'combined_spinal')
nls_5dpf = pd.read_excel('/Users/miramota/OHSU Dropbox/Tania Miramontes/Data_sheets/WIN_mbp-nls_5dpf.xlsx',
                         sheet_name= 'combined_spinal')

# Plot mbpnls
fig, (ax1,ax2) = plt.subplots(1,2, sharey=True)
sns.boxplot(data = nls_4dpf,
            fill = False, widths = 0.25, linewidth= 0.75,
            palette= ['black', 'black', 'black'], ax=ax1)
sns.swarmplot(data = nls_4dpf,
              palette = ["#1768AC", "#F72585", "#420039"],
              legend = False, ax=ax1)
sns.boxplot(data = nls_5dpf, 
            fill = False, widths = 0.25, linewidth= 0.75,
            palette = ['black', 'black', 'black'], ax=ax2)
sns.swarmplot(data = nls_5dpf, 
              palette = ["#1768AC", "#F72585", "#420039"],
              legend = False, ax=ax2)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False) 
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False) 
plt.yticks(np.arange(0, 250, 50))  
ax2.legend(loc = 'upper right')
plt.savefig("/Users/miramota/Desktop/Figures/mbp_nls/mbpnls-45graph.pdf", format='pdf')
plt.show()
