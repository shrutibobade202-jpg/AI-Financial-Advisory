import gradio as gr
from llama_index_instrumentation.span_handlers import null
import pandas as pd
import json
from utils.central_logging import setup_logging,get_logger
from user.user import get_user_portfolio,dict_to_table
from ui.chat_handlers import stream_response
import gc





setup_logging()
logger = get_logger("profile")

try:
    with open("./profiles/user_profiles.json") as file:
        profiles = json.load(file)
except Exception as e:
    logger.exception(f"Profile exception occured: {e}")


input_data = None



def load_profile(index:int):

    profile = profiles[index]
    user_portfolio = get_user_portfolio("./profiles/all_users_portfolio.csv",profile['user_id']).to_json( orient="records")
    portfolios =  json.loads(user_portfolio)
    stock_list = [[portfolio['ticker'], portfolio['quantity'], portfolio['price']] for portfolio in portfolios]
    update_profile(profile,user_portfolio,index)
    

    return (
        dict_to_table(json.loads(profile['assets'])),
        dict_to_table(json.loads(profile['liabilities'])),
        dict_to_table(json.loads(profile['expenses'])),
        dict_to_table(json.loads(profile['goals'])),
        [
        ['risk_tolerance',profile['risk_tolerance']],
        ['name',profile['name']]
        ],
        stock_list,
        dict_to_table(json.loads(profile['taxes'])),
        index)

def update_profile(profile,user_portfolio,index):
    global input_data
    input_data = {
        "user": profile,
        "portfolio": user_portfolio,
        "jurisdiction": "CA",
        "profile_id": index,
    }


load_profile(0)

def launch_ui():

    with gr.Blocks(title="📊 Financial Overview") as demo:
        
        selected_profile_state = gr.State(0)
        input_data_state = gr.State(input_data)
        #tax_agent_state = gr.State(tax_agent)
        #investment_agent_state = gr.State(investment_agent)
        #retirement_agent_state = gr.State(retirement_agent)
        with gr.Row():
                btn1 = gr.Button(f"👤 {profiles[0]['name']}")
                btn2 = gr.Button(f"👤 {profiles[1]['name']}")
                btn3 = gr.Button(f"👤 {profiles[2]['name']}")

        with gr.Row():

            with gr.Column(scale=1.5):    
                with gr.Tabs():

                    with gr.Tab("Assets"):
                        assets_table = gr.Dataframe(headers=["Cash","Stocks","Bonds","Real Estate","Retirement Accounts"])

                    with gr.Tab("Liabilities"):
                        liabilities_table  = gr.Dataframe(headers=["Credit Card","Auto Loan","Mortgage","Student loan"])

                    with gr.Tab("Expenses"):
                        expenses_table = gr.Dataframe(headers=["Housing","Utilities","Food","Transport","Insurance","Entertainment","Other"])
                    
                    with gr.Tab("Goals"):
                        goals_table = gr.Dataframe(headers=["Short", "Mid","Long"])
                        
                    with gr.Tab("Risks"):
                        risks_table = gr.Dataframe(headers=["Risk Tolerance","Name"])

                    with gr.Tab("Portfolio"):
                        portfolio_table = gr.Dataframe(headers=['ticker','quantity','price'])
                
                    with gr.Tab("Taxes"):
                        taxe_table = gr.Dataframe(headers=["title","value"])
                        
            with gr.Column(scale=1.5):
                #chatbot = gr.Chatbot(height=400,show_label=False, render_markdown=True,type="messages")
                gr.Markdown("### 💬 Ask your Financial Advisor")

                chatbot = gr.Chatbot(height=450)

                user_input = gr.Textbox(placeholder="Ask about investments, taxes, or retirement...",show_label=False)

                #send_btn = gr.Button ("Send") 
                
        demo.load(
             fn=lambda: load_profile(0),
             outputs=[assets_table, liabilities_table, expenses_table, goals_table,risks_table, portfolio_table,taxe_table,selected_profile_state]
        )

        btn1.click(
                fn=lambda: load_profile(0),
                outputs=[assets_table, liabilities_table, expenses_table, goals_table,risks_table, portfolio_table,taxe_table,selected_profile_state])
            
        btn2.click(
                fn=lambda: load_profile(1),
                outputs=[assets_table, liabilities_table, expenses_table, goals_table,risks_table, portfolio_table,taxe_table,selected_profile_state])
            
        btn3.click(
                fn=lambda: load_profile(2),
                outputs=[assets_table, liabilities_table, expenses_table, goals_table,risks_table, portfolio_table,taxe_table,selected_profile_state])
        

        #print(f"user_input: {user_input}")
        #print(f"selected_profile_state: {selected_profile_state}")
        #send_btn.click(fn=stream_response,inputs=[user_input, chatbot, selected_profile_state],outputs=[chatbot,user_input],queue=True)

        user_input.submit(fn=stream_response,inputs=[user_input, chatbot, selected_profile_state,input_data_state],outputs=[chatbot,user_input],queue=True)

    #demo.launch()
    demo.queue(default_concurrency_limit=64)
    demo.launch(debug=True, share=False)


    
