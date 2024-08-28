import os
import streamlit as st
import google.generativeai as genai

def main():
    # Set your Gemini API key directly here
    api_key = 'AIzaSyCSrEWAwXi7JJ6AtOx5Xq6HKJukAyHYsn8'  
    genai.configure(api_key=api_key)

    # Set up the Streamlit interface
    st.title("Chatbot")

    # Custom CSS for styling the conversation
    st.markdown(
        """
        <style>
        .user-message {
            background-color: #DCF8C6;
            color: #000000;
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 10px;
            max-width: 80%;
            float: left;
            clear: both;
        }
        .assistant-message {
            background-color: #F1F0F0;
            color: #000000;
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 10px;
            max-width: 80%;
            float: right;
            clear: both;
        }
        .message-box {
            margin: 0;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # User input for chatbot interaction
    user_input = st.text_input("You:", placeholder="Ask me anything...")

    # Initialize session state to store conversation history
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []

    # Button to interact with the chatbot
    if st.button("Send") and user_input.strip():
        try:
            # Add user input to the conversation history
            st.session_state.conversation_history.append(f"You: {user_input}")

            # Create a prompt for the chatbot
            prompt = f"""
            The following is a conversation with a helpful assistant. The assistant is helpful, creative, clever, and very friendly.

            {" ".join(st.session_state.conversation_history)}

            Assistant:
            """

            # Use the Gemini generative model to generate the chatbot's response
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            chatbot_reply = response.text.strip()

            # Add the chatbot's reply to the conversation history
            st.session_state.conversation_history.append(f"Assistant: {chatbot_reply}")

        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.warning("We couldn't process your request. Please try again later.")
    elif not user_input.strip():
        st.warning("Please enter a message.")

    # Display the conversation history with custom styles
    if st.session_state.conversation_history:
        st.subheader("Conversation:")
        for i, message in enumerate(st.session_state.conversation_history):
            if message.startswith("You:"):
                st.markdown(f'<div class="user-message"><p class="message-box">{message}</p></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="assistant-message"><p class="message-box">{message}</p></div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
