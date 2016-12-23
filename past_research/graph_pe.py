import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec



def graph_pe(df, col1='z_bp', col2='pe', col3='sleep_stage_pe'):
    """Graphs the bandpass filtered data, permutation entropy (PE) results 
    and the comparison between the ground truth vs the predicted sleep stages.
    """
    plt.figure(figsize=(20,6))
    gs = gridspec.GridSpec(3,1, height_ratios=[1,1,1.5])
    
    ax1 = plt.subplot(gs[0])
    ax1.plot_date(df.dtime, df[col1], '-')
    ax1.xaxis.grid(True)
    ax1.yaxis.grid(True)
    ax1.set_ylabel('Raw Data (%s)' %col1)
    ax1.tick_params(axis='y', which='major', labelsize=8)  
    ax1.set_xticklabels([])

    ax2 = plt.subplot(gs[1])
    ax2.plot_date(df.dtime, df[col2], '-')
    ax2.xaxis.grid(True)
    ax2.yaxis.grid(True)
    ax2.set_ylabel('Permutation Entropy')
    ax2.tick_params(axis='y', which='major', labelsize=8) 
    ax2.set_xticklabels([])
    
    df.loc[df['psg']==6, 'psg'] = 8
    df.loc[df['psg']==7, 'psg'] = 6
    
    df.loc[df[col3]==6, col3] = 8
    df.loc[df[col3]==7, col3] = 6

    ax3 = plt.subplot(gs[2])
    ax3.plot_date(df.dtime, df.psg, '-', label='polysomnography')
    ax3.plot_date(df.dtime, df[col3], 'r-', label='predicted')
    ax3.xaxis.grid(True)
    ax3.yaxis.grid(True)
    ax3.set_ylim([0, 9])
    ax3.set_ylabel('Sleep Stages')
    ax3.set_yticklabels(['', '3', '2', '1', '', 'R', 'M', ' ', 'W', ''])
    ax3.tick_params(axis='y', which='major', labelsize=8)  
    
    plt.legend(ncol=2, bbox_to_anchor=[1, 1.18])
    plt.show()
