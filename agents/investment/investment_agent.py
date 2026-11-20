from langchain.agents import create_agent
from .investment_prompt import get_investment_prompt
from utils.central_logging import setup_logging,get_logger
from typing import TypedDict, List
from langchain_core.prompts import ChatPromptTemplate
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables import RunnableLambda

setup_logging()
# Create a logger instance
logger = get_logger("investment")




class AgentState(TypedDict):
    messages: List


def create_investment_agent(llm, tools=[]):
    try:
        llm = llm.bind_tools(tools)

        system_prompt = get_investment_prompt()
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}")
        ])

        agent_runnable = prompt | llm
        tool_node = ToolNode(tools)

        graph = StateGraph(AgentState)

        def llm_node(state: AgentState):
            if not state.get("messages"):
                return state

            last_msg = state["messages"][-1]
            last_content = last_msg.content if hasattr(last_msg, "content") else last_msg["content"]

            response = agent_runnable.invoke({"input": last_content})

            return {"messages": state["messages"] + [response]}

        graph.add_node("llm", RunnableLambda(llm_node))
        graph.add_node("tools", tool_node)

        # 🔁 Conditional routing
        def route_after_llm(state: AgentState):
            last_msg = state["messages"][-1]
            if isinstance(last_msg, AIMessage) and last_msg.tool_calls:
                return "tools"
            return "__end__"

        graph.add_conditional_edges("llm", route_after_llm)
        graph.add_edge("tools", "llm")

        graph.set_entry_point("llm")

        return graph.compile()

    except Exception as e:
        logger.exception(f"Exception during investment agent creation: {e}")
        raise