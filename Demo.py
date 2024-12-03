from typing import Annotated, Literal
import os
from autogen import UserProxyAgent, ConversableAgent, register_function

config_list = [
    {
        "base_url": "http://35.244.13.63:11434/v1",
        "model": "llama3.1:latest",
        "api_key": "ollama",
    }
]


operator = Literal["+", "-", "*", "/"]


"""def calculator(a: int, b: int, op: Annotated[operator, "op"]) -> int:
    if op == "+":
        return a + b
    elif op == "-":
        return a - b
    elif op == "*":
        return a * b
    elif op == "/":
        return a / b
    else:
        raise ValueError("Invalid operator")"""


assistant = ConversableAgent(
    name="Assistant",
    system_message="You are a helpful assistant You can help with simple calculations",
    llm_config={"config_list": config_list},
    human_input_mode="NEVER",
)

user_proxy = ConversableAgent(
    name="User",
    llm_config=False,
    is_termination_msg=lambda msg: msg.get("content") is not None
    and "TERMINATE" in msg["content"],
    human_input_mode="ALWAYS",
)

assistant.register_for_llm(name="calculator", description="A simple calculator")(calculator)

user_proxy.register_for_execution(name="calculator")(calculator)


register_function(
    calculator,
    caller=assistant,
    executor=user_proxy,
    name="calculator",
    description="A simple calculator",
)

chat_result = user_proxy.initiate_chat(assistant, message="Ask to the user")
