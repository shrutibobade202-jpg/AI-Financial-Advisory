from utils.central_logging import get_logger
from tools.search import rag_search_tool
from tools.yahoo_prices import yahoo_market_prices
from tools.taxes_analysis import analyze_tax_scenario
from tools.image_generation import generate_image
from tools.portfolio import calculate_weights,calculate_volatility_correlation,portfolio_analysis
from tools.perplexity import perplexity_live_search
from langchain_openai import ChatOpenAI
from agents.investment.investment_agent import create_investment_agent
from agents.tax.tax_agent import create_tax_agent
from agents.retirement.retirment_agent import create_retirement_agent
from typing import AsyncGenerator, Dict, List
from langchain_core.messages import HumanMessage, AIMessage,AIMessageChunk,ToolMessage

from agents.orchestrator.render_image import render_image_payload

from dotenv import load_dotenv
import pprint

import os
import json
import gc


logger = get_logger("orchestrator")


load_dotenv('../.env',override=True)

# Get our API keys
openai_api_key = os.getenv("OPENAI_API_KEY")


if openai_api_key:
    message = "Openai api  key has been set"
    logger.info(message)
else:
    message = "Error no openai api  key found"
    logger.error(message)


AGENT_COLORS = {
    "tax": "🟦",
    "investment": "🟩",
    "retirement": "🟪"
}


# Initialize our llm
llm = ChatOpenAI(
        model=  "gpt-4o-mini", #"gpt-4.1", #"gpt-4o-mini",
        temperature=0.3,
        max_tokens=400,
        streaming=True
    )

# Create agents
#calculate_weights
investment_tools = [rag_search_tool,perplexity_live_search,generate_image,calculate_volatility_correlation,portfolio_analysis,yahoo_market_prices]
investment_agent = create_investment_agent(llm,investment_tools)


tax_tools = [analyze_tax_scenario]
tax_agent = create_tax_agent(llm,tax_tools)


retirement_tools = []
retirement_agent = create_retirement_agent(llm,retirement_tools)


tools_registry = {
    "perplexity_live_search": perplexity_live_search,
    #"calculate_weights":calculate_weights,
    #"calculate_volatility_correlation":calculate_volatility_correlation,
    "portfolio_analysis":portfolio_analysis,
    "market_data": yahoo_market_prices,
    "rag_search_tool": rag_search_tool,
    "generate_image": generate_image,
    "analyze_tax_scenario": analyze_tax_scenario
}

agents = {
        "tax": tax_agent,
        "investment": investment_agent,
        "retirement": retirement_agent,
    }

INTENT_MAP = {
    "tax": [
        "tax", "deduction", "rrsp", "tfsa", "ira", "401k",
        "capital gains", "income tax", "reduce taxes"
    ],
    "investment": [
        "invest", "portfolio", "rebalance", "stocks",
        "etf", "allocation", "risk", "returns","current","market","live search"
    ],
    "retirement": [
        "retire", "retirement", "pension",
        "withdrawal", "rrsp", "ira", "401k", "fire"
    ]
}

PRIORITY = ["investment","tax", "retirement"]

"""
AGENT_MAP = {
    "investment": investment_agent,
    "tax": tax_agent,
    "retirement": retirement_agent
}
"""

def resolve_conflicts(agent_outputs):
    resolved = {}

    for key in PRIORITY:
        if key in agent_outputs:
            resolved[key] = agent_outputs[key]
    logger.info("Orchestrator conflict resolution")
    return resolved


    

def detect_intents(question: str) -> set[str]:
    question_lc = question.lower()
    intents = set()

    for intent, keywords in INTENT_MAP.items():
        if any(k in question_lc for k in keywords):
            intents.add(intent)
    logger.info("Intent detection")
    return intents


def route_agents(input_data):
    intents = detect_intents(input_data["question"])

    calls = []

    if "tax" in intents:
        calls.append(("tax", input_data))

    if "investment" in intents:
        calls.append(("investment", input_data))

    if "retirement" in intents:
        calls.append(("retirement", input_data))

    # Fallback
    if not calls:
        calls.append(("investment", input_data))  
    
    logger.info("Initialize routing")

    return calls


