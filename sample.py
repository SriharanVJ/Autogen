from autogen import ConversableAgent, UserProxyAgent
import psycopg2

# Database configuration
DB_HOST = "localhost"
DB_NAME = "TestCase1"
DB_USER = "postgres"
DB_PASS = "........"

# Establishing connection to the PostgreSQL database
con = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASS
)
cur = con.cursor()

# Configuration for the language model
config_list = [
    {
        "base_url": "http://35.244.13.63:11434/v1",
        "model": "llama3.2:latest",
        "api_key": "ollama"
    }
]

# Function to handle patient information insertion into DB
def patient_info(name, email, phone):
    try:
        # Insert patient information into the database
        cur.execute("""
            INSERT INTO patient (name, email, phone_number) 
            VALUES (%s, %s, %s);
        """, (name, email, phone))
        con.commit()
        print(f"Patient record for {name} added successfully!")
        return f"Patient record for {name} has been added."
    except Exception as e:
        print(f"Error inserting patient info: {e}")
        return f"Failed to add patient record for {name}. Please try again."

# Task description for the assistant
task = f"""
You are a helpful assistant.
1. Ask the user for their details like Name, Age, Email, and Phone Number.
2. Store these details in variables name, age, email, and phone_number.
3. Confirm the details with the user.
4. Ask the user to select a problem from the following list: fever, cold, cough, accident, headache, stomachache.
5. Based on the user's selection, show the related doctors.
6. Ask the user to choose a doctor and their preferred time.
7. Confirm the appointment with the user.
"""

# Creating the patient table if not already created
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

# Initialize ConversableAgent
conversable_agent = ConversableAgent(
    name="patient_info_collect",
    llm_config={"config_list": config_list},
    description="Collect and store patient information"
)

# Initialize UserProxyAgent
user_proxy = UserProxyAgent("user", code_execution_config={"use_docker": False})

# Start the conversation with the agent
response = user_proxy.initiate_chat(conversable_agent, message=task)

# Extract patient details (assuming the assistant has collected this info)
try:
    user_message = response.chat_history
    print(f"Chat history: {user_message}")

    # Assuming the assistant collects patient details in the response
    # Extract the details from the user message (customize as per actual response structure)
    name = user_message.get('name', '')
    email = user_message.get('email', '')
    phone_number = user_message.get('phone_number', '')

    # Call the patient_info function to update the database
    result = patient_info(name, email, phone_number)
    print(result)

except Exception as e:
    print(f"Error processing user message: {e}")

# Close the cursor and database connection
cur.close()
con.close()
print("Connection is closed")
