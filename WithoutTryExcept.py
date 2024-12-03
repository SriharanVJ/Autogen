from autogen import AssistantAgent,UserProxyAgent
from sqlalchemy import create_engine


database_url="postgresql+psycopg2://postgres:........@localhost:5432/TestCase1"

engine=create_engine(database_url)

con=engine.connect()



config_list=[
    
    {
        "base_url":"http://35.244.13.63:11434/v1",
        "model":"llama3.2:latest",
        "api_key":"ollama"
    }
]

assistant=AssistantAgent("Ai",llm_config={"config_list":config_list})

user_proxy=UserProxyAgent("user",code_execution_config=False)


problem=["fever","cold","cough","accident","headache","stomachache"]
problem_list=', '.join(problem)

doctors = {
    "fever": [
        {"id":1, "name": "Ram", "available_times": ["9:00 AM - 2:00 PM"]},
        {"id":2,"name": "Sam", "available_times": ["2:00 PM - 8:00 PM"]}
    ],
    "cold": [
        {"id":3,"name": "Krishnan", "available_times":  ["9:00 AM - 2:00 PM"]},
        {"id":4,"name": "Raman", "available_times":["2:00 PM - 8:00 PM"]}
    ],
    "cough": [
        {"id":5,"name": "Sanjay", "available_times":  ["9:00 AM - 2:00 PM"]},
        {"id":6,"name": "Samy", "available_times": ["2:00 PM - 8:00 PM"]}
    ],
    "accident": [
        {"id":7,"name": "Venkat", "available_times":  ["9:00 AM - 2:00 PM"]},
    ],
    "headache": [
        {"id":8,"name": "Naidu", "available_times":  ["9:00 AM - 2:00 PM"]},
    ],
    "stomacache": [
        {"id":9,"name": "Balu", "available_times":  ["9:00 AM - 2:00 PM"]},
        {"id":10,"name": "Balaji", "available_times": ["2:00 PM - 8:00 PM"]}
    ]
}

task = f"""
You are a helpful assistant.
you dont write the code and aythinh on terminal, only ask details of the user

1. properly Ask the user for their details like please tell Name, Age, Email, and Phone Number.
2. Store only the details provide by user Name, Age, Email, and Phone Number in variables named
name, age, email, and phone_number.ensure all the details collected and confirm with the user these are correct show it
3. If the user doesn't provide these details don't move on next step, ask repeatedly for the missing information.
4. If all details are collected, display the following list of problems and prompt the user to select one:
{', '.join(problem)}.
5. Based on the user's selection, display the related doctors from this dictionary:
{doctors}.
6. Ask the user to choose a doctor and their preferred time as mentioned with doctor.
7. Confirm the appointment with the user.
"""
cur=con.cursor()
print(task)

cur.execute("""
    CREATE TABLE IF NOT EXISTS patient(
        id SERIAL PRIMARY KEY NOT NULL,
        name VARCHAR(200) NOT NULL,
        age VARCHAR(200) NOT NULL,
        email VARCHAR(200) NOT NULL,
        phone_number VARCHAR(100) NOT NULL
        
    );
""")
print("Table successfully created")
response=user_proxy.initiate_chat(assistant,message=task)

print('check, when this line will be executed?')



user_message = response.chat_history      
    
name = user_message
age = user_message
email = user_message
phone_number = user_message
    
    
cur.execute("""
        INSERT INTO patient (name, age, email, phone_number) 
        VALUES (%s, %s, %s, %s);
    """, (name, age, email, phone_number))
print(f"Record for {name} added successfully!")
    
con.commit()


cur.close()
con.close()
print("Connection is closed")
