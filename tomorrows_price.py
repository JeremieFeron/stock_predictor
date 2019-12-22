from flask import Flask, render_template, request
from scraper import scrape_one_ticker, scrape_SP500
from mooving_average import mooving_average_pred
from pred_comparison import comparator_prediction


def tomorrows_predicted_price():
    """
    Passes the Ticker argument to the prediction and scrape functions
    to compute the predicted price

    Args:
        Ticker: the company ticker inputed by the user
        Predictprice: the output of mooving_average_pred for the Ticker

    Returns:
        A float: The predicted price for tomorrow in $
    """

    if request.method == 'POST':
        # Get the ticker the user inputed
        ticker = request.form['ticker']
        # Pass the argument to our scrape function
        data = scrape_one_ticker(ticker)
        # Launch the predicting model on the output of the scrape function
        predictprice = mooving_average_pred(data)

        return render_template('predictprice.html', ticker=ticker,
                predicted_price=predictprice)
