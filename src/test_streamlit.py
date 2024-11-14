import streamlit as st
from anthropic import Anthropic

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

def chat_interface():
    client = get_grok_client()
    if client is None:
        st.stop()

    st.title("Grok AI Chatbot")
    st.write("Ask Grok anything!")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    user_input = st.chat_input("Your message:")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        try:
            response = client.completions.create(
                model="grok-1",
                max_tokens=128,
                messages=st.session_state.messages,
                stream=False
            )
            bot_response = response.completion.strip()
            st.session_state.messages.append({"role": "assistant", "content": bot_response})
            with st.chat_message("assistant"):
                st.write(bot_response)
        except Exception as e:
            st.error(f"Error in API call: {e}")

if __name__ == "__main__":
    chat_interface()
