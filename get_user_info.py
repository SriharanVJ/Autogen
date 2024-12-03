from autogen import AssistantAgent, UserProxyAgent
import psycopg2

DB_HOST = "localhost"
DB_NAME = "TestCase1"
DB_USER = "postgres"
DB_PASS = "........"  


con = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASS
)
cur = con.cursor()


cur.execute("""
    CREATE TABLE IF NOT EXISTS reception(
        id SERIAL PRIMARY KEY NOT NULL,
        name VARCHAR(200) NOT NULL,
        age VARCHAR(200) NOT NULL,
        email VARCHAR(200) NOT NULL,
        phone_number VARCHAR(10) NOT NULL
    );
""")
print("Table successfully created.")


config_list = [
    {
        "base_url": "http://35.244.13.63:11434/v1",
        "model": "llama3.2:latest",
        "api_key": "ollama"
    }
]


assistant = AssistantAgent("Ai", llm_config={"config_list": config_list})
user_proxy = UserProxyAgent("user", code_execution_config={"use_docker": False})

problem = ["fever", "cold", "cough", "accident", "headache", "stomachache"]
problem_list = ', '.join(problem)

doctors = {
    "fever": [
        {"id": 1, "name": "Ram", "available_times": ["9:00 AM - 2:00 PM"]},
        {"id": 2, "name": "Sam", "available_times": ["2:00 PM - 8:00 PM"]}
    ],
    "cold": [
        {"id": 3, "name": "Krishnan", "available_times": ["9:00 AM - 2:00 PM"]},
        {"id": 4, "name": "Raman", "available_times": ["2:00 PM - 8:00 PM"]}
    ],
    "cough": [
        {"id": 5, "name": "Sanjay", "available_times": ["9:00 AM - 2:00 PM"]},
        {"id": 6, "name": "Samy", "available_times": ["2:00 PM - 8:00 PM"]}
    ],
    "accident": [
        {"id": 7, "name": "Venkat", "available_times": ["9:00 AM - 2:00 PM"]}
    ],
    "headache": [
        {"id": 8, "name": "Naidu", "available_times": ["9:00 AM - 2:00 PM"]}
    ],
    "stomacache": [
        {"id": 9, "name": "Balu", "available_times": ["9:00 AM - 2:00 PM"]},
        {"id": 10, "name": "Balaji", "available_times": ["2:00 PM - 8:00 PM"]}
    ]
}

task = f"""
You are a helpful assistant.
you dont write the code and aythinh on terminal, only ask details of the user

1. Ask the user for their details: Name, Age, Email, and Phone Number.
2. Store these details in variables: name, age, email, and phone_number.
3. If the user doesn't provide these details don't move on next step, ask repeatedly for the missing information.
4. If all details are collected, display the following list of problems and prompt the user to select one:
{', '.join(problem)}.
5. Based on the user's selection, display the related doctors from this dictionary:
{doctors}.
6. Ask the user to choose a doctor and their preferred time as mentioned with doctor.
7. Confirm the appointment with the user.
"""


response = user_proxy.initiate_chat(assistant, message=task)


name = "unknown"
age = "00"
email = "unknown@example.com"
phone_number = "0000000000"

try:
  
    user_message = response.chat_history[2]['content']

    
    if "\n" in user_message:
        user_data = user_message.split('\n')
    else:
        user_data = user_message.split()

    
    

    
    
    name = user_data[0]
    age = user_data[1]
    email = user_data[2]
    phone_number = user_data[3]

    
    if name == "unknown" or age == "00" or email == "unknown@example.com" or phone_number == "0000000000":
        raise ValueError("Invalid user data. Please ensure all fields are filled.")

    
    cur.execute("""
        INSERT INTO reception (name, age, email, phone_number) 
        VALUES (%s, %s, %s, %s);
    """, (name, age, email, phone_number))
    print(f"Record for {name} added successfully!")

except Exception as e:
    print(f"Error: {e}")

con.commit()
cur.close()
con.close()
print("Connection is closed")
