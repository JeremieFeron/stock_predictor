import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
from scraper import scrape_one_ticker, scrape_SP500
import pandas_datareader as pdr


def mooving_average_pred(data):
        """Makes stock price prediction on 1-500 firms of the S&P500 firms.
        The prediction is a weighted average of the last 20 days' prices.

        Args:
            ticker: an upper case 3 or 4 letter word that represents a specific stock.

        Returns:
            The predicted price.
        """
        window = round(len(data)*0.2)
        num = 0
        denom = 0
        for j in range(window):
            num += j*(data.Close[len(data) - window + j])
            denom += j
        return num / denom

#-------------------------------------------------------------------------------

# #Creating new dataframe with only Date & closing columns
# df = pd.DataFrame(scrape(ticker), columns=['Date', 'Close', 'SMA', 'EMA_Short',
# 'EMA_Long'])
# df.Close = np.around(df.Close, decimals=2)
#
# window = round(len(df)*0.2)

#-------------------------------------------------------------------------------

#Simple Moving Average
# def sma_price(ticker):
#     """Makes stock price prediction on 1-500 firms of the S&P500 firms.
#     The prediction is a simple moving average (SMA) of 20 days' prices.
#
#     Args:
#         ticker: an upper case 3/4 letter word that represents a specific stock.
#
#     Returns:
#         The table of closing prices with a column listing the predicted prices
#         as per SMA.
#     """
#
#     preds=[]
#     for i in range(window):
#         x = df.Close[(len(df) - 2*window + i):(len(df) - window + 1)].sum() + sum(preds)
#         x_mean = x/window
#         preds.append(np.around(x_mean, decimals=2))
#         df['SMA'][len(df) - window + i] = preds[i]
#
#     return df

#-------------------------------------------------------------------------------

#Exponential Moving Average
# def ema_price():
#     """Makes stock price prediction on 1-500 firms of the S&P500 firms.
#     The prediction is an exponential moving average.
#     There are 2 predictions:
#     one based on 20 days' prices, and the other on 20% of the given prices.
#
#     Args:
#
#     Returns:
#         The table of closing prices with a column listing the predicted prices
#         as per SMA.
#     """
#
#     df['EMA_Short']  = round(df.ewm(span=20, adjust=False).mean(), 2)
#     df['EMA_Long'] = round(df.ewm(span=window, adjust=False).mean(), 2)
#
#     return df

#root mean squared error between price and sma, ema_short, ema_long
#-------------------------------------------------------------------------------


# def meansqerror():
#     """Calculates root mean squared error (RMSE) of the moving avg predictions.
#
#         Args:
#
#         Returns:
#             The RMSE of SMA, EMA(short) and EMA(long).
#         """
#     rms_sma=np.sqrt(mean_squared_error(np.array(df['Close'][(len(df) - window) :]),
#     np.array(df['SMA'][(len(df) - window) :])))
#     rms_ema_short=np.sqrt(mean_squared_error(np.array(df['Close']),
#     np.array(df['EMA_Short'])))
#     rms_ema_long=np.sqrt(mean_squared_error(np.array(df['Close']),
#     np.array(df['EMA_Long'])))
