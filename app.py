import streamlit as st
import os
import openai
from dotenv import load_dotenv
from autogen import ConversableAgent

# Load environment variables from .env file
load_dotenv()  # This loads the .env file, automatically detecting it in the root folder

# Set OpenAI API key from environment variables
openai.api_key = os.getenv('OPENAI_API_KEY')  # Get the API key from the .env file

# Sidebar Layout (Column 1 for logo, company, and developers' names)
with st.sidebar:
    st.image("logo.jpg", width=150)  # Adjust the width of the logo
    st.markdown("""
        # Powered by Aibytec 
        *Developers: Anum Zeeshan & Sabahat Shakeel*
    """)

# Main Layout (Column 2 for the rest of the app content)
col1, col2 = st.columns([1, 5])  # 1:5 ratio for sidebar to content

with col2:
    # Streamlit App Title
    st.title('PODCASTERS')

    # Define the LLM configuration
    llm_config = {"model": "gpt-3.5-turbo"}

    # Termination message logic
    def is_termination_msg(msg, termination_phrases):
        """Check if a message contains any termination phrases."""
        return any(phrase in msg["content"] for phrase in termination_phrases)

    # User Input to define Agent names
    st.subheader('Define Agent Names')
    agent_1 = st.text_input("Enter the First Agent name:", "Huberman-Lab")  # Tech Agent
    agent_2 = st.text_input("Enter the Second Agent name:", "smartless")  # Comedian

    # Define termination phrases for each agent
    agent_1_termination_phrases = [
        "I look forward to continuing our conversation in the future. Take care!"
    ]
    agent_2_termination_phrases = [
        "That works for me! Let’s keep the ideas flowing next time. Take care!",
        "Goodbye"
    ]

    # Create Conversable Agents with dynamic names and role-based system messages
    Agent_1 = ConversableAgent(
        name=agent_1,
        system_message=(
            f"Your name is {agent_1} and you are a knowledgeable Tech Agent. "
            "You provide informative responses related to technology, science, and innovations. "
            "Keep your tone professional and tech-savvy. You may use technical jargon and be precise. "
            "When you're ready to end the conversation, say 'I look forward to continuing our conversation in the future. Take care!'"
        ),
        llm_config=llm_config,
        human_input_mode="NEVER"
    )

    Agent_2 = ConversableAgent(
        name=agent_2,
        system_message=(
            f"Your name is {agent_2} and you are a comedic personality. "
            "You engage with humor, wit, and playful responses. Your role is to entertain, make jokes, "
            "and keep the conversation light-hearted. Don't hesitate to crack a joke or be sarcastic. "
            "When you're ready to end the conversation, say 'That works for me! Let’s keep the ideas flowing next time. Take care!'"
        ),
        llm_config=llm_config,
        human_input_mode="NEVER"
    )

    # User Input to define the start of the conversation
    st.subheader('Start a Conversation')

    # Text input for the first message from the user
    initial_message = st.text_input(f'Define the start of the conversation (Message from {agent_2} to {agent_1}):', 
                                    f'I\'m {agent_2}. {agent_1}, let\'s talk about any topic.')

    # Set number of turns for the conversation
    max_turns = st.slider('Max turns for conversation:', 1, 10, 2)

    # Button to initiate the conversation
    if st.button('Start Conversation'):
        if initial_message:  # Ensure the user has provided a starting message
            try:
                # Start the conversation between the two agents
                chat_result = Agent_2.initiate_chat(
                    recipient=Agent_1,
                    message=initial_message,
                    max_turns=max_turns,
                )

                if chat_result is None:
                    st.error("Error: No chat history returned. Please check the ConversableAgent configuration.")
                else:
                    # Display the conversation history in a professional, user-friendly way
                    st.subheader('Conversation Transcript:')
                    
                    # Assign different colors for each agent
                    agent_1_color = "#3498db"  # Blue for Agent 1 (Tech)
                    agent_2_color = "#e74c3c"  # Red for Agent 2 (Comedian)

                    for i, msg in enumerate(chat_result.chat_history, 1):
                        # Determine which color to use for each agent
                        color = agent_1_color if msg['name'] == agent_1 else agent_2_color
                        # Display the conversation with bold agent names, uppercase and colored text
                        st.markdown(f"<strong style='text-transform: uppercase; color:{color};'>"
                                    f"TURN {i} ({msg['name']}):</strong> <span style='color:{color};'>{msg['content']}</span>", 
                                    unsafe_allow_html=True)

                    # Check for termination message
                    if len(chat_result.chat_history) > 0:
                        last_message = chat_result.chat_history[-1]
                        if is_termination_msg(last_message, agent_1_termination_phrases) or is_termination_msg(last_message, agent_2_termination_phrases):
                            st.success("The conversation ended as per the termination logic.")
                        else:
                            st.info("The conversation is ongoing.")

            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter a valid start message.")
