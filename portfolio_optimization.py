#import packages
import requests
from bs4 import BeautifulSoup
import pandas as pd
import pandas_datareader as pdr
import numpy as np
import datetime
import cvxpy
import scraper

def portfolio_allocation():
    """Optmization of a convex problem. The algorithm is given the list
    of all the tickers of the S&P500. It then returns the best portfolio
    allocation to choose.

    Args:

    Returns:
        List of numbers between 0 and 1 that represent the % of your wealth
        that should be invested in each stock.
    """

    #we change the name of the tickers in the dataframe into a string format
    df_tickers = scraper.scrape_SP500()
    #we change the tickers to string to use it later in the get_data_yahoo function.
    df_tickers['tickers'].apply(str)


    #we create a new dataframe with tickers as columns.
    #we import the historical prices of our scraped stock on yahoo finance.
    data = pdr.get_data_yahoo(df_tickers['tickers'][0]).reset_index().drop([ 'High', 'Low', 'Open', 'Volume', 'Adj Close'], axis=1)
    data['Date'] = pd.to_datetime(data['Date'])
    # Set the datetime column as the index
    data.index = data['Date']
    df_reference = data.groupby(pd.Grouper(freq='M')).mean()
    #assign column name to ticker name
    df_reference.columns = [df_tickers['tickers'][0]]
    df_reference

    #We use df_reference as a basis for our dataframe and join it with other tickers' historical prices to create the full dataframe.
    for i in range(len(df_tickers[0:50])):
        data = pdr.get_data_yahoo(df_tickers['tickers'][i+1]).reset_index().drop([ 'High', 'Low', 'Open', 'Volume', 'Adj Close'], axis=1)
        data['Date'] = pd.to_datetime(data['Date'])
        # Set the datetime column as the index
        data.index = data['Date']
        data = data.groupby(pd.Grouper(freq='M')).mean()
        data.columns = [df_tickers['tickers'][i+1]]
        df_reference = df_reference.join(data)

    df_reference

    # We change index to number of months passed to facilitate plotting.
    df = df_reference.reset_index()
    df['Date'] = pd.to_datetime(df['Date'])
    df['Date'] = (df['Date'].dt.year - 2014) * 12 + df['Date'].dt.month - 12
    df.index = df['Date']
    df = df.drop(['Date'], axis=1)
    df

    # we compute monthly returns for each stock and create a new dataframe
    for ticker in df.columns:
        date_1st = df.index[0]
        price_0 = df[ticker][date_1st]
        for period in range(1,len(df.index)):
            date = df.index[period]
            price_1 = df[ticker][date]
            ret = (price_1-price_0)/price_0
            df.set_value(period, ticker, ret)
            price_0 = price_1

    df

    df = df.iloc[1:]

    #Computing the average expected return per stock.
    expected_return = df.as_matrix().T
    r = np.asarray(np.mean(expected_return, axis=1))

    # Covariance matrix
    covariance_matrix = np.asmatrix(np.cov(expected_return))
    covariance_matrix

    # This is the sample tickers'name.
    tickers = df.columns
    tickers

    x = cvxpy.Variable(n)

    ret = r.T*x

    # We express x^TAx.
    portfolio_return_variance = cvxpy.quad_form(x, covariance_matrix)
    portfolio_return_variance

    # We set up the minimum requirement return of portfolio
    required_return = 0.01

    # We use the same convex optimization package to specify our optimization problem.
    # The problem function allows us to specify our constraints.
    prob = cvxpy.Problem(cvxpy.Minimize(portfolio_return_variance), [sum(x)==1, ret >= required_return, x >= 0])
    # We compute the minimization of x^TAx.
    prob.solve()

    return x.value
