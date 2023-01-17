# Trading-Analysis
Python script to test trading strategies on price data from the past.

The history of prices must be stored in a file named price.csv. The given price.csv contains daily bitcoin prices from 2021. 

main.py should be used to run the strategies one wishes to study or compare, and do the relevant statistical analysis. The given main.py simply tests all the preset strategies.

indicators.py should be used to store indicators. The Simple Moving Average (SMA) and the Relative Strength Index (RSI) are already implemented.

strategies.py should be used to store strategies. It contains the Portfolio class, with 'cash' and 'assets' as attributes, and methods to update them. It also contains the Position class, that allows to describe Long or Short trading positions with a target price, stop-loss price, and time expiration. Several preset strategies are also present, including a commonly used sma-rsi combination strategy.
