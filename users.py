import pandas as pd
import json
from llama_index.core import Document

class HandleUsers:
    def __init__(self,path:str):
        self.path = path
    
    def load_user_profiles(self) -> pd.DataFrame:
        users_df = pd.read_csv(self.path)
        return users_df

    def row_profile_to_json(self,row):
        return {
            "user_id":row["user_id"],
            "name":row["name"],
            "assets":row["assets"],
            "liabilities":row["liabilities"],
            "expenses":row["expenses"],
            "goals":row["goals"],
            "risk_tolerance":row["risk_tolerance"]
        }    
    
    def save_profiles(self,df,out_path="profiles/user_profiles.json"):
        profiles = [self.row_profile_to_json(r) for _, r in df.iterrows()]
        with open(out_path,"w",encoding="utf-8") as file:
            json.dump(profiles,file,indent=2)
        return profiles

    
    def profile_to_document(self,profile: dict) -> Document:
        
        text = f"""
    User financial profile:
    Assets: {profile['assets']}
    Liabilities: {profile['liabilities']}
    Expenses: {profile['expenses']}
    Goals: {profile['goals']}
    Risk tolerance: {profile['risk_tolerance']}
    """
        return Document(
            text=text.strip(),
            metadata={
                "user_id": profile["user_id"],
                "type": "user_profile",
                "risk_tolerance": profile["risk_tolerance"]
            }
        )
    
    def get_user_portfolio(self,path:str,user_id:str):
        portfolios_df = pd.read_csv(path)
        user_portfolio_df = portfolios_df.where(portfolios_df['user_id'] == user_id)
        user_portfolio_df = user_portfolio_df.dropna(how="all")
        return user_portfolio_df