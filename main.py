from AlgorithmImports import *


class Learningalgotrade(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2008, 1, 1)
        self.SetEndDate(2023, 5, 31)
        self.SetCash(100000)  # Set initial capital

        self.spy = self.AddEquity("SPY", Resolution.Minute)
        # self.spy.SetDataNormalizationMode(DataNormalizationMode.Raw)
        self.SetBrokerageModel(
            BrokerageName.InteractiveBrokersBrokerage, AccountType.Margin)

        self.fast_ma_period = 90  # Period for the fast moving average
        self.slow_ma_period = 200  # Period for the slow moving average
        self.fast_ma = self.SMA(self.spy.Symbol, self.fast_ma_period)
        self.slow_ma = self.SMA(self.spy.Symbol, self.slow_ma_period)

        # Warm-up the indicators with historical data
        self.SetWarmUp(100, Resolution.Minute)

    def OnData(self, data):

        if self.IsWarmingUp:
            return

        # Check if the 90-day moving average is above the 200-day moving average
        if self.fast_ma.Current.Value > self.slow_ma.Current.Value:
            if not self.Portfolio.Invested:
                self.Debug("Purchased SPY")
                self.SetHoldings("SPY", 1.0)  # Buy SPY

        # Check if the 90-day moving average is below the 200-day moving average
        elif self.fast_ma.Current.Value < self.slow_ma.Current.Value:
            if self.Portfolio.Invested:
                self.Debug("Sold SPY")
                self.Liquidate(self.spy.Symbol)  # Sell SPY