async def orchestrator_invoke(input_data):
    """
    Orchestrates a single user interaction by invoking the investment agent,
    streaming assistant responses, and handling tool calls in real time.

    This function is the central execution loop for the agent. It:
    - Builds the agent payload from user input and chat history
    - Streams model output incrementally (tokens, messages, or values)
    - Detects and executes tool calls (RAG, search, portfolio analysis, image generation, etc.)
    - Prevents duplicate tool execution during streaming
    - Converts tool outputs into structured messages consumable by the UI

    Supported behaviors:
    - Text streaming to the UI (partial and final responses)
    - Tool execution with strict tool_call_id tracking
    - Image tool handling (base64 → UI-renderable image)
    - Error-safe fallback when tools fail or return invalid payloads
    """

    taxes = json.loads(input_data['user']['taxes'])
    routing_plan = route_agents(input_data)
    results = {}
    executed_tool_ids = set()
    # Initial payload
    messages = [{"role": "user", "content": input_data}]
    payload = {"messages": messages}
    for agent_type, _ in routing_plan:
        agent = agents.get(agent_type)

        if not agent:
            continue

        
        logger.info(f"{agent_type.capitalize()} agent streaming response")

        partial_text = f"{AGENT_COLORS.get(agent_type, '')}**{agent_type.capitalize()} Output**:\n"

        async for event in agent.astream(payload, stream_mode="messages"):
            if isinstance(event, tuple):
                chunk_obj, metadata = event
            else:
                chunk_obj, metadata = event, {}

            if isinstance(chunk_obj, AIMessageChunk):
                chunk = chunk_obj.content or ""
                if chunk.strip():
                    partial_text += chunk
                    yield {
                        "role": agent_type,
                        "content": chunk,
                        "full_content": partial_text,
                        "final": False
                    }
               
                if getattr(chunk_obj, "tool_calls", None):
                    for tool_call in chunk_obj.tool_calls:
                        tool_name = tool_call.get("name")
                        tool_args = tool_call.get("args") or {}
                        tool_call_id = tool_call.get("id")                        
                        
                        if not tool_call_id or tool_call_id in executed_tool_ids:
                            continue

                        executed_tool_ids.add(tool_call_id)

                        if "query" not in tool_args:
                            tool_args["query"] = input_data["question"]
                            tool_args["user_id"] =  str(input_data['user']['user_id'])
                            tool_args["assets"] = input_data['user']['assets']
                            tool_args["liabilities"] = input_data['user']['liabilities']
                            tool_args["expenses"] = input_data['user']['expenses']
                            tool_args["risktolerance"] = input_data['user']['risk_tolerance']
                            tool_args["portfolio"] = input_data['portfolio']
                            tool_args["jurisdiction"] = input_data['jurisdiction']
                            tool_args["income"] = taxes['income'] 
                            tool_args["gains"] =  taxes['gains']
                            tool_args["deductions"] = taxes['deductions']
                            tool_args["tax_rate"] = taxes['tax_rate']
                            tool_args["cg_rate"] = taxes['cg_rate']
                            tool_args["goals"] = input_data['user']["goals"]
                                                    
                        if isinstance(tool_args, str):
                            try:
                                tool_args = json.loads(tool_args)
                                tool_args = {"query": tool_args}
                            except Exception as e:
                                logger.info(f"Tool requested: {tool_name}({tool_args})")
                        
                        tool = tools_registry.get(tool_name)

                        if not tool:
                            logger.info(f"Tool '{tool_name}' not found.")
                        else:
                            try:
                                tool_result = await tool.ainvoke(tool_args)
                                if tool_name == "generate_image":
                                        #print(f"tool_name: {tool_name}")
                                    yield {
                                        "tool_name": tool_name,
                                        "role": "image",
                                        "content": tool_result,
                                        "final": False}
                                    return
                            except Exception as e:
                                tool_result = f"Tool execution error: {str(e)}"

                        #ToolMessage is the official way to send a tool’s result back to the LLM
                        #tool_message = ToolMessage(
                         #   name=tool_name,
                         #   content=str(tool_result),
                          #  tool_call_id=tool_call_id)

                        #messages.append({
                        #    "role": "assistant",
                         #   "content": "",
                         #   "tool_calls": [tool_call]
                        #})

                        #messages.append({
                        #    "role": "tool",
                        #    "name": tool_name,
                        #    "content": str(tool_result)
                        #})

                        #payload = {"messages": messages}

                        yield {
                            "role": "tool_result",
                            "tool_name": tool_name,
                            "content": str(tool_result),
                            "full_content": partial_text,
                            "final": False
                        }


        
        results[agent_type] = partial_text
        yield {
            "role": agent_type,
            "content": partial_text,
            "full_content": partial_text,
            "final": True
        }

    
    if len(results) > 1:
        
        combined = "\n\n".join(
            f"**{k.capitalize()} Agent:**\n{v}"
            for k, v in results.items()
        )

        yield {
            "role": "orchestrator",
            "content": combined,
            "final": True
        }



