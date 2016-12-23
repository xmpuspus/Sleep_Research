import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec



def graph_sleep_wake_psg(df_, df_algo):
    """Graphs the raw accelerometer readings, polysomnography data and the results from the sleep-wake algorithms.
    Parameter
    ----------
    df_ : DataFrame
    df_algo : DataFrame
    """
    plt.figure(10, figsize=(20,20),dpi=85,facecolor='w',edgecolor='k')
    gs = gridspec.GridSpec(14,1)#,height_ratios=[1,1,1,1,1,1])

    ax1 = plt.subplot(gs[0])
    ax1.plot_date(df_.t, df_.z, '-', color = 'r')
    ax1.plot_date(df_.t, df_.x, '-', color = 'b')
    ax1.plot_date(df_.t, df_.y, '-', color = 'c')
    ax1.xaxis.grid(True)
    ax1.yaxis.grid(True)
    ax1.set_ylabel('Raw Data')
    ax1.set_yticks([])
    ax1.set_yticklabels([])
    ax1.set_xticklabels([])

    #Sleep stages from polysomnography data
    df_.loc[df_['psg']==6, 'psg'] = 8
    df_.loc[df_['psg']==7, 'psg'] = 6
    ax2 = plt.subplot(gs[1])
    ax2.plot_date(df_.t, df_.psg, '-')
    ax2.set_ylim([0,9])
    ax2.set_ylabel('Sleep Stages-psg')
    ax2.set_yticklabels(['', '3', '2', '1', '', 'R', 'M', ' ', 'W', ''])
    ax2.set_xticklabels('')
    ax2.xaxis.grid(True)
    
    #Sleep-Wake from polysomnography data
    df_['psg_'] = df_['psg'].apply(lambda x: 1 if ((x > 5) | (x==0)) else 0)
    df_['dtime'] = pd.to_datetime(df_['dtime'])
    df_ = df_.set_index('dtime')
    ax3 = plt.subplot(gs[2])
    ax3.fill_between(df_.index, df_.psg_, 1, facecolor = 'yellow')
    ax3.set_ylabel('PSG')
    ax3.set_yticks([])
    ax3.set_yticklabels([])
    ax3.set_xticklabels([])
    ax3.xaxis.grid(True)
    
    
    df_algo['dtime'] = pd.to_datetime(df_algo['dtime'])
    df_algo = df_algo.set_index('dtime')   

    #Cole
    ax4 = plt.subplot(gs[3])
    ax4.fill_between(df_algo.index, df_algo.rescored_cole, 1, facecolor = 'cyan')
    ax4.set_ylabel('Cole Rescored')
    ax4.set_yticks([])
    ax4.set_yticklabels([])
    ax4.set_xticklabels([])
    ax4.xaxis.grid(True)

    #Sadeh
    ax5 = plt.subplot(gs[4])
    ax5.fill_between(df_algo.index, df_algo.rescored_sadeh, 1, facecolor = 'cyan')
    ax5.set_ylabel('Sadeh Rescored')
    ax5.set_yticks([])
    ax5.set_yticklabels([])
    ax5.set_xticklabels([])
    ax5.xaxis.grid(True)
    
    #Oakley
    ax6 = plt.subplot(gs[5])
    ax6.fill_between(df_algo.index, df_algo.rescored_oakley, 1, facecolor = 'cyan')
    ax6.set_ylabel('Oakley Rescored')
    ax6.set_yticks([])
    ax6.set_yticklabels([])
    ax6.set_xticklabels([])
    ax6.xaxis.grid(True)

    #Oakley using RMS
    ax7 = plt.subplot(gs[6])
    ax7.fill_between(df_algo.index, df_algo.rescored_oakley_rms, 1, facecolor = 'orange')
    ax7.set_ylabel('Oakley-RMS Rescored')
    ax7.set_yticks([])
    ax7.set_yticklabels([])
    ax7.set_xticklabels([])
    ax7.xaxis.grid(True)
    
    #Cole using RMS
    ax8 = plt.subplot(gs[7])
    ax8.fill_between(df_algo.index, df_algo.rescored_cole_rms, 1, facecolor = 'orange')
    ax8.set_ylabel('Cole-RMS Rescored')
    ax8.set_yticks([])
    ax8.set_yticklabels([])
    ax8.xaxis.grid(True)


    plt.show()
