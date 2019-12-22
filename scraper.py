import requests
from bs4 import BeautifulSoup
import pandas as pd
import pandas_datareader as pdr


def scrape_one_ticker(ticker):
    """Web scraper that returns the 100 last values of a company's stock.

    Args:
        ticker: an upper case 3 or 4 letter word that represent a specific stock

    Returns:
        A dataframe of two columns: the date and the price of the stock at each period
    """

    data = {
        'Date': [],
        'Close': [],
    }

    try:
        url = "https://finance.yahoo.com/quote/{}/history?p={}".format(
        ticker, ticker)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        all_tr = soup.find_all('tr', {'class':
        'BdT Bdc($seperatorColor) Ta(end) Fz(s) Whs(nw)'})

        for row in all_tr:
            all_td = row.find_all('td')
            data['Date'].append(all_td[0].text)
            data['Close'].append(float(all_td[5].text.replace(",", "")))

        df = pd.DataFrame(data).reindex(
        index=pd.DataFrame(data).index[::-1]).reset_index().drop(
        ['index'], axis=1)

        if df.empty:
            df = pd.DataFrame(data=pdr.get_data_yahoo(ticker))[-100:]
            df = data.reset_index()
            df = df[["Date", "Close"]]
        else:
            return df

    except IndexError as error:
        data = pd.DataFrame(data=pdr.get_data_yahoo(ticker))[-100:]
        df = data.reset_index()
        df = df[["Date", "Close"]]

        return df

    except Exception as error:
        return "Could not find ticker."


def scrape_SP500():
    """ Web scraper of one wikipedia page
     that returns the tickers of all 500 firms the compose the S&P500.

    Args:

    Returns:
        A dataframe of one column with the 500 tickers name.
    """
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find('table', {'class': {'wikitable sortable'}})
    rows = table.find_all('tr')

    tickers = []

    for row in table.findAll('tr'):
        cells = row.findAll('td')
        if len(cells) > 0:
            tickers.append(cells[0].find(text=True))

    df = pd.DataFrame(tickers, columns=['tickers'])

    return df
