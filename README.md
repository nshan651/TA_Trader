# TA-Trader

## Overview ## 

TA-Trader is an alogrithmic trader that uses technical analysis to buy and sell securities.

* Data Retrieval: retrieves closing price data from yfinance and saves to file
* Calculations: calculates the technical indicators needed for the strategy
* Analysis & Execution: uses technical indicators to place trades

***
## Trading Strategy ##

I used the **Moving Average Convergence Divergence (MACD)** technical indicator for my trading strategy. The MACD has three main components. 

![alt text](images/macd_eq.jpg?raw=True "Data Header format.")
<br><br>
First, there is the 12-day and 26-day **Exponential Moving Averages (EMA)** which represent a fast and a slow period. The fast period minus the slow period gives us the MACD.

![alt text](images/ema_eq.jpg?raw=True "Data Header format.")
<br><br>
Second is the **signal line**, which is the 9-day EMA of the MACD line. 

![alt text](images/signal_eq.jpg?raw=True "Data Header format.")
<br><br>
The final element is the MACD minus the signal line, which is also known as the **histogram**. This is useful for identifying changes in momentum, and is what I will mainly be using.

I used a basic MACD crossover strategy, where I looked for buy and sell signals based on the histogram. Specifically, I opened positions when the histogram was went above 0.05, and I closed existing positions when the signal line went below -1.

Facebook's MACD Chart Data:
![alt text](images/macd_ex_tos.jpg?raw=True "Data Header format.")
*Example image taken from thinkorswim trading platform*

There is not necessarily a definitive buy and sell target when using a crossover strategy such as this one. Experiement and determine what works best for your strategy. In my case, I set my sell line to -1, because I was experiencing a lot of market "fake-outs", where histogram would bottom out at around -1 then shoot back up.
***
## Technologies and Services ##

* yfinance for data
  - I tried out several different data vendors, but ultimately settled on yfinance as a data source because of their free and mostly reliable data
  - The other implementations are available as well
* Alpaca as paper trading broker
  - I used the Alpaca API as a paper trading broker to facilitate my trades



        

  
