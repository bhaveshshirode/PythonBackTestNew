import numpy as np
import pandas as pd
import INDEX
from datetime import datetime

class OrderBookGenerator:

    indicator = []
    index = INDEX.BANKNIFTY
    otm_offset = 500
    def __init__(self, index, indicator, otm_offset):
        self.indicator = indicator
        self.index = index
        self.otm_offset = otm_offset

    def generate_order_book(self):

        self.indicator['Type'] = np.where(self.indicator['macd_signal'] > 0, 'CE', np.NAN)
        self.indicator['Type'] = np.where(self.indicator['macd_signal'] < 0, 'PE', self.indicator['Type'])

        #start_date = datetime.strptime('2021-11-01 09:15:00', '%Y-%m-%d %H:%M:%S')
        start_date = self.indicator.index.min() + pd.DateOffset(days=30)
        idx = self.indicator.index[:] > start_date
        self.indicator = self.indicator[idx]

        buy_book = self.indicator[self.indicator['macd_signal'] > 0]
        buy_book['Strike'] = buy_book['Ticker'].map(str) + 'WK' + (buy_book['ATM'].map(int) + self.otm_offset).map(str) + buy_book['Type']

        sell_book = self.indicator[self.indicator['macd_signal'] < 0]
        sell_book['Strike'] = sell_book['Ticker'].map(str) + 'WK' + (sell_book['ATM'].map(int) - self.otm_offset).map(str) + sell_book['Type']

        order_book = pd.concat([buy_book, sell_book])

        order_book.to_csv('result/'+self.index+'orderbook.csv', index=False)
        print(order_book[['DateTime', 'macd_signal', 'Strike', 'Close']])
        return order_book