
from macd_indicator import  MACDIndicator
from strategy_backtester import StrategyBackTester
from tradebook_analyze import analyze_tradebook
import INDEX
from order_generator import OrderBookGenerator

class MACDStrategy:

    BN_OTM_OFFSET = 500
    NIFTY_OTM_OFFSET = 200

    def applyStrategy(self):

        bn_macd_indicator = MACDIndicator(INDEX.BANKNIFTY)
        bn_indicator = bn_macd_indicator.createIndicator()

        order_book_generator = OrderBookGenerator(INDEX.BANKNIFTY, bn_indicator, self.BN_OTM_OFFSET)
        bn_order_book = order_book_generator.generate_order_book()

        strategy_backtester = StrategyBackTester(INDEX.BANKNIFTY, bn_order_book)
        tradebook = strategy_backtester.backtest_strategy()
        analyze_tradebook(tradebook)

        #signalGenerator.generateBNOrderBook(bn_indicator)
        #nifty_h_data_signal = macdIndicator.createNiftyIndicator()
        #signalGenerator.generateNiftyOrderBook(nifty_h_data_signal)
        #signalGenerator.backtest_strategy(nifty_h_data_signal)



macdStrategy = MACDStrategy()
macdStrategy.applyStrategy()