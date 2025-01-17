import openai
import streamlit as st
from autogen.agentchat import ConversableAgent
from autogen.oai.client import OpenAIWrapper, OpenAIError

# Streamlit app title and introduction
st.title("Conversable Agent Chat App")
st.write("This app uses OpenAI's API to power intelligent agents that can chat with you.")

# Ensure the OpenAI API key is set correctly from Streamlit secrets
openai.api_key = st.secrets["API_KEY"]

# Define LLM config for the ConversableAgent
llm_config = {
    "model": "gpt-3.5-turbo",  # Specify the OpenAI model you're using
    "api_key": openai.api_key   # Pass the API key from Streamlit secrets
}

# Function to test if the OpenAI API key works and avoid API errors
def test_openai_api():
    try:
        # Test the OpenAI API with a simple prompt
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt="Say hello!",
            max_tokens=5
        )
        # Display the response from the API
        st.write("OpenAI API Test Response: ", response.choices[0].text.strip())
    except openai.OpenAIError as e:
        st.error(f"OpenAI API error: {e}")
        st.stop()  # Stop the app if the API test fails

# Call the function to test the OpenAI API
test_openai_api()

# Try to create ConversableAgent instances with error handling
try:
    # Create the first agent with the provided LLM config
    Agent_1 = ConversableAgent(
        name="Agent_1",
        llm_config=llm_config  # Pass the validated LLM configuration
    )

    # Optionally, create a second agent (you can remove this if only one agent is needed)
    Agent_2 = ConversableAgent(
        name="Agent_2",
        llm_config=llm_config  # Same configuration for the second agent
    )

    # Interact with Agent 1 and display the response
    agent_prompt = st.text_input("Type your message to Agent 1:", "Hello, how can you assist me?")
    
    if st.button("Send to Agent 1"):
        # Send the user's message to the agent and get a response
        agent_response = Agent_1.chat(agent_prompt)
        st.write("Agent 1's response: ", agent_response)

    # You can also add interactions with Agent 2 if needed
    agent2_prompt = st.text_input("Type your message to Agent 2 (optional):", "Hi Agent 2, what can you do?")
    
    if st.button("Send to Agent 2"):
        # Send the user's message to the second agent and get a response
        agent2_response = Agent_2.chat(agent2_prompt)
        st.write("Agent 2's response: ", agent2_response)

except OpenAIError as e:
    # Handle OpenAI-related errors (e.g., invalid API key, rate limits, etc.)
    st.error(f"Failed to initialize agent due to OpenAI error: {e}")
except Exception as ex:
    # Handle any other unexpected errors
    st.error(f"An unexpected error occurred: {ex}")
