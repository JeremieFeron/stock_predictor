import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
from scraper import scrape_one_ticker, scrape_SP500
import pandas_datareader as pdr
from flask import Flask, render_template, request

def comparator_prediction():
    """Makes stock price prediction on 1-500 firms of the S&P500 firms.
    The prediction is only the mean of the previous stock prices.

    Args:

    Returns:
        A dataframe of four columns: the tickers' names, the last closing price
        of each ticker, the prediction price and the difference between the
        latter two numbers .
    """
    df = scrape_SP500()
    df['tickers'].apply(str)

    table = {
            'tickers': [],
            'prediction': [],
            'closing_price': [],
            'difference': [],
        }

    for i in range(len(df[0:30])):
        data = pdr.get_data_yahoo(df['tickers'][i]).tail(100).reset_index().drop(
        ['Date', 'High', 'Low', 'Open', 'Volume', 'Adj Close'], axis=1)
        table['tickers'].append(df['tickers'][i])
        table['closing_price'].append(data["Close"].iloc[-1])
        table['prediction'].append(data['Close'].mean())

        difference = np.around((float(data['Close'].mean()) - float(
        data["Close"].iloc[-1]))/ (float(data["Close"].iloc[-1])), decimals=3)
        table['difference'].append(difference)


    df = pd.DataFrame(table,columns=[
    'tickers', 'prediction', 'closing_price', 'difference']).sort_values(
    ['difference'])

    return render_template('comparator.html',
    tables=[df.to_html(classes="table")], titles=df.columns.values)
