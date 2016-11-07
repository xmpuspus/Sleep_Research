import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec



def graph_sleep_pred(df_pred, col_='pred'):
    """Graphs the result from the classifier.
    Parameter
    ----------
    df_pred : DataFrame
    col_ : string
    """
    #sleep phases_classification
    plt.figure(figsize=(20,4))
    gs = gridspec.GridSpec(2,1, height_ratios=[1.5,2])
    
    df_pred.loc[df_pred['psg']==6, 'psg'] = 8
    df_pred.loc[df_pred['psg']==7, 'psg'] = 6

    ax1 = plt.subplot(gs[0])
    ax1.plot_date(df_pred.dtime, df_pred.psg, '-')
    ax1.xaxis.grid(True)
    ax1.yaxis.grid(True)
    ax1.set_ylim([0, 9])
    ax1.set_ylabel('Sleep Stages-PSG')
    ax1.set_yticklabels(['', '3', '2', '1', '', 'R', 'M', ' ', 'W', ''])
    ax1.tick_params(axis='y', which='major', labelsize=8)  
    ax1.set_xticklabels([])
    
    df_pred.loc[df_pred[col_]==6, col_] = 8
    df_pred.loc[df_pred[col_]==7, col_] = 6
    
    ax2 = plt.subplot(gs[1])
    ax2.plot_date(df_pred.dtime, df_pred[col_], '-')
    ax2.xaxis.grid(True)
    ax2.yaxis.grid(True)
    ax2.set_ylim([0, 9])
    ax2.set_ylabel('Sleep Stages-pred')
    ax2.set_yticklabels(['', '3', '2', '1', '', 'R', 'M', ' ', 'W', ''])
    ax2.tick_params(axis='y', which='major', labelsize=8)  
    
    plt.show()
