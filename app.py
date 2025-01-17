import openai
import streamlit as st

# Function to initialize OpenAI API
def init_openai(api_key):
    openai.api_key = api_key

# Function to call OpenAI GPT model
def generate_response(prompt, model="gpt-3.5-turbo"):
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": prompt}]
        )
        return response['choices'][0]['message']['content']
    except openai.OpenAIError as e:
        return f"Error: {e}"

# Streamlit UI
st.title("Talking Agent")

# Input field for API key
api_key = st.text_input("Enter your OpenAI API Key", type="password")
prompt = st.text_area("Enter your question")

if st.button("Submit"):
    if api_key and prompt:
        # Initialize OpenAI API with provided key
        init_openai(api_key)
        
        # Generate response from the model
        response = generate_response(prompt)
        st.write(response)
    else:
        st.write("Please provide both the API key and a prompt.")
