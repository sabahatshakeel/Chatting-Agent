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
    st.image("logo.png", width=320)  # Adjust the width of the logo
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
    llm_config = {"model": "gpt-3.5-turbo", "max_tokens": 65}  # Limit responses to 50 tokens

    # Termination message logic
    def is_termination_msg(msg, termination_phrases):
        """Check if a message contains any termination phrases."""
        return any(phrase in msg["content"] for phrase in termination_phrases)

    # Define termination phrases for each agent
    smartless_termination_phrases = [
        "That works for me! Let’s keep the ideas flowing next time. Take care!",
        "Goodbye"
    ]
    huberman_termination_phrases = [
        "I look forward to continuing our conversation in the future. Take care!"
    ]

    # Create Conversable Agents with updated names and roles
    Agent_1 = ConversableAgent(
        name="smartless",
        system_message=(
            "Your name is smartless and you are a comedic personality. "
            "Keep your responses short, witty, and humorous. Focus on entertaining the audience with brief jokes. "
            "When you're ready to end the conversation, say 'That works for me! Let’s keep the ideas flowing next time. Take care!'"
        ),
        llm_config=llm_config,
        human_input_mode="NEVER"
    )

    Agent_2 = ConversableAgent(
        name="Huberman-Lab",
        system_message=(
            "Your name is Huberman-Lab and you are a knowledgeable Tech Agent. "
            "You provide short, concise, and informative responses related to technology, science, and innovations. "
            "Focus on keeping the conversation informative but succinct. When you're ready to end the conversation, "
            "say 'I look forward to continuing our conversation in the future. Take care!'"
        ),
        llm_config=llm_config,
        human_input_mode="NEVER"
    )

    # User Input to define the start of the conversation
    st.subheader('Start a Conversation')

    # Text input for the first message from the user
    initial_message = st.text_input('Define the start of the conversation (Message from smartless to Huberman-Lab):', 
                                    'I\'m smartless. Huberman-Lab, let\'s talk about any topic.')

    # Button to initiate the conversation
    if st.button('Start Conversation'):
        if initial_message:  # Ensure the user has provided a starting message
            try:
                # Start the conversation between the two agents
                chat_result = Agent_1.initiate_chat(
                    recipient=Agent_2,
                    message=initial_message,
                    max_turns=2  # Only 2 turns, no user choice required
                )

                if chat_result is None:
                    st.error("Error: No chat history returned. Please check the ConversableAgent configuration.")
                else:
                    # Display the conversation history in a professional, user-friendly way
                    st.subheader('Conversation Transcript:')
                    
                    # Assign different colors for each agent
                    smartless_color = "#e74c3c"  # Red for smartless (Comedian)
                    huberman_color = "#3498db"  # Blue for Huberman-Lab (Tech)

                    for i, msg in enumerate(chat_result.chat_history, 1):
                        # Determine which color to use for each agent
                        color = smartless_color if msg['name'] == "smartless" else huberman_color
                        # Display the conversation with bold agent names, uppercase and colored text
                        st.markdown(f"<strong style='text-transform: uppercase; color:{color};'>"
                                    f"TURN {i} ({msg['name']}):</strong> <span style='color:{color};'>{msg['content']}</span>", 
                                    unsafe_allow_html=True)

                    # Check for termination message
                    if len(chat_result.chat_history) > 0:
                        last_message = chat_result.chat_history[-1]
                        if is_termination_msg(last_message, smartless_termination_phrases) or is_termination_msg(last_message, huberman_termination_phrases):
                            st.success("The conversation ended as per the termination logic.")
                        else:
                            st.info("The conversation is ongoing.")

            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter a valid start message.")
