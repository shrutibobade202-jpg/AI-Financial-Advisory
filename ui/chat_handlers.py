import json
import os

from utils.central_logging import setup_logging,get_logger
import time
from agents.orchestrator.orchestrator_agent import orchestrator_invoke
from langchain_core.messages import HumanMessage, AIMessage
import asyncio
import gradio as gr 
from PIL import Image

async def stream_response(message, history, profile_id, input_data):
    
    input_data = dict(input_data) 
    input_data["profile_id"] = profile_id
    input_data["question"] = message
    tools_list = set()

    history = history or []
    history.append({"role": "user", "content": message})
    yield  history, ""  
    # Stream assistant events
    async for event in orchestrator_invoke(input_data):
        role = event.get("role", "")
        content = event.get("content", "")
        tool_name = event.get("tool_name","")

        if history and history[-1]["role"] == "assistant":
            history[-1]["content"] += content
        else:
            if tool_name == "generate_image" and content !="":
                history.append({"role": "assistant", "content": gr.Image(content, show_label=False)})
                yield history, ""
            else:
                history.append({"role": "assistant", "content": content})
        yield  history,""  
