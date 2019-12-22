from flask import Flask, render_template, request
from scraper import scrape_one_ticker, scrape_SP500
from mooving_average import mooving_average_pred
from pred_comparison import comparator_prediction
from tomorrows_price import tomorrows_predicted_price

app = Flask('stock_predictor')


@app.route('/')
def home_page():
    return render_template('home.html')


@app.route('/inputticker')
def input_ticker():
    return render_template('inputticker.html')


@app.route('/predictprice', methods=['POST'])
def get_tomorrow_predicted_price():
    return tomorrows_predicted_price()


@app.route('/comparator', methods=("POST", "GET"))
def html_table():
    return comparator_prediction()


@app.route('/portfoliator')
def portfoliator():
    return render_template('portfoliator.html')


if __name__ == '__main__':
    app.run(port=5000, debug=True)
