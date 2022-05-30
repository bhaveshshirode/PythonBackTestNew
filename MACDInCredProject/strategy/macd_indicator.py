import pandas as pd
import data
import numpy as np
import INDEX

class MACDIndicator:

    BN_SPOT_CSV = '../data/BN_Spot_H_data'
    NIFTY_SPOT_CSV = '../data/NIFTY_Spot_H_data'

    SPOT_CSV = '../data/BN_Spot_H_data' #deault pointing to BankNifty

    SPOT_DATA = []
    INDEX = INDEX.BANKNIFTY
    def __init__(self, index):
        self.index = index

        if self.index == INDEX.BANKNIFTY:
            self.SPOT_CSV = self.BN_SPOT_CSV
        else:
            self.SPOT_CSV = self.NIFTY_SPOT_CSV

    def createIndicator(self):

        self.SPOT_DATA =  pd.read_csv(self.SPOT_CSV)

        self.SPOT_DATA['macd'] = self.SPOT_DATA['Close'].ewm(span=12).mean() - self.SPOT_DATA['Close'].ewm(span=26).mean()
        self.SPOT_DATA['signal'] = self.SPOT_DATA['macd'].ewm(span=9).mean()

        self.SPOT_DATA['macd_signal'] = np.where((self.SPOT_DATA['macd'] > self.SPOT_DATA['signal']) & (self.SPOT_DATA['macd'].shift(1) < self.SPOT_DATA['signal'].shift(1)), 1, 0)
        self.SPOT_DATA['macd_signal'] = np.where((self.SPOT_DATA['macd'] < self.SPOT_DATA['signal']) & (self.SPOT_DATA['macd'].shift(1) > self.SPOT_DATA['signal'].shift(1)), -1, self.SPOT_DATA['macd_signal'])

        self.SPOT_DATA['ATM'] = np.round(self.SPOT_DATA['Close'] / 100).astype(int) * 100

        return self.SPOT_DATA
