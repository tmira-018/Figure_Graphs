import os
import argparse
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def plot_ind_OL(df,analysis_type, title = 'title',
                       y_min = 0,y_interval=5,
                       x_interval=1, figsize=(10, 6),
                       error_bar_kws = {'capsize': 5, 'capthick': 2, 'elinewidth': 2},
                       xlabel = str, ylabel = str):
    """
    Plots the all individual cells across time grouped by condition.
    Average value of each condition is overlayed with standard error shown.
    
    df = dataframe ,
    analysis_type = column name of the data to be plotted,
    title = (str) title of the plot,
    y_min = (int) minimum value on y-axis default = 0, y_max = (int) maximum value on y-axis,
    y_max_rounded = (int) rounded up maximum value on y-axis,
    x_interval = (int) interval on the x axis default = 1,
    y_interval = (int) interval on the y axis default = 5, 
    figsize = (tuple) size of the figure default (10,6),
    error_bar_kws = (dict) adjust error bar style needs capsize, capthick, elinewidth
    """
    #condition = sheaths_df[sheaths_df['cond'] == condition]
    y_max = df[analysis_type].max()
    y_max_rounded = np.ceil(y_max / y_interval) * y_interval
    # Create figure
    plt.figure(figsize=figsize)

    # Create main plot
    # Individual lines each cell
    ax = sns.lineplot(data=df,
                x='cell_age',
                y= analysis_type,
                units='cell_ID',
                estimator=None,
                hue='cond',
                palette=["#1768AC", "#420039"],
                legend=False,
                alpha= 0.8,  # Make individual lines transparent
                linewidth=.25)  # Thinner lines for individuals
    
    #Thicker line for the average
    ax = sns.lineplot(data=df,
                 x = 'cell_age',
                 y= analysis_type,
                 hue = 'cond',
                 err_style = 'bars',
                 err_kws={'capsize': 5, 'capthick': 2, 'elinewidth': 2},
                 palette=["#1768AC", "#420039"],
                 errorbar=("se", 1))  
    
    #Customize the plot
    plt.title(title, fontsize=18)
    plt.xlabel(xlabel, fontsize=14)
    plt.ylabel(ylabel, fontsize=14)
    plt.legend(title= analysis_type, bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(np.arange(1, 5, x_interval), fontsize=12)
    plt.yticks(np.arange(y_min, y_max_rounded + y_interval, y_interval), fontsize=12)  

    #Customize plot 
    ax.spines[['top', 'right']].set_visible(False)
    #ax.spines[linewidth=2]
    ax.spines[['left', 'bottom']].set_linewidth(2)

    # Adjust layout
    plt.tight_layout()
    return plt.gcf()


def main():
    parser = argparse.ArgumentParser(description = 'Graphing multiple measurements of individual OL across time')

    #Arguments
    parser.add_argument('path', type = str, help= 'The path to the excel file with the combined data of individual OL measurements')
    parser.add_argument('analysis_type', type = str, help= 'OL measurement to plot, number of sheaths, average sheath length, or total myelin output')
    parser.add_argument('title', type = str, help = 'Title of the graph')
    
    args = parser.parse_args()

    path = args.path
    analysis_type = args.analysis_type
    title = args.title

    if not os.path.isfile(path):
        print(f"Error: the directory '{path}' does not exist")
        return
    
    #Load data
    ol_df = pd.read_excel(path)

    #shows how many times each cell is repeated, how many days the cell is available
    repeats = ol_df['cell_ID'].value_counts()
    #check how many cells appear only once
    one_times = repeats[repeats == 1].index
    #keeps the cells that appear more than one time shape of ol_analysis plus one_times should equal shape of ol_df
    ol_analysis= ol_df[ol_df['cell_ID'].map(ol_df['cell_ID'].value_counts()) > 1]
    #removes cells that were treated with 0.5 um WIN
    ol_analysis2 = ol_analysis[ol_analysis.cond != 0.5]

    #Make fish id and cell id categorical for statistical analysis if needed
    fish_ID = ol_analysis["fish_ID"].astype("category")
    cell_ID = ol_analysis["cell_ID"].astype("category")

    # Usage: plotting OL measurement
    plot_ind_OL(df = ol_analysis2, analysis_type= analysis_type, 
                    title = title, 
                    ylabel='N', xlabel='Age')
    plt.show()

if __name__ == '__main__':
    main()


#plt.savefig('/Users/miramota/Desktop/Figures/single_cell_WIN/total_output_means.pdf', format='pdf')

