import matplotlib.pyplot as plt
import pandas as pd


def analyze_tradebook(tradebook):
    tradebook['PnL'] = (tradebook['Exit Price'] - tradebook['Entry Price']) * tradebook['Sell Qty']
    groups = tradebook.groupby(['Entry Time', 'Strike'],as_index=False)
    grouped_df = groups.sum()
    total_trades = groups.ngroups
    total_profit = grouped_df['PnL'].sum()
    avg_pft = total_profit / total_trades
    max_profit = grouped_df['PnL'].max()
    max_loss = grouped_df['PnL'].min()
    win_trades = grouped_df[grouped_df['PnL'] > 0]['PnL'].count()
    win_trade_profit = grouped_df[grouped_df['PnL'] > 0]['PnL'].sum()
    avg_win_profit = win_trade_profit / win_trades
    loss_trades = grouped_df[grouped_df['PnL'] < 0]['PnL'].count()
    loss_trade_profit = grouped_df[grouped_df['PnL'] < 0]['PnL'].sum()
    avg_loss = loss_trade_profit / loss_trades

    grouped_df_mean = groups.mean()
    grouped_df_mean['Percent Change'] = grouped_df_mean['Percent Change'] * 100
    total_pct_profit = grouped_df_mean['Percent Change'].sum()
    avg_pct_pft = total_pct_profit / total_trades
    max_pct_profit = grouped_df_mean['Percent Change'].max()
    max_pct_loss = grouped_df_mean['Percent Change'].min()
    win_pct_trades = grouped_df_mean[grouped_df_mean['Percent Change'] > 0]['Percent Change'].count()
    win_pct_trade_profit = grouped_df_mean[grouped_df_mean['Percent Change'] > 0]['Percent Change'].sum()
    avg_pct_win_profit = win_pct_trade_profit / win_trades
    loss_pct_trades = grouped_df_mean[grouped_df_mean['Percent Change'] < 0]['Percent Change'].count()
    loss_pct_trade_profit = grouped_df_mean[grouped_df_mean['Percent Change'] < 0]['Percent Change'].sum()
    avg_pct_loss = loss_pct_trade_profit / loss_trades
    sl_hit = grouped_df_mean[grouped_df_mean['SL hit'] > 0]['SL hit'].count()
    sl_hit_pct = sl_hit / total_trades

    print('Percentage Return Stats :')

    print('Total Pct Profit : %5.2f' % total_pct_profit ,'%')
    print('Average Pct Trade Profit : %5.2f' % avg_pct_pft,'%')
    print('Maximum Pct Profit : %5.2f' % max_pct_profit,'%')
    print('Maximum Pct Loss : %5.2f' % max_pct_loss,'%')
    print('Win Pct Percentage Trades : %5.2f' % (win_pct_trades / total_trades),'%')
    print('Loss Pct Percentage Trades : %5.2f' % (loss_pct_trades / total_trades),'%')
    print('Avg Pct Profit on Win Trade : %5.2f' % avg_pct_win_profit,'%')
    print('Avg Pct Loss on Loss Trade : %5.2f' % avg_pct_loss,'%')
    print('No of Days SL hit Either Trailing or Combined SL : %5.2f' % sl_hit)
    print('SL Hit Percentage : %5.2f' % sl_hit_pct,'%')


    print('PnL Stats :')

    print('Total Profit : %12.2f' % total_profit)
    print('Average Trade Profit : %12.2f' % avg_pft)
    print('Maximum Profit : %12.2f' % max_profit)
    print('Maximum Loss : %12.2f' % max_loss)
    print('Win Percentage Trades : %12.2f' % (win_trades / total_trades))
    print('Loss Percentage Trades : %12.2f' % (loss_trades / total_trades))
    print('Avg Profit on Win Trade : %12.2f' % avg_win_profit)
    print('Avg Loss on Loss Trade : %12.2f' % avg_loss)

    plt.figure(figsize=(10, 7))

    plt.title("Cumulative Strategy Returns")
    plt.xlabel('Time From {} To {}'.format( grouped_df_mean['Entry Time'].min(),grouped_df_mean['Entry Time'].max()) )
    plt.xticks(range(0,len(grouped_df_mean['Entry Time'])),pd.DatetimeIndex(grouped_df_mean['Entry Time']).month)
    plt.ylabel('Percentage Returns')
    plt.plot(grouped_df_mean['Percent Change'].cumsum())
    plt.tight_layout()
    plt.show()

    #grouped_df_mean['Percent Change'].cumsum().plot(figsize=(10, 7))


def readtradebook():
    tradebook =  pd.read_csv('result/tradebook.csv')
    analyze_tradebook(tradebook)

#readtradebook()
