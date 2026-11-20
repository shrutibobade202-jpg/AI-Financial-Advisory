from langchain.tools import tool
from user.user import get_user_portfolio
import pandas as pd

def _calculate_weights(porfolio_path:str,user_id:str)->str:
    output = []
    df = get_user_portfolio(porfolio_path,user_id)
    df["value"] = df["quantity"] * df["price"]
    total_value = df["value"].sum()
    df["weight"] = df["value"] / total_value
    output.append("📊 CURRENT PORTFOLIO WEIGHTS")
    output.append(df[["ticker", "value", "weight"]].to_string(index=False))
    output.append(f"\nTotal Portfolio Value: ${total_value:,.2f}")
    return "\n".join(output)

def _calculate_volatility_correlation(historical_prices_path:str = None)->str:
    output = []
    if historical_prices_path:
        prices = pd.read_csv(historical_prices_path, index_col=0, parse_dates=True)
        returns = prices.pct_change().dropna()

        mean_returns = returns.mean() * 252
        vol = returns.std() * np.sqrt(252)
        corr = returns.corr()
        output.append("\n📈 ANNUALIZED RETURNS")
        output.append(mean_returns.to_string())

        output.append("\n📉 ANNUALIZED VOLATILITY")
        output.append(vol.to_string())

        output.append("\n🔗 CORRELATION MATRIX")
        output.append(corr.to_string())

    return "".join(output)


@tool
def calculate_weights(porfolio_path:str,user_id:str)->str:
    """
    Calculate for a user portfolio the weights of his portfolio
    Args: 
     porfolio_path: path to portfolio CSV with columns [ticker, quantity, price]
     user_id: The id of the user portfolio so we can select user portfolio
    """
    return _calculate_weights(porfolio_path,user_id)

@tool
def calculate_volatility_correlation(historical_prices_path:str=None):
    """
     Perform volatility and correlation:
    - Computes returns, volatility, correlations (if historical data provided)
    Args: 
     historical_prices_path: CSV with date column + tickers as columns
    """
    return _calculate_volatility_correlation(historical_prices_path)

@tool
def portfolio_analysis(user_id:str,historical_prices_path:str = None)->str:
    """
    Perform portfolio analysis using pandas:
    - Calculates weights
    - Calculate for a user portfolio the weights of his portfolio
    - Computes returns, volatility, correlations (if historical data provided)
    Args: 
     porfolio_path: path to portfolio CSV with columns [ticker, quantity, price]
     user_id: The id of the user portfolio so we can select user portfolio
     historical_prices_path: CSV with date column + tickers as columns
    """
    output = []
    weights = _calculate_weights("./profiles/all_users_portfolio.csv",user_id)
    output.append(weights)
    volatility_correlation = _calculate_volatility_correlation(historical_prices_path)
    if volatility_correlation != "":
        output.append(volatility_correlation)
    
    return "".join(output)

