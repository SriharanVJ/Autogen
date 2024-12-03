from autogen import ConversableAgent, register_function

# Configuration for the assistant
config_list = [
    {
        "base_url": "http://35.244.13.63:11434/v1",
        "model": "llama3.1:latest",
        "api_key": "ollama"
    }
]

task="""you are a helpful ai assistant .
Dont write the execution code on terminal and dont ask the extra details to the user,
ask only what is available in the function.then execute the function of collect patient details
and collect the details of the patient and store it in the dictionary and return the dictionary."""
# Dictionary to store patient details
user_details = {}

# Function to collect patient details
def collect_patient_details():
    global user_details
    details = ["name", "age", "email", "ph_no"]  # Fields to collect
    for item in details:
        # Prompt the user for each detail
        response = user_proxy.initiate_chat(
            assistant, 
            message=f"Please provide your {item}:"
        )
        # Extract response text
        value = response.human_input("text","").strip()
        user_details[item] = value # Store in dictionary
    
    return user_details

# Set up the Assistant Agent
assistant = ConversableAgent(
    name="Assistant",
    system_message="You are a helpful assistant. Collect the details of the user using the function.",
    llm_config={"config_list": config_list},
    human_input_mode="NEVER"
    
)

# Set up the User Proxy Agent
user_proxy = ConversableAgent(
    name="User",
    llm_config={"config_list": config_list} ,code_execution_config={"use_docker": False},
    human_input_mode="ALWAYS"
    
    
)

# Register the collect_patient_details function
assistant.register_for_llm(name="collect_patient_details", description="Collect the details of the user")(collect_patient_details)

# Connect the assistant and user proxy for execution
register_function(
    collect_patient_details,
    caller=assistant,
    executor=user_proxy,
    name="collect_patient_details",
    description="Collect the details of the user"
)

# Initiate chat and collect details
response= user_proxy.initiate_chat(assistant, message=task)

# Print collected details
print("Collected Patient Details:")
for key,value in user_details.items():    
    print(f"{key}: {value}")

