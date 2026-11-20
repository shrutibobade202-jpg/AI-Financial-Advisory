# Required libraries
import os
import logging
from dotenv import load_dotenv
load_dotenv(override=True)
import json
from users import HandleUsers

from langchain_openai import ChatOpenAI
from utils.central_logging import setup_logging,get_logger
from tools.perplexity import perplexity_live_search
from tools.search import rag_search_tool
from tools.yahoo_prices import yahoo_market_prices
from tools.taxes_analysis import analyze_tax_scenario
from tools.portfolio import calculate_weights,calculate_volatility_correlation,portfolio_analysis

from agents.investment.investment_agent import create_investment_agent
from agents.tax.tax_agent import create_tax_agent
from agents.retirement.retirment_agent import create_retirement_agent
from agents.orchestrator.orchestrator_agent import orchestrator_invoke
from langchain_core.messages import AIMessage, ToolMessage
from tools.search import warmup
from ui.gradio_app import launch_ui

from typing import Generator
from langchain_core.messages import HumanMessage
from langchain.agents import create_agent



# Logging basic configuration
#logger = logging.getLogger(__name__)
#logging.basicConfig(level=logging.INFO)
#logging.getLogger('httpx').setLevel(logging.WARNING)

# Setup logging
setup_logging()




def main():
    launch_ui()

if __name__ == "__main__":
    warmup()
    main()