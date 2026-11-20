import pandas as pd


def get_user_portfolio(path:str,user_id:str):
    portfolios_df = pd.read_csv(path)
    user_portfolio_df = portfolios_df.where(portfolios_df['user_id'] == user_id)
    user_portfolio_df = user_portfolio_df.dropna(how="all")
    return user_portfolio_df

def dict_to_table(d):
    return [[k, v] for k, v in d.items()]