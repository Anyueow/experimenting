import streamlit as st
from anthropic import Anthropic


# Initialize the API client
def get_grok_client():
    try:
        api_key = st.secrets["XAI_API_KEY"]
        if not api_key:
            raise ValueError("XAI_API_KEY is empty in secrets.")
        return Anthropic(api_key=api_key, base_url="https://api.x.ai")
    except KeyError:
        st.error("XAI_API_KEY not found in secrets.")
        return None
    except ValueError as e:
        st.error(str(e))
        return None


# Main chat interface function
def chat_interface():
    # Initialize client
    client = get_grok_client()
    if client is None:
        st.stop()

    # Set wide layout for the app
    st.set_page_config(layout="wide")
    st.markdown(
        """
        <style>
            /* Page styling */
            .stApp { background-color: #f9f9f9; }

            /* Chat container styling */
            .chat-container { 
                border: 1px solid #ddd; 
                padding: 10px;
                background-color: #ffffff; 
                border-radius: 10px; 
                margin-top: 20px;
            }

            /* Chat message styling */
            .user-message { background-color: #e6f7ff; padding: 10px; border-radius: 5px; margin-bottom: 10px; }
            .assistant-message { background-color: #f0f0f0; padding: 10px; border-radius: 5px; margin-bottom: 10px; }
            .system-message { font-size: 12px; color: #888888; }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Header for the chatbot
    st.title("🎭 Sassy Grok: The AI with Attitude")
    st.markdown("##### *A cute, fun, and sassy AI assistant by @anyueow*")
    st.markdown("""
        <div class="system-message">
        Warning: This model is here for entertainment and scathing replies. Limited to $25 in credits, so proceed with caution! 😉
        </div>
        """, unsafe_allow_html=True)

    # Initialize session state for message history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages with borders and background colors
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for message in st.session_state.messages:
        message_class = "user-message" if message["role"] == "user" else "assistant-message"
        with st.markdown(f'<div class="{message_class}">', unsafe_allow_html=True):
            st.write(f"{message['content']}")
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # User input field
    user_input = st.text_input("Your message:", key="user_input")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.write(user_input)

        # Define system message for sassy personality
        system_message = """You are a witty and sarcastic AI assistant designed to generate content for tweets and witty replies.
        Feel free to:
        - Use playful sarcasm and dark humor
        - Add clever observations and occasional pop culture references
        Just remember: If a question is too boring, tell the user to do better!"""

        # Construct the prompt with conversation history
        conversation_history = "\n".join(
            f"{msg['role'].capitalize()}: {msg['content']}"
            for msg in st.session_state.messages[:-1]
        )

        prompt = f"""System: {system_message}

        Past conversation:
        {conversation_history}

        User: {user_input}
        """

        try:
            # Send prompt to API
            response = client.completions.create(
                model="grok-beta",
                max_tokens_to_sample=128,
                prompt=prompt
            )
            bot_response = response.completion.strip()
            st.session_state.messages.append({"role": "assistant", "content": bot_response})
            with st.markdown(f'<div class="assistant-message">', unsafe_allow_html=True):
                st.write(bot_response)
            st.markdown("</div>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error in API call: {e}")


if __name__ == "__main__":
    chat_interface()
