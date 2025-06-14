import streamlit as st
from openai import OpenAI

# Set your OpenAI API key
# You can store this securely using Streamlit secrets or as an environment variable
# For local development, you might set it directly or load from a .env file
# For deployment on Streamlit Cloud, use st.secrets["OPENAI_API_KEY"]
# client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
client = OpenAI(api_key="AIzaSyBDEAME9W0nT-xU4bvscXdQqy8Nm-6e9lY") # Replace with your actual key for testing, or use st.secrets

st.title("Simple AI Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What's on your mind?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        # Use OpenAI's chat completions
        for chunk in client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += chunk.choices[0].delta.content or ""
            message_placeholder.markdown(full_response + "▌") # Add a blinking cursor effect
        message_placeholder.markdown(full_response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Optional: Add a button to clear chat history
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.experimental_rerun() # Rerun the app to clear the displayed messages