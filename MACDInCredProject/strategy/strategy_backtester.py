import numpy as np
import pandas as pd
from datetime import datetime
import INDEX
import DATAFILES
#from data.dataExtraction import extractOptionsData
pd.options.mode.chained_assignment = None

class StrategyBackTester:

    DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    INITIAL_CAPITAL = 100
    order_book = []

    index = INDEX.BANKNIFTY
    BN_OPTIONS_CSV = DATAFILES.BN_OPTIONS_CSV
    NIFTY_OPTIONS_CSV = DATAFILES.NIFTY_OPTIONS_CSV

    OPTIONS_CSV = DATAFILES.BN_OPTIONS_CSV  # deault pointing to BankNifty

    def __init__(self, index, order_book):
        self.order_book = order_book
        self.index = index

        if self.index == INDEX.BANKNIFTY:
            self.OPTIONS_CSV = self.BN_OPTIONS_CSV
        else:
            self.OPTIONS_CSV = self.NIFTY_OPTIONS_CSV


    def backtest_strategy(self):

        options_data = pd.read_csv(self.OPTIONS_CSV)

        options_data.set_index(['Ticker'], append=False, inplace=True)
        options_data.set_index(['DateTime'], append=True, inplace=True)

        trade_details = []
        for i in self.order_book.index:

            dateTime = self.order_book.loc[i, 'DateTime']
            entry_date = datetime.strptime(dateTime, self.DATE_FORMAT)

            strike = self.order_book.loc[i,'Strike']

            MTM, QTY, slExit, trailing_stop, trailing_profit, profit_hit, profit = 0, 100, 0, 100, 200, 0 , 0
            target1, target2 , strategySL = 200, 300 , 50 #(100%,200%,-50%)
            target1_hit, target2_hit = 0, 0
            # fetching all dates for strike
            strike_data = options_data.loc[strike]
            strike_dates_data_dt = np.array([datetime.strptime(date, self.DATE_FORMAT) for date in strike_data.index.values])

            #filtering the Dates with current position date
            idx = strike_dates_data_dt[:] > entry_date
            strike_dates_data_dt = strike_dates_data_dt[idx]

            #entry_price = options_data.loc[strike, dateTime]['Close']
            entry_price = options_data.loc[[[strike, dateTime]], ['Close']].loc[(strike, dateTime)]['Close']

            entry_date = entry_date.strftime(self.DATE_FORMAT)
            for d in strike_dates_data_dt:
                current_date = d.strftime(self.DATE_FORMAT)
                #new_price = options_data.loc[strike, current_date]['Close']
                new_price = options_data.loc[[[strike, current_date]], ['Close']].loc[(strike, current_date)]['Close']
                percent_change = ((new_price - entry_price) / entry_price)
                MTM = self.INITIAL_CAPITAL * abs(percent_change + 1)

                if ((MTM >= target1) & (target1_hit == 0)):
                    QTY = QTY / 2
                    trade_details.append([strike, entry_date, entry_price, current_date, new_price, percent_change, MTM, QTY, 0])
                    target1_hit = 1

                if (target1_hit == 0) & (MTM <= strategySL): # sell full quantity
                    trade_details.append([strike, entry_date, entry_price, current_date, new_price, percent_change, MTM, QTY, 1])
                    QTY = 0
                    break

                # if target1 hit start trailing and look for target 2 else do nothing and wait for SL to hit
                if (target1_hit == 1):

                    if (MTM <= trailing_stop):
                        trade_details.append([strike, entry_date, entry_price, current_date, new_price, percent_change, MTM, QTY, 1])
                        QTY = 0 # sell remaining 50% Qty
                        break

                    if (MTM >= target2): #book remaining quantity
                        trade_details.append([strike, entry_date, entry_price, current_date, new_price, percent_change, MTM, QTY, 0])
                        QTY = 0
                        break

                    if ( MTM >= trailing_profit ): # trail 50%  for every 50%
                        trailing_profit += 50
                        trailing_stop += 50

        tradebook = pd.DataFrame(trade_details, columns=['Strike', 'Entry Time', 'Entry Price', 'Exit Time', 'Exit Price','Percent Change', 'MTM', 'Sell Qty', 'SL hit'])
        tradebook.to_csv('result/tradebook.csv',index=False)
        print(tradebook[['Strike', 'Entry Time', 'Entry Price', 'Exit Time', 'Exit Price']])

        return tradebook