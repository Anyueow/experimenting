import streamlit as st
import requests


def get_grok_client():
    try:
        api_key = st.secrets["XAI_API_KEY"]
        if not api_key:
            raise ValueError("XAI_API_KEY is empty in secrets.")
        return api_key
    except KeyError as e:
        st.error("XAI_API_KEY not found in secrets.")
        raise e


def chat_interface():
    try:
        api_key = get_grok_client()
    except Exception as e:
        st.error(f"Failed to initialize client: {e}")
        return

    st.title("Grok AI Chatbot")
    st.write("Ask Grok anything!")

    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Get user input
    user_input = st.chat_input("Your message:")

    if user_input:
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        try:
            # Prepare headers and payload for X.AI API
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "messages": st.session_state.messages,
                "model": "grok-1",
                "max_tokens": 128,
                "stream": False
            }

            # Make API call to X.AI
            response = requests.post(
                "https://api.x.ai/v1/chat/completions",
                headers=headers,
                json=payload
            )

            if response.status_code != 200:
                raise Exception(f"API call failed with status code {response.status_code}: {response.text}")

            response_data = response.json()
            bot_response = response_data['choices'][0]['message']['content']

            # Add assistant message to chat
            st.session_state.messages.append({"role": "assistant", "content": bot_response})
            with st.chat_message("assistant"):
                st.write(bot_response)

        except Exception as e:
            st.error(f"Error in API call: {e}")


if __name__ == "__main__":
    chat_interface()