import pandas as pd
import yfinance as yf
from langchain.tools import tool

def fetch_yahoo_prices(
    tickers: list[str],
    period: str = "1mo",
    interval: str = "1d"
) -> pd.DataFrame:
    """
    Fetch adjusted close prices from Yahoo Finance.
    """
    data = yf.download(
        tickers,
        period=period,
        interval=interval,
        auto_adjust=True,
        progress=False,
        group_by="ticker"
    )

    # Handle single vs multi ticker format
    if len(tickers) == 1:
        prices = data["Close"].to_frame(name=tickers[0])
    else:
        prices = pd.concat(
            {t: data[t]["Close"] for t in tickers},
            axis=1
        )

    prices.index = pd.to_datetime(prices.index)
    prices = prices.dropna()
    return prices

def save_yahoo_prices_csv(
    tickers: list[str],
    path: str = "live_prices.csv",
) -> str:
    prices = fetch_yahoo_prices(tickers)
    prices.to_csv(path)
    return path

@tool 
def yahoo_market_prices(tickers:list[str],save=False) -> str:
    """
    Fetch historical adjusted close prices from Yahoo Finance.
    Args:
        tickers: List
    Returns:
       List of finace return by yahoo
    """
    prices = fetch_yahoo_prices(tickers)

    if save == True:
        save_yahoo_prices_csv(tickers,"profiles/live_prices.csv")

    return prices