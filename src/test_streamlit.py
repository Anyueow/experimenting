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

    # Set page configuration for wide layout
    st.set_page_config(layout="wide")

    # Header for the chatbot
    st.title("🎭 Sassy Grok: The AI with Attitude")
    st.markdown("##### *An irreverent AI assistant by @anyueow*")
    st.markdown("""
        **Warning:** This model is here for entertainment and scathing replies only. Use sparingly if you value your ego! 😉
    """)

    # Initialize session state for message history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages with default Streamlit chat styling
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message("user"):
                st.write(message["content"])
        else:
            with st.chat_message("assistant"):
                st.write(message["content"])

    # User input field at the bottom of the page
    user_input = st.chat_input("Your message:")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
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
            with st.chat_message("assistant"):
                st.write(bot_response)
        except Exception as e:
            st.error(f"Error in API call: {e}")


if __name__ == "__main__":
    chat_interface()
