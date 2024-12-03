from autogen import AssistantAgent,ConversableAgent,UserProxyAgent,register_function

config_list=[
    {
        "base_url": "http://35.244.13.63:11434/v1",
        "model": "llama3.1:latest",
        "api_key": "ollama",
    }
]


task="""you are a helpful ai assistant .Ask to the user to provide the details of name, age, email and phone number only.
Dont ask any other things. these four details is mandatory to collect, there is no need to go if not collect these items.
After details are collected store in to the user_details dictionary"""

fields = ["name", "age", "email", "phone_number"]

user_details = {}

def collect_user_details(name="",age=None,email="",phone_number="1234567890"):    
    global user_details     
    
    print('x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x')
    
  
    
    for field in fields:
       
        response=user_proxy.initiate_chat(assistant,message=task)
         
        value = response.human_input(f"{field}: ")     
        user_details[field] = value.strip() 
    
    return user_details

assistant=ConversableAgent(
    name="Assistant",
    system_message=task,
    llm_config={"config_list": config_list},
    human_input_mode="NEVER"
)

user_proxy=ConversableAgent(
    name="User",
    llm_config={"config_list": config_list} ,code_execution_config={"use_docker": False},
    human_input_mode="ALWAYS"
)

assistant.register_for_llm(name="UserDetails", description=task)(collect_user_details)


register_function(
    collect_user_details,
    caller=assistant,
    executor=user_proxy,
    name="UserDetails",
    description="Collect the details of the user"
)

response= user_proxy.initiate_chat(assistant, message=task)

print(user_details)