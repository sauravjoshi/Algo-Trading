from AlgorithmImports import *


class Learningalgotrade(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2008, 1, 1)  # Set the start date for backtesting
        self.SetEndDate(2023, 6, 10)  # Set the end date for backtesting
        self.SetCash(100000)  # Set an initial cash amount

        # Add SPY as the symbol for trading
        self.spy = self.AddEquity("SPY", Resolution.Daily).Symbol

        # Set MACD indicator parameters
        self.fastPeriod = 12
        self.slowPeriod = 26
        self.signalPeriod = 9

        # Initialize MACD indicator
        self.macd = self.MACD(self.spy, self.fastPeriod, self.slowPeriod,
                              self.signalPeriod, MovingAverageType.Exponential, Resolution.Daily)

        self.SetWarmUp(50, Resolution.Daily)
        # Schedule daily function to check and rebalance the portfolio
        # self.Schedule.On(self.DateRules.EveryDay(
        #     self.spy), self.TimeRules.AfterMarketOpen(self.spy, 30), self.CheckSignal)

    def OnData(self, data):

        if self.IsWarmingUp:
            return

        if not self.macd.IsReady:
            return

        macd_line = self.macd.Current.Value
        signal_line = self.macd.Signal.Current.Value

        if macd_line > signal_line and self.Portfolio[self.spy].Invested == 0:
            self.SetHoldings(self.spy, 1.0)  # Buy SPY

        elif macd_line < signal_line and self.Portfolio[self.spy].Invested > 0:
            self.Liquidate(self.spy)  # Sell SPY
