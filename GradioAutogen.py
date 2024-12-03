from autogen import AssistantAgent, UserProxyAgent
import gradio as gr
from datetime import datetime

def run_assistant(message):
    config_list=[
      {
        "base_url":"http://35.244.13.63:11434/v1",
        "model":"llama3.2:latest",
        "api_key":"ollama"
     }
    ]

    assistant=AssistantAgent("AI",llm_config={"config_list":config_list})
    user_proxy=UserProxyAgent("USER",code_execution_config={"work_dir":"write_code","use_docker":False},human_input_mode="NEVER")

    task="""  you are an ai what question the user ask tell the answer"""

    
    response=user_proxy.initiate_chat(assistant,message=task)
    return response

ui=gr.Interface(fn=run_assistant,inputs="text",outputs="text",title="CodeLlamaAssistant")
ui.launch(share=True)